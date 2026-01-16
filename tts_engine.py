# tts_engine.py
import dashscope
import uuid
import os
import requests
import wave

class QwenTTSEngine:
    def __init__(self, api_key: str, output_dir="tts_output"):
        self.api_key = api_key
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def synthesize(self,text: str) -> dict:
        filename = f"{uuid.uuid4().hex}.wav"
        output_path = os.path.join(self.output_dir, filename)
        response = dashscope.MultiModalConversation.call(
            model="qwen3-tts-flash",
            api_key=self.api_key,
            text=text,
            voice="Cherry",
            language_type="Chinese", 
            stream=False
        )

        audio_url = response.output.audio.url
        save_path = output_path
        try:
            response = requests.get(audio_url)
            response.raise_for_status()  # 检查请求是否成功
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"音频文件已保存至：{save_path}")
        except Exception as e:
            print(f"下载失败：{str(e)}")

        """""
        调用 云端 TTS 模型
        把 text 转成语音
        """

        duration = self._get_wav_duration(output_path)

        return {
            "audio_path": output_path,
            "duration_sec": duration
        }

    def _get_wav_duration(self, path: str) -> float:
        with wave.open(path, "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate)