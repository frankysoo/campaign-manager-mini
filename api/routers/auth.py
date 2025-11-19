from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from common.auth import authenticate_user, create_access_token, User, get_admin_user
from common.auth import fake_users_db, get_current_active_user, create_token_for_user
from common.metrics import events_received_total

router = APIRouter(tags=["authentication"])

@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

@router.get("/admin/")
async def admin_route(current_user: User = Depends(get_admin_user)):
    return {"message": "You are an admin!"}

@router.post("/test-token/{username}", response_model=dict)
async def test_create_token(username: str, current_user: User = Depends(get_admin_user)):
    """Admin endpoint to create test tokens"""
    return create_token_for_user(username)
