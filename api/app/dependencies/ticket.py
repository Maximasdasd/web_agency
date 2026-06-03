from app.db.db import get_db
from fastapi import Depends
from app.controllers.ticket import TicketController
from sqlalchemy.orm import Session

def get_controllers(db: Session = Depends(get_db)) -> TicketController:
    return TicketController(db)
