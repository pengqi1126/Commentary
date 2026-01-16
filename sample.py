import os
import shutil
import random

# ===== 配置 =====
# 桌面路径（可改为你的实际路径）
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
RESULT_FOLDER = os.path.join("/Volumes/pq的硬盘", "result")
CLIP_FOLDER = os.path.join(DESKTOP_PATH, "clip")     # 采样目标根文件夹

SAMPLE_RATIO = 0.1  # 采样比例 10%

# ===== 创建 clip 根目录 =====
os.makedirs(CLIP_FOLDER, exist_ok=True)

# ===== 遍历 result 文件夹 =====
for subfolder_name in os.listdir(RESULT_FOLDER):
    subfolder_path = os.path.join(RESULT_FOLDER, subfolder_name)
    if not os.path.isdir(subfolder_path):
        continue  # 跳过文件

    # 获取所有视频文件
    clips = [f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))]
    if not clips:
        continue  # 子文件夹为空

    # 计算采样数量（至少 1 个）
    sample_count = max(1, int(len(clips) * SAMPLE_RATIO))

    # 随机选择采样视频
    sample_clips = random.sample(clips, sample_count)

    # 在 clip 根目录下创建同名子文件夹
    target_subfolder = os.path.join(CLIP_FOLDER, subfolder_name)
    os.makedirs(target_subfolder, exist_ok=True)

    # 复制选中的视频
    for clip_name in sample_clips:
        src_path = os.path.join(subfolder_path, clip_name)
        dst_path = os.path.join(target_subfolder, clip_name)
        shutil.copy2(src_path, dst_path)

    print(f"{subfolder_name}: {len(sample_clips)} 个视频已采样到 clip/{subfolder_name}")

print("采样完成！")