# merge.py
import subprocess
from pathlib import Path


class VideoAudioMerger:
    """
    使用 FFmpeg 将视频与解说音频合成为最终视频
    输出路径统一由类内部管理
    """

    def __init__(
        self,
        output_dir: str = "output",
        video_codec: str = "copy",
        audio_codec: str = "aac",
        overwrite: bool = True,
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.video_codec = video_codec
        self.audio_codec = audio_codec
        self.overwrite = overwrite

    def get_output_path(self, video_path: str) -> Path:
        """
        clips/0f3f2b02_Q4.mp4
        -> output/0f3f2b02_Q4C.mp4
        """
        video_file = Path(video_path)
        return self.output_dir / f"{video_file.stem}C{video_file.suffix}"

    def merge(self, video_path: str, audio_path: str) -> Path:
        """
        合并视频和音频，输出到 output_dir
        """
        video_file = Path(video_path)
        audio_file = Path(audio_path)
        output_file = self.get_output_path(video_path)

        cmd = ["ffmpeg"]
        if self.overwrite:
            cmd.append("-y")

        cmd += [
            "-i", str(video_file),
            "-i", str(audio_file),
            "-loglevel", "error",
            "-c:v", self.video_codec,
            "-c:a", self.audio_codec,
            "-shortest",
            str(output_file),
        ]

        subprocess.run(cmd, check=True)
        print(f"合成完成: {output_file}")

        return output_file
