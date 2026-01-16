from scene.scene_builder import SceneBuilder
from scene.frame_sampler import FrameSampler       
from scene.frame_analyzer import FrameAnalyzer  
from video_io import VideoReader
from llm.qwen_client import QwenClient
from llm.prompt_builder import build_prompt
from tts_engine import QwenTTSEngine  
from video_to_description_mapper import map_video_to_event_info
from merge import VideoAudioMerger
from pathlib import Path
import dashscope
import os

API_KEY = "key"

def start(video_path: str, output_subfolder: str):
    """
    对单个视频生成中文解说、TTS，并输出合成视频到 output_subfolder
    """
    # 1. 读视频
    video = VideoReader(video_path)
    sampler = FrameSampler(video.fps)

    # 2. 获取关键帧 & 索引
    frames = sampler.get_keyframes(video)
    frame_indices = sampler.get_keyframe_indices()

    # 3. offense 判断 + 描述
    qwen = QwenClient(API_KEY)
    descriptor = FrameAnalyzer(qwen)
    frame_desc_info = descriptor.analyze(frames)

    # 4. 构建事件对象
    pbp_json_path = "Game_PBP_zh.json"
    event_info = map_video_to_event_info(video_path, pbp_json_path)

    # 5. 构建 scene
    scene = SceneBuilder().build(frame_indices, event_info, frame_desc_info)

    # 6. 根据视频时长计算最大字符数
    clip_sec = video.get_duration()
    video.release()
    chars_per_sec = 5
    max_chars = min(int(clip_sec * chars_per_sec), 35)

    # 7. 构造 prompt
    prompt = build_prompt(scene, max_chars)
    print("=== Prompt ===")
    print(prompt)

    # 8. 调用 Qwen SDK
    dashscope.api_key = API_KEY
    response = dashscope.Generation.call(
        model="qwen-plus",
        prompt=prompt
    )
    commentary_text = response.output.text
    print("=== 中文解说 ===")
    print(commentary_text)

    # 9. 调用 TTS
    tts = QwenTTSEngine(api_key=API_KEY)
    audio_result = tts.synthesize(commentary_text)
    print("=== TTS 输出 ===")
    print("音频路径:", audio_result["audio_path"])
    print("音频时长（秒）:", audio_result["duration_sec"])

    # 10. 合成音视频
    merger = VideoAudioMerger(output_dir=output_subfolder)
    final_video = merger.merge(
        video_path=video_path,
        audio_path=audio_result["audio_path"]
    )
    print(f"生成完成，保存到: {final_video}\n")


if __name__ == "__main__":
    clips_root = Path("clip")  # 输入根目录
    output_root = Path("output")  # 输出根目录
    output_root.mkdir(exist_ok=True)

    # 遍历 clip/下的每个子文件夹
    for subfolder in clips_root.iterdir():
        if not subfolder.is_dir():
            continue  # 跳过文件

        # 输出对应子文件夹
        output_subfolder = output_root / subfolder.name
        output_subfolder.mkdir(exist_ok=True)

        # 遍历子文件夹下的所有视频
        for video_file in subfolder.glob("*.mp4"):
            print(f"处理视频: {video_file}")
            start(str(video_file), str(output_subfolder))
