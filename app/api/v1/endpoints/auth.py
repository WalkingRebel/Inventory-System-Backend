from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.core.database import get_db
from app.core.config import settings
from app.core.oauth import oauth
from app.services.auth_service import handle_oauth_user
from app.services.auth_service import login_user_service

router = APIRouter()


@router.post(
    "/login",
    summary="Log in with email and password",
    description="Validates user credentials and returns a bearer token for protected API access.",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    result = login_user_service(db, form_data.username, form_data.password)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    return result


def _ensure_google_oauth_configured() -> None:
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth is not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.",
        )
    if not hasattr(oauth, "google"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth is not registered. Check GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET.",
        )


@router.get(
    "/logon/google",
    summary="Start Google OAuth login",
    description="Redirects the client to Google so the user can authorize access with their Google account.",
)
async def login_google(request: Request):
    _ensure_google_oauth_configured()
    redirect_uri = request.url_for("auth_google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get(
    "/google/callback",
    summary="Complete Google OAuth callback",
    description="Finishes the Google OAuth flow, creates or fetches the user, and returns a bearer token plus basic user data.",
)
async def auth_google_callback(request: Request, db: Session = Depends(get_db)):
    _ensure_google_oauth_configured()
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.userinfo(token=token)

    user_data = {
        "email": user_info["email"],
        "name": user_info["name"],
        "sub": user_info["sub"],
    }

    user = handle_oauth_user(db, user_data)
    access_token = create_access_token({"sub": user.email, "role": user.role_id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role_id": user.role_id,
        },
    }
