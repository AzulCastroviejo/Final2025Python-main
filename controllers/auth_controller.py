from fastapi import APIRouter, Depends, HTTPException, status
from schemas.client_schema import ClientLoginSchema
from services.client_service import ClientService
from config.database import get_db

router = APIRouter(tags=["Auth"])

@router.post("/login")
def login(data: ClientLoginSchema, db = Depends(get_db)):
    service = ClientService(db)
    user = service.login(data.email, data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return {"message": "Login successful", "client": user}