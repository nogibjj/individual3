from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Simulates user wait time between requests
    host = "http://localhost:8080"  # Base host of the app

    @task(1)
    def load_homepage(self):
        # Test the home route
        self.client.get("/")

    @task(3)
    def submit_input_and_get_result(self):
        # Simulate user filling the form and submitting it
        payload = {
            "gender": "Male",
            "age": 30,
            "height_ft": 5,
            "height_in": 10,
            "weight_lbs": 180,
            "target_weight_lbs": 160,
            "num_of_weeks": 12,
            "weekly_frequency": 3,
            "exercise_intensity": 2,
        }
        response = self.client.post("/input", data=payload)
        
        if response.status_code == 200:
            # Fetch the result page if form submission was successful
            self.client.get("/result")
