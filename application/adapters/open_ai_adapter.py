# application/adapters/open_ai_adapter.py

import os
import openai
from domain.entities.chat_message import ChatMessage
from domain.ports.chat_gpt_client_port import ChatGPTClientPort

class OpenAIAdapter(ChatGPTClientPort):
    """
    ChatGPT API'siyle konuşan gerçek implementasyon.
    """

    def __init__(self, openai_api_key: str = None):
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY", "")
        openai.api_key = self.api_key

    def generate_response(self, user_message: ChatMessage) -> ChatMessage:
        # OpenAI'nin ChatCompletion vb. endpointini çağırıyoruz (basit örnek)
        if not self.api_key:
            raise ValueError("OpenAI API key is not set.")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello World!"}]
        )

        content = response.choices[0].message["content"]
        ai_message = ChatMessage(
            sender_id="chatgpt",
            content=content,
            is_response=True
        )
        return ai_message