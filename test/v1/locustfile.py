from locust import HttpUser, task, between
import random


class TimeSaleUser(HttpUser):
    """
    타임세일 구매 API 성능 테스트를 위한 Locust 사용자 클래스
    """
    wait_time = between(1, 2.5)  # 각 작업 실행 사이의 대기 시간 (초)

    @task
    def purchase_timesale(self):
        """
        타임세일 구매 API (TimeSaleOrderView.post) 호출
        """
        # 테스트를 위한 더미 데이터
        # 실제 환경에서는 유효한 timesale_id, user_id, quantity를 사용해야 합니다.
        timesale_id = 1222  # 예시 timesale_id. 실제 테스트에서는 여러 ID를 사용하거나 동적으로 생성할 수 있습니다.
        user_id = random.randint(1, 1000)  # 1부터 1000까지의 랜덤 user_id
        quantity = random.randint(1, 5)  # 1부터 5까지의 랜덤 구매 수량

        payload = {
            "user_id": user_id,
            "quantity": quantity
        }

        # API 엔드포인트: /timesales/{timesale_id}/purchase
        self.client.post(f"/api/v1/timesales/{timesale_id}/purchase", json=payload)
