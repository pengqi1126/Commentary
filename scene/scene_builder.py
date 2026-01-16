# scene_builder.py

from scene.frame_info import FrameInfo

class SceneBuilder:
    """
    构建单事件 scene，直接使用 FrameAnalyzer 输出的信息
    """

    def build(
        self,
        frame_indices: dict,
        event_info: dict,
        frame_desc_info: dict
    ) -> dict:
        """
        Args:
            frame_indices: {'sec_2': int, 'sec_4': int, 'sec_6': int}
            event_info: PBP json 信息
            frame_desc_info: FrameAnalyzer.analyze() 输出
                {
                    "sec_2_desc": str,
                    "sec_4_desc": str,
                    "sec_6_desc": str
                }

        Returns:
            dict: scene 对象
        """

        frames = {}

        # sec_2 / sec_4 / sec_6 描述
        frames['sec_2'] = FrameInfo(
            name='sec_2',
            index=frame_indices['sec_2'],
            description=frame_desc_info["sec_2_desc"]
        )
        frames['sec_4'] = FrameInfo(
            name='sec_4',
            index=frame_indices['sec_4'],
            description=frame_desc_info["sec_4_desc"]
        )
        frames['sec_6'] = FrameInfo(
            name='sec_6',
            index=frame_indices['sec_6'],
            description=frame_desc_info["sec_6_desc"]
        )

        # 起讲时间固定从 sec_2 开始
        start_second = 2.0

        scene = {
            "start_second": start_second,
            "event_type": event_info.get('event_type', 'two_point_made'),
            "frames": frames,
            "home_points": event_info.get('home_points', 0),
            "away_points": event_info.get('away_points', 0),
            "quarter": event_info.get('quater', "Q?"),
            "home_team": event_info.get('home_team', ""),
            "away_team": event_info.get('away_team', ""),
            "event_description": event_info.get('description', "")
        }

        return scene
