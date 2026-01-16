# frame_analyzer.py

from llm.qwen_client import QwenClient

class FrameAnalyzer:
    """
    对关键帧进行智能分析：
    - 每个关键帧生成一句中文描述
    """

    def __init__(self, qwen_client: QwenClient):
        self.qwen = qwen_client

    def analyze(self, frames: dict) -> dict:
        """
        Args:
            frames: {
                "sec_2": ndarray,        # 2秒画面
                "sec_4": ndarray,        # 4秒画面
                "sec_6": ndarray         # 6秒画面
            }
        Returns:
            dict:
            {
                "sec_2_desc": str,
                "sec_4_desc": str,
                "sec_6_desc": str
            }
        """
        sec_2_desc = self._describe_single_frame(frames["sec_2"], "sec_2")
        sec_4_desc = self._describe_single_frame(frames["sec_4"], "sec_4")
        sec_6_desc = self._describe_single_frame(frames["sec_6"], "sec_6")

        return {
            "sec_2_desc": sec_2_desc,
            "sec_4_desc": sec_4_desc,
            "sec_6_desc": sec_6_desc
        }

    def _describe_single_frame(self, frame, frame_type: str) -> str:
        """
        frame_type: 用于定制提示
        """
        prompt = f"""
        你是一名篮球比赛分析助手。
        描述该比赛画面，双方队员状态，客观简短中文描述。
        只返回一句中文描述文本。
        """
        return self.qwen.call(frame, prompt)
