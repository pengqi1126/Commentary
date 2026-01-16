# frame_info.py
from dataclasses import dataclass

@dataclass
class FrameInfo:
    """
    一个帧的结构化描述
    """
    name: str         # 帧类型：pre_shot / made / score_updated
    index: int        # 视频帧索引
    description: str  # 文本描述，用于 LLM prompt
