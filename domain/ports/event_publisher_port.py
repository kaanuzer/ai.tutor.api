# domain/ports/event_publisher_port.py

class EventPublisherPort:
    """
    Domain içinde gerçekleşen olayları (domain events) dışarıya
    yayınlamak için kullanılan port.
    """
    def publish_event(self, event: object) -> None:
        """
        Herhangi bir domain event nesnesini
        message broker'a veya benzer bir sisteme gönderir.
        """
        raise NotImplementedError