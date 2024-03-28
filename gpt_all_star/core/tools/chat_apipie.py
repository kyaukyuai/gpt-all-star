import requests
from langchain_core.language_models.chat_models import BaseChatModel


class ChatAPIpie(BaseChatModel):
    def __init__(self, model_name: str, temperature: float, streaming: bool, api_key: str):
        self.model_name = model_name
        self.temperature = temperature
        self.streaming = streaming
        self.api_key = api_key
        self.api_url = "https://api.apipie.ai/v1/chat/completions"

    def send_request(self, prompt: str):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": self.temperature,
            "stream": self.streaming
        }
        response = requests.post(self.api_url, json=data, headers=headers)
        response.raise_for_status()
        return self.process_response(response.json())

    def process_response(self, response):
        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["text"]
        else:
            raise ValueError("No response from APIpie API")
