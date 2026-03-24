from locust import HttpUser, task, between
import json
import random

PROMPTS = [
    "Explain quantum computing in simple words.",
    "Write a short story about space exploration.",
    "Summarize the importance of cybersecurity.",
    "Describe how load testing works.",
]


class LLMSyncUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def generate_text_sync(self):
        query = random.choice(PROMPTS)

        response = self.client.post("/chat/sync", json={"query": query})

        if response.status_code != 200:
            print("Error:", response.text)


class LLMASyncUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def generate_text_async(self):
        query = random.choice(PROMPTS)

        response = self.client.post("/chat/async", json={"query": query})

        if response.status_code != 200:
            print("Error:", response.text)
