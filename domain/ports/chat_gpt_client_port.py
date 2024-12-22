# domain/ports/chat_gpt_client_port.py

from domain.entities.chat_message import ChatMessage

class ChatGPTClientPort:
    """
    Domain'in, ChatGPT gibi bir dış AI servisiyle etkileşime girmesi
    için gereken arayüz. Domain katmanı bu interface'i bilir ama
    implementasyon detayını bilmez.
    """

    def generate_response(self, user_message: ChatMessage) -> ChatMessage:
        """
        Bir kullanıcı mesajına karşılık, ChatGPT'den yanıt döndürür.
        Domain katmanında, ChatMessage döndürür.
        """
        raise NotImplementedError