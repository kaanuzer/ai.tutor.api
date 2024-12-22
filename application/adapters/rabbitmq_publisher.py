# rabbitmq_publisher.py
import json
import dataclasses
import pika
from domain.ports.event_publisher_port import EventPublisherPort
from datetime import datetime

class RabbitMQPublisherAdapter(EventPublisherPort):
    def __init__(self, connection_params: pika.ConnectionParameters, exchange: str = '', routing_key: str = 'chat_events'):
        self.connection_params = connection_params
        self.exchange = exchange
        self.routing_key = routing_key

    def publish_event(self, event: object) -> None:
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()

        # 1) Tüm attribute'leri yakala
        event_type = event.__class__.__name__
        payload_dict = {}

        for key, value in event.__dict__.items():
            # Eğer value bir dataclass ise asdict(...) yapalım
            if dataclasses.is_dataclass(value):
                # asdict sonrası datetime'ları stringe çevirelim
                payload_dict[key] = self._asdict_with_datetime(value)
            else:
                payload_dict[key] = value

        message_dict = {
            "event_type": event_type,
            "payload": payload_dict
        }

        # 2) JSON'a çevir
        body = json.dumps(message_dict)
        channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=body)
        connection.close()

    def _asdict_with_datetime(self, obj):
        """
        Dataclass nesnesini dict'e dönüştürürken,
        datetime alanlarını isoformat string'e çeviren yardımcı fonksiyon.
        """
        result = dataclasses.asdict(obj)
        for k, v in result.items():
            if isinstance(v, datetime):
                result[k] = v.isoformat()  # "2024-12-21T15:30:00.123456" gibi
        return result