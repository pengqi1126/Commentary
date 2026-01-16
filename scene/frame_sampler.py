import tempfile
import cv2
from typing import Dict, List

class FrameSampler:
    """
    关键帧抽取，返回 BGR ndarray
    """

    def __init__(self, fps: float):
        self.fps = fps

    def get_keyframes(self, video) -> Dict[str, any]:
        """
        video: VideoReader
        Returns:
        """
        return {
            "sec_2": video.get_frame_at_second(2.0),
            "sec_4": video.get_frame_at_second(4.0),
            "sec_6": video.get_frame_at_second(6.0)
        }

    def get_keyframe_indices(self) -> Dict[str, int]:
        """
        Returns:
            dict: {"pre_shot":int(fps*2), "made": int(fps*4), "score_updated": int(fps*6)}
        """
        return {
            "sec_2": int(self.fps * 2),
            "sec_4": int(self.fps * 4),
            "sec_6": int(self.fps * 6)
        }
