# actor.py
import requests

class Actor:
    def __init__(self, base_url="http://127.0.0.1:8001"):
        self.base_url = base_url

    def call_api(self, topic):
        url = f"{self.base_url}/info/{topic}"
        response = requests.get(url)
        return response.json()