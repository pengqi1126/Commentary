# prompt_builder.py

from typing import Dict, Optional

def build_prompt(scene: Dict, max_chars: Optional[int] = None, min_chars: Optional[int] = None) -> str:
    """
    根据不同事件类型生成对应的比赛解说 prompt。
    
    scene = {
        "home_team": "步行者",
        "away_team": "尼克斯",
        "quarter": "Q4",
        "home_points": 102,
        "away_points": 98,
        "event_type": "twopointmade",  # twopointmade, threepointmade, opentip, freethrowmade, freethrowmiss, turnover, rebound, personalfoul, shootingfoul, lineupchange
        "event_description": "OG 安努诺比投中二分回转斜投（乔什·哈特助攻）",
        "frames": {
            "sec_2": Frame(desc="球员持球突破"),
            "sec_4": Frame(desc="球起手投篮"),
            "sec_6": Frame(desc="篮球命中篮筐")
        }
    }
    """

    frames = scene.get("frames", {})
    sec_2_desc = frames.get("sec_2").description if frames.get("sec_2") else ""
    sec_4_desc = frames.get("sec_4").description if frames.get("sec_4") else ""
    sec_6_desc = frames.get("sec_6").description if frames.get("sec_6") else ""

    event_type = scene.get("event_type", "twopointmade").lower()

    # ==========================
    # Event-specific generation rules
    # ==========================
    # ===== 事件类型对应 prompt 规则 =====
    if event_type in ["twopointmade", "threepointmade", "opentip"]:
        generation_rules = """
- 描述一次完整进攻过程
- 按“出手 → 投篮结果 → 得分成立”顺序描述
- 可自然使用“随后 / 接着 / 最终”
- 可以适当提高情绪，渲染进球的喜悦气氛
- 可以适当使用修辞，让观众感受进球激动
- 如果片段有回放镜头，可以适当解说分析
"""
    elif event_type in ["twopointmiss", "threepointmiss", "fieldgoal"]:
        generation_rules = """
- 描述一次完整进攻过程
- 按“出手 → 投篮未中 → 篮板争抢或回合延续”顺序描述
- 可适当描述球员动作或防守反应
- 不渲染得分喜悦，但可适当说明紧张氛围
- 如果片段有回放镜头，可以适当解说分析
"""
    elif event_type in ["freethrowmade", "freethrowmiss", "freethrow"]:
        generation_rules = """
- 描述罚球回合
- 说明罚球是否命中
- 若只出现一次罚球，不虚构连续罚球
- 可弱化画面动作描述
"""
    elif event_type == "assist":
        generation_rules = """
- 描述助攻过程
- 指明传球球员和接球球员
- 描述球员动作与配合，但不评价球员表现
"""
    elif event_type in ["turnover"]:
        generation_rules = """
- 描述失误发生方式
- 明确球权被对方获得
- 不描述比分变化
"""
    elif event_type in ["rebound"]:
        generation_rules = """
- 说明投篮未中或争抢篮板背景
- 区分进攻篮板或防守篮板
- 指明回合是否延续或结束
"""
    elif event_type in ["block", "steal"]:
        generation_rules = """
- 描述防守动作发生瞬间
- 明确进攻被打断或投篮受阻
- 不夸大防守效果
"""
    elif event_type in ["personalfoul", "shootingfoul", "offensivefoul"]:
        generation_rules = """
- 简要描述动作（犯规类型）
- 不推断比赛外信息
- 不补充未出现的结果
"""
    elif event_type in ["lineupchange", "teamtimeout"]:
        generation_rules = """
- 简要说明换人或暂停情况
- 不评论策略，仅描述事件
"""
    elif event_type in ["fouldrawn"]:
        generation_rules = """
- 描述被犯规的球员动作
- 可说明犯规对比赛的影响
- 不进行夸张评价
"""
    elif event_type == "jumpball":
        generation_rules = """
- 描述跳球场景
- 指明参与球员和球权归属
- 可说明比赛开局或特殊争球情况
"""
    else:
        # fallback
        generation_rules = """
- 描述画面中最明确的比赛动作
- 不虚构比赛结果
"""

    # ==========================
    # Build prompt
    # ==========================
    prompt = f"""
你是一名篮球比赛解说员。
请根据以下信息，生成一条中文比赛解说,
描述应与画面同步，优先参考“事件发展”中的视频帧描述,讲清楚事件类型，使用事件描述的人名，而不是简单复述事件描述。
不要出现英文


比赛信息：
- 主队：{scene.get('home_team', '')}
- 客队：{scene.get('away_team', '')}
- 当前节数：{scene.get('quarter', 'Q?')}
- 进球后比分：home 比 away = {scene.get('home_points', '')} 比 {scene.get('away_points', '')}

事件类型：event_type

事件描述：
- {scene.get('event_description', '')}

事件发展（视频关键帧）：
- 第2秒：{sec_2_desc}
- 第4秒：{sec_4_desc}
- 第6秒：{sec_6_desc}

生成要求：
{generation_rules}
"""

    # 可选字数约束
    if max_chars is not None:
        prompt += f"\n- 解说不超过 {max_chars} 字"
    if min_chars is not None:
        prompt += f"\n- 解说不少于 {min_chars} 字"

    # 清理多余空行
    prompt = "\n".join(line.strip() for line in prompt.strip().splitlines() if line.strip())

    return prompt
