from pathlib import Path
import json
from typing import Dict

def map_video_to_event_info(video_path: str, pbp_json_path: str) -> Dict[str, str | int]:
    """
    将单个视频文件映射到 PBP JSON 的事件信息，包括 description、home_points、away_points、quarter 等。

    Args:
        video_path: 视频文件路径
        pbp_json_path: PBP JSON 文件路径

    Returns:
        Dict 包含事件信息
        {
            "description": str,
            "home_points": int,
            "away_points": int,
            "event_type": str,
            "home_team": str,
            "away_team": str,
            "quater": str
        }
    """
    # 1. 读取 PBP JSON
    with open(pbp_json_path, "r", encoding="utf-8") as f:
        pbp_data = json.load(f)

    home_team = pbp_data["home"]["name"]
    away_team = pbp_data["away"]["name"]

    # 2. 构建短 event_id -> 事件信息 映射
    short_id_to_event = {}
    for period_data in pbp_data.get("periods", []):
        period_number = period_data.get("number")
        for event in period_data.get("events", []):
            full_id = str(event.get("id"))
            short_id = full_id[:8] if len(full_id) > 8 else full_id

            description = event.get("description", "")
            home_points = event.get("home_points", 0)
            away_points = event.get("away_points", 0)
            event_type = event.get("event_type", "unknown")

            short_id_to_event[short_id] = {
                "description": description,
                "home_points": home_points,
                "away_points": away_points,
                "event_type": event_type
            }

    # 3. 处理单个视频文件
    video_file = Path(video_path)
    basename = video_file.stem
    if "_" not in basename:
        raise ValueError(f"视频文件 {video_file} 命名不符合规则：eventid_quater.mp4")
    event_id_short, quater = basename.split("_")

    event_info = short_id_to_event.get(event_id_short)
    if not event_info:
        raise ValueError(f"找不到匹配 PBP event，视频文件 {video_file}")

    # 添加额外信息
    event_info["home_team"] = home_team
    event_info["away_team"] = away_team
    event_info["quater"] = quater

    return event_info


if __name__ == "__main__":
    video_path = "clips/0f3f2b02_Q4.mp4"
    pbp_json_path = "Game_PBP_zh.json"

    event_info = map_video_to_event_info(video_path, pbp_json_path)
    print(f"视频: {video_path}")
    print(f"Description: {event_info}")
