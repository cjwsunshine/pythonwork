from locust import HttpUser, task, between
from locust import events
import time


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    """初始化自定义统计"""
    global token_stats
    token_stats = {
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "request_count": 0
    }


class AdvancedTokenTestUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def test_with_custom_metrics(self):
        # 您的测试逻辑
        payload = {"message": "测试 token 消耗"}

        with self.client.post("/api/chat", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                # 假设响应包含 token 使用信息
                data = response.json()
                input_tokens = data.get("input_tokens", 0)
                output_tokens = data.get("output_tokens", 0)

                # 更新全局统计
                token_stats["total_input_tokens"] += input_tokens
                token_stats["total_output_tokens"] += output_tokens
                token_stats["request_count"] += 1

                response.success()


# 定期打印统计信息
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, context, **kwargs):
    if context and "input_tokens" in context:
        print(f"Token Usage - Input: {context['input_tokens']}, Output: {context['output_tokens']}")