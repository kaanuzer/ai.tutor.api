# domain/usecases/send_chat_message.py

from domain.entities.chat_message import ChatMessage
from domain.services.chat_service import ChatService

def send_chat_message(chat_service: ChatService, sender_id: str, content: str):
    """
    Use case: Kullanıcıdan gelen bir mesajı ChatService'e ilet.
    """
    message = ChatMessage(sender_id=sender_id, content=content)
    chat_service.handle_incoming_message(message)