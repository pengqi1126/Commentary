import dashscope
import cv2
import tempfile

class QwenClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def call(self, frame, prompt: str) -> str:
        """
        frame: BGR ndarray
        prompt: str
        """
        # 1. 写临时 JPEG
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_file:
            cv2.imwrite(tmp_file.name, frame)

            messages = [
                {
                    "role": "user",
                    "content": [
                        {"image": tmp_file.name},  # 文件路径
                        {"text": prompt}
                    ]
                }
            ]

            try:
                response = dashscope.MultiModalConversation.call(
                    api_key=self.api_key,
                    model="qwen3-vl-plus",
                    messages=messages
                )
                if response and getattr(response, "output", None) and getattr(response.output, "choices", None):
                    return response.output.choices[0].message.content[0]["text"].strip()
                else:
                    print("警告: Qwen 返回 None 或没有 output")
                    return ""
            except Exception as e:
                print(f"调用 Qwen 失败: {e}")
                return ""
