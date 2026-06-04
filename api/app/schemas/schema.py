from pydantic import BaseModel
from app.models.model import Category
from datetime import datetime
from typing import Optional

class TicketCreate(BaseModel):
    name: str
    email: Optional[str]
    phone: str
    telegram: Optional[str]
    category: Category
    description: str

class TicketResponse(TicketCreate):
    id_ticket: int
    created_at: datetime
