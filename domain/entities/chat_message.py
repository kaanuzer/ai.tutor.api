
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import uuid

@dataclass
class ChatMessage:
    """
    Domain entity: Kullanıcı veya sistem tarafından üretilen mesaj.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = ""
    content: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_response: bool = False