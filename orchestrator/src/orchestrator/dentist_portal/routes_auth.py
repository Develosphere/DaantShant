"""Auth routes for Dentist Portal."""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from orchestrator.dentist_portal.auth import create_token, hash_password, verify_password
from orchestrator.dentist_portal.db import get_portal_users_col
from orchestrator.dentist_portal.models import LoginRequest, RegisterRequest, TokenResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/portal/auth", tags=["portal-auth"])


@router.post("/register", response_model=TokenResponse)
async def register(req: RegisterRequest):
    users = get_portal_users_col()
    existing = await users.find_one({"email": req.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(req.password)
    doc = {
        "email": req.email,
        "hashed_password": hashed,
        "name": req.name,
        "role": req.role,
        "clinic_name": req.clinic_name,
        "license_number": req.license_number,
        "created_at": datetime.now(timezone.utc),
        "is_verified": False,
    }
    result = await users.insert_one(doc)
    user_id = str(result.inserted_id)
    token = create_token(user_id, req.email, req.role)

    logger.info("[PORTAL AUTH] Registered user %s as %s", req.email, req.role)
    return TokenResponse(access_token=token, role=req.role, user_id=user_id, name=req.name)


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    users = get_portal_users_col()
    user = await users.find_one({"email": req.email})
    if not user or not verify_password(req.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_id = str(user["_id"])
    token = create_token(user_id, user["email"], user["role"])

    logger.info("[PORTAL AUTH] Login: %s", req.email)
    return TokenResponse(
        access_token=token,
        role=user["role"],
        user_id=user_id,
        name=user["name"],
    )
