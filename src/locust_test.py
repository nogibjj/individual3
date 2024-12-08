from locust import HttpUser, task


class WebsiteUser(HttpUser):
    host = "https://crispy-space-spork-g457q5j94x643wj9q-5000.app.github.dev"
    # wait_time = between(1, 5)

    @task
    def home_page(self):
        """Test the home page"""
        self.client.get("/")

    @task
    def input_page(self):
        """Test the input"""
        payload = {
            "gender": "female",
            "age": 30,
            "height_ft": 5,
            "height_in": 6,
            "weight_lbs": 160.0,
            "target_weight_lbs": 140.0,
            "duration_days": 90,
            "weekly_frequency": 4,
        }
        with self.client.post(
            "/input", data=payload, catch_response=True
        ) as response:
            if (
                response.status_code == 200
                and "error_message" not in response.text
            ):
                response.success()
            else:
                response.failure(
                    "Input validation failed or error message displayed."
                )

    @task
    def result_page(self):
        """Test the result"""
        self.client.get("/result")
