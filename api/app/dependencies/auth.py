from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    """Проверяет API-ключ в заголовке X-API-Key"""
    if not api_key or api_key != settings.API_SECRET_KEY:
        raise HTTPException(
            status_code=401, 
            detail="Неверный или отсутствующий API-ключ"
        )
    return api_key