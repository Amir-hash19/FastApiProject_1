from locust import task, between, HttpUser


class PaymentUser(HttpUser):
    wait_time = between(1,3)

    def on_start(self):
        response = self.client.post("/api/v1/login",json={
        "email": "alitesti12@email.com",
        "password": "stringst12"
    },
    headers={"accept": "application/json"}
)

        if response.status_code in [200, 202]:
            data = response.json()
            self.access_token = data.get("access_token")
            if not self.access_token:
                print("⚠️ access_token دریافت نشد:", data)
        else:
            print(f"⚠️ Login ناموفق: {response.status_code} - {response.text}")
            self.access_token = None  # جلوگیری از AttributeError

    @task
    def get_payments(self):
        if not hasattr(self, "access_token") or not self.access_token:
            print("⚠️ توکن موجود نیست، skip request")
            return

        response = self.client.get(
            "/api/v1/payments",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "accept": "application/json"
            }
        )
        print(response.status_code, response.text)
