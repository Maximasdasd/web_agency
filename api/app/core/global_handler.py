from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from json import JSONDecodeError
from fastapi.exceptions import RequestValidationError 
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import psycopg2


def validation_exception_handler(_: Request, exc: RequestValidationError):
    """Простой обработчик ошибок валидации"""
    for exception in exc.errors():
        print(exception)
        if exception['type'] == 'string_too_short' or exception['type'] == 'string_too_long':
            return JSONResponse(
                status_code=422,
                content={
                    "success": False,
                    "error": {
                        "message": f"Некорректный JSON: проверьте синтаксис (кавычки, скобки, запятые)",
                        "type": "validation_error",
                        "status_code": 422
                    }
                }
            )
        elif exception['type'] == 'json_invalid':
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": {
                        "message": f"Ошибка декодирования json",
                        "type": "json_invalid",
                        "status_code": 400
                    }
                }
            )
        else:
                return JSONResponse(
                status_code=422,
                content={
                    "success": False,
                    "error": {
                        "message": f"Ошибка валидации данных в поле {exception} возможно неправильный тип",
                        "type": "validation_error",
                        "status_code": 422
                    }
                }
            )


def integrity_error_handler(_: Request, exc: IntegrityError) -> JSONResponse:
    """
    СИНХРОННЫЙ обработчик IntegrityError
    """
    
    # проверяем оригинальную ошибку PostgreSQL
    if exc.orig and isinstance(exc.orig, psycopg2.errors.UniqueViolation):
        error_msg = str(exc.orig)
        
        # проверяем конкретные constrain
        if error_msg:
            detail = "Нарушение данных"
            status_code = 422
    
    elif exc.orig and isinstance(exc.orig, psycopg2.errors.NotNullViolation):
        detail = "Обязательное поле не заполнено"
        status_code = 422
    
    elif exc.orig and isinstance(exc.orig, psycopg2.errors.ForeignKeyViolation):
        detail = "Ссылка на несуществующий объект"
        status_code = 400
    
    else:
        detail = "Ошибка целостности данных"
        status_code = 422
    
    return JSONResponse(
        status_code=status_code,
        content={"error": f"{detail} ||||| {exc}"} # добавляем оригинальную ошибку PostgreSQL ТОЛЬКО ВО ВРЕМЯ РАЗРАБОТКИ
        )


def sqlalchemy_error_handler(_: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    СИНХРОННЫЙ обработчик SQLAlchemyError
    
    """
    

    detail = "Ошибка базы данных"
    
    return JSONResponse(
        status_code=503,
        content={"error": detail + ' ' + str(exc)}
    )



def http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    СИНХРОННЫЙ обработчик HTTP исключений
    

    """
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )



def global_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    СИНХРОННЫЙ обработчик всех необработанных исключений
    
    """
    
    # определяем детали ошибки в зависимости от среды
    detail = "Внутренняя ошибка сервера"
    
    return JSONResponse(
        status_code=500,
        content={"error": detail})