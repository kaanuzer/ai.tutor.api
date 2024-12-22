# domain/services/chat_service.py

from domain.entities.chat_message import ChatMessage
from domain.ports.chat_gpt_client_port import ChatGPTClientPort
from domain.ports.event_publisher_port import EventPublisherPort
from domain.events.chat_events import ChatMessageReceived, ChatMessageAnswered

class ChatService:
    """
    Domain servisi: Chat mesajlarının iş mantığını barındırır.
    """

    def __init__(
        self, 
        chat_gpt_client: ChatGPTClientPort, 
        event_publisher: EventPublisherPort
    ):
        self.chat_gpt_client = chat_gpt_client
        self.event_publisher = event_publisher

    def handle_incoming_message(self, incoming_message: ChatMessage):
        """
        Kullanıcıdan gelen mesajı domain'de işler.
        """
        # 1. Olayı yayınla (ChatMessageReceived)
        event = ChatMessageReceived(incoming_message)
        self.event_publisher.publish_event(event)

        # 2. ChatGPT'den yanıt al
        response_message = self.chat_gpt_client.generate_response(incoming_message)

        # 3. Yanıt için event yayınla (ChatMessageAnswered)
        answer_event = ChatMessageAnswered(response_message)
        self.event_publisher.publish_event(answer_event)

        return response_message