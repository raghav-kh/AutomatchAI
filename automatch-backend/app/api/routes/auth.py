from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import secrets

from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.crud import user as user_crud
from app.schemas.auth import UserRegister, UserOut, Token
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """
    Creates an admin account. Requires ADMIN_SETUP_KEY (set via env var) --
    there's no public sign-up here, this is an internal tool. Anyone with
    the setup key can create additional admin accounts.
    """
    if not secrets.compare_digest(payload.setup_key, settings.admin_setup_key):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid setup key")

    if user_crud.get_user_by_username(db, payload.username):
        raise HTTPException(status_code=409, detail="Username already taken")

    return user_crud.create_user(db, payload.username, payload.password)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=user.username)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
