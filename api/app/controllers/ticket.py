from app.models.model import ticket as TicketModel
from sqlalchemy import select, delete
from fastapi_pagination.ext.sqlalchemy import paginate
from app.schemas.schema import TicketCreate, TicketResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session



class TicketController:
    def __init__(self, db: Session):
        self.db = db

    def get_all_tickets(self):
        query = select(TicketModel).order_by(TicketModel.id_ticket)
        return paginate(self.db, query)
    
    def create_ticket(self, ticket_data: TicketCreate):
            
        new_ticket = TicketModel(
            name=ticket_data.name,
            email=ticket_data.email,
            phone=ticket_data.phone,
            telegram=ticket_data.telegram,
            category=ticket_data.category
        )
        self.db.add(new_ticket)
        self.db.commit()
        return new_ticket