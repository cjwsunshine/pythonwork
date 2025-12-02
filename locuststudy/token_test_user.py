from locust import HttpUser, task, between
import json
import time


class TokenTestUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://api.deepseek.com"  # 或者您的智能体 API 地址

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer ysk-a83a41f3f245431a9c2a57dc187faac9"
        }

    @task
    def test_chat_completion(self):
        # 测试不同长度的消息来观察 token 消耗
        test_messages = [
            "Hello, how are you?",
            "请解释一下人工智能的基本概念和发展历程",
            "Write a detailed analysis of the current trends in machine learning and artificial intelligence, including transformer architectures, reinforcement learning, and their applications in various industries."
        ]

        for message in test_messages:
            payload = {
                "model": "deepseek-chat",  # 或您的模型名称
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello!"}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }

            with self.client.post("https://api.deepseek.com/chat/completions",
                                  json=payload,
                                  headers=self.headers,
                                  catch_response=True) as response:
                if response.status_code == 200:
                    # 解析响应获取 token 使用情况
                    data = response.json()
                    completion_tokens = data.get("usage", {}).get("completion_tokens", 0)
                    prompt_tokens = data.get("usage", {}).get("prompt_tokens", 0)
                    total_tokens = data.get("usage", {}).get("total_tokens", 0)

                    # 记录 token 使用情况
                    response.success()
                    print(
                        f"Prompt: {message[:50]}... | Prompt tokens: {prompt_tokens}, Completion: {completion_tokens}, Total: {total_tokens}")
                else:
                    response.failure(f"Status: {response.status_code}")

