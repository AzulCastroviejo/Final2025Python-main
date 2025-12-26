"""
Authentication Controller Module

This module provides the API endpoints for user registration and login.
It handles creating new users and issuing JWT access tokens.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.auth_schema import UserCreate, Token
from schemas.client_schema import ClientSchema
from services import auth_service
from models.client import ClientModel
from models.enums import UserRole
from config.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

ADMIN_EMAIL = "azulcastroviejo@gmail.com"

@router.post("/register", response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    - Hashes the password before storing.
    - Checks for existing user with the same email.
    - Assigns ADMIN role if the email matches the admin email.
    """
    db_user = auth_service.get_user(db, email=user_create.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    hashed_password = auth_service.get_password_hash(user_create.password)
    
       # Assign role based on email
    user_role = UserRole.ADMIN if user_create.email.lower() == ADMIN_EMAIL else UserRole.USER
    
    # Create the new user model
    new_user = ClientModel(
        email=user_create.email,
        hashed_password=hashed_password,
        name=user_create.name,
        lastname=user_create.lastname,
        role=user_role 
        )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Log in a user and return a JWT access token.

    - Authenticates the user with email and password.
    - Returns an access token on success.
    """
    user = auth_service.get_user(db, email=form_data.username) # OAuth2 form uses 'username' for the email
    
    if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "role": str(user.role.value)}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
