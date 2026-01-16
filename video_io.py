import cv2
import numpy as np

class VideoReader:
    def __init__(self, path: str):
        self.path = path
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open video: {path}")

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.frame_count / self.fps

    def get_frame(self, index: int):
        """读取指定帧（BGR ndarray）"""
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError(f"Cannot read frame {index}")
        return frame

    def get_frame_at_second(self, sec: float):
        """读取指定秒的帧"""
        index = int(sec * self.fps)
        return self.get_frame(index)
    
    def get_duration(self):
        return self.duration

    def release(self):
        self.cap.release()
