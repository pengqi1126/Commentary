🚀 快速开始

前置要求

Python 3.8+
FFmpeg（视频处理）
通义千问 API 密钥（或其他 LLM 服务）

安装步骤
# 克隆仓库
git clone https://github.com/pengqi1126/Commentary.git
cd Commentary


🏗️ 系统架构

1️⃣ 视频处理层 🎥

video_io.py - 视频读取器
核心方法：get_frame(second) - 精确获取视频第 X 秒的画面
职责：处理不同视频格式，管理视频流，提供精确时间戳定位

frame_sampler.py - 关键帧采样器
功能：选择需要分析的关键帧（目前固定第2/4/6秒的三个frame）
输出：frames

2️⃣ 内容分析层 🔍

frame_analyzer.py - 视觉分析引擎
功能：将画面转换为文字描述
流程：接收帧 → 调用视觉模型 → 生成自然语言描述

qwen-client.py - 通义千问模型客户端
功能：连接阿里云通义千问-Plus 模型
输入：JPG 图片 + 自定义提示词（prompt）
输出：针对画面的详细文字描述（字符串）

3️⃣ 数据整合层 📊

video_to_description_mapper.py - 事件映射器
功能：将视频片段与PBP JSON关联
关键：通过 clip 文件名反查 PBP JSON（Play-by-Play，逐播报）文件
输出：event_info - 包含事件类型，事件描述，比分等

scene_builder.py - 场景构造器
功能：融合视觉内容与事件数据，构建完整场景
输入：frames 描述 + event_info
输出：scene 对象 - 包含frames, event_info的复合结构

4️⃣ 内容生成层 ✍️
prompt_builder.py - 提示词工程师
功能：根据场景类型生成优化的 LLM 提示词
输入：scene 对象
输出：针对不同 event_type 的专业解说 prompt

main.py - 总控与中文解说生成
功能：项目主控制器，协调所有模块
调用 LLM 生成中文解说文本

5️⃣ 输出合成层 🔊
tts_engine.py - 语音合成器
功能：将文字解说转换为自然语音
技术：使用 qwen_tts 引擎
输出：与解说文本同步的音频文件

merge.py - 多媒体合成器
功能：将各个组件合并为最终成品
合成内容：
原始/处理后的视频流
生成的解说语音
输出：可直接分发的完整解说视频

🔄 完整数据处理流程

输入：原始视频 + PBP JSON（专业赛事数据）
抽取：获取关键帧 → 分析画面内容 → 关联专业事件数据
理解：构建场景对象 → 生成针对性提示词
创作：LLM生成中文解说 → TTS转为语音
合成：语音 + 视频 + 字幕合并输出



场景感知解说：不同事件类型触发不同的解说风格

端到端自动化：从原始视频到成品解说全自动处理

高度模块化：各组件可独立替换或升级
