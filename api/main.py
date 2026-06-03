from fastapi import FastAPI, APIRouter, Request
from fastapi_pagination import add_pagination

# Импорт роутеров
from app.api.ticket import router as ticket_router

from app.db.db import create_tables, drop_tables



# error
from app.core.global_handler import integrity_error_handler, sqlalchemy_error_handler, http_exception_handler, global_exception_handler, validation_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi.exceptions import RequestValidationError



# Создаем приложение
app = FastAPI(
    title="WEB AGENCY API",
    version="1.0.0",
    description="API для формы заявок агенства",
)


add_pagination(app)
app.include_router(ticket_router, prefix="/ticket",tags=["ticket"])



# error
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/")
def root():
    return {
        "message": "Car Rental API",
        "docs": "/docs",
        "version": "1.0.0",
        "test": "docker"
    }
        


if __name__ == "__main__":
    # drop_tables()
    create_tables()
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
