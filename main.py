from fastapi_users import FastAPIUsers

from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

import crud
from auth.auth import auth_backend
from auth.database import User, get_async_session
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

app = FastAPI()

templates = Jinja2Templates(directory='templates')

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix='/auth',
    tags=['/auth']
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"


@app.get('/is-verified')
def if_user_verified(user: User = Depends(current_user)):
    return 'You are verified ;)' if user.is_verified is True else 'You are not verified :('


@app.get('/', response_class=HTMLResponse)
def main(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse('index.html', {'request': request, 'user': user})
