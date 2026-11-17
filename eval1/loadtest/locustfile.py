from locust import HttpUser, task, constant
import random

class MusicUser(HttpUser):
    wait_time = constant(0)

    @task
    def check_stream(self):
        listener_id = random.randint(1, 5)
        track_id = random.randint(1, 10)
        self.client.get(f"/stream/check?listener_id={listener_id}&track_id={track_id}", name="/stream/check")
