# domain/events/chat_events.py

from domain.entities.chat_message import ChatMessage

class ChatMessageReceived:
    """
    Kullanıcıdan (veya herhangi bir kaynaktan) gelen yeni mesaj olayı.
    """
    def __init__(self, message: ChatMessage):
        self.message = message

class ChatMessageAnswered:
    """
    ChatGPT ya da başka bir yapay zeka tarafından verilen yanıt olayı.
    """
    def __init__(self, message: ChatMessage):
        self.message = message