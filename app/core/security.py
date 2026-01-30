from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt
import requests

from app.core.config import settings

security = HTTPBearer()
JWKS_URL = f"{settings.CLERK_JWT_ISSUER}/.well-known/jwks.json"
_jwks = requests.get(JWKS_URL).json()


def get_current_user_id(token=Depends(security)) -> str:
    try:
        payload = jwt.decode(
            token.credentials,
            _jwks,
            algorithms=["RS256"],
            audience=settings.CLERK_JWT_AUDIENCE,
            issuer=settings.CLERK_JWT_ISSUER,
        )
        return payload["sub"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )
