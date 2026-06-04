
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Category(str, Enum):
    LANDING = "landing"
    SITE = "site"
    INTERENTSHOP = "internetshop"
    TGBOT = "tgbot"
    REWORK = "rework"
    UNDECIDED = "undecided"

class ticket(SQLModel, table=True):
  id_ticket: int = Field(primary_key=True)
  name: str
  email: str = Field(nullable=True)
  phone: str
  telegram: str = Field(nullable=True)
  category: Category
  description: str
  created_at: datetime = Field(default_factory=datetime.now)