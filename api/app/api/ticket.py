from fastapi import APIRouter, HTTPException, Depends
from app.schemas.schema import TicketCreate, TicketResponse
from app.dependencies.ticket import get_controllers
from fastapi_pagination import Page
from app.controllers.ticket import TicketController


router = APIRouter()

@router.get("/get_all_tickets", response_model=Page[TicketResponse])
def get_all_tickets(controller: TicketController = Depends(get_controllers)):
    return controller.get_all_tickets()
