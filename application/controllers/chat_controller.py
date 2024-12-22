# application/controllers/chat_controller.py

from fastapi import APIRouter
from domain.usecases.send_chat_message import send_chat_message
from domain.services.chat_service import ChatService

router = APIRouter()

@router.post("/chat/send")
def send_message(sender_id: str, content: str):
    """
    Örnek FastAPI endpoint'i: Bir mesaj alır ve use case'i çağırır.
    """
    # ChatService'i bir DI (Dependency Injection) mekanizmasıyla veya manuel oluşturman gerekebilir
    # Aşağıdaki, ilkel bir örnek (burada her seferinde instance oluşturmuyor varsayalım).
    global_chat_service: ChatService = get_global_chat_service()  # Bu fonksiyon projenize özel olabilir.

    send_chat_message(global_chat_service, sender_id, content)
    return {"status": "Message sent successfully"}

def get_global_chat_service():
    # Burada bir singleton ya da DI Container ile ChatService döndürebilirsiniz.
    # Örnek olarak basit bir dummy instance verelim.
    from application.adapters.open_ai_adapter import OpenAIAdapter
    from application.adapters.rabbitmq_publisher import RabbitMQPublisherAdapter
    import pika

    publisher = RabbitMQPublisherAdapter(
        connection_params=pika.ConnectionParameters(host="localhost"),
        routing_key="chat_events"
    )
    openai_adapter = OpenAIAdapter(openai_api_key="")

    # Tek seferlik instance oluştur
    from domain.services.chat_service import ChatService
    service = ChatService(openai_adapter, publisher)
    return service