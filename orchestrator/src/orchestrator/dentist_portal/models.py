"""Pydantic models for Dentist Portal."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class UserRole(str, Enum):
    DENTIST = "dentist"
    PATIENT = "patient"


class ProductCategory(str, Enum):
    TOOTHBRUSH = "toothbrush"
    TOOTHPASTE = "toothpaste"
    MOUTHWASH = "mouthwash"
    FLOSS = "floss"
    WHITENING = "whitening"
    ORTHODONTIC = "orthodontic"
    OTHER = "other"


class ProductStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


# --- Auth Models ---

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    role: UserRole = UserRole.PATIENT
    clinic_name: Optional[str] = None
    license_number: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: UserRole
    user_id: str
    name: str


# --- Product Models ---

class ProductUpload(BaseModel):
    name: str
    category: ProductCategory
    price: float
    raw_description: str
    images: list[str] = []


class ProductOut(BaseModel):
    product_id: str
    name: str
    category: str
    price: float
    ai_description: str
    problems_solved: list[str]
    images: list[str]
    dentist_id: str
    status: str
    view_count: int = 0
    recommendation_count: int = 0
    created_at: datetime


class ProductUpdateRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    raw_description: Optional[str] = None
    status: Optional[ProductStatus] = None


# --- Recommendation Models ---

class RecommendRequest(BaseModel):
    issue: str
    session_id: Optional[str] = None


class RecommendResponse(BaseModel):
    session_id: str
    recommendations: str  # agent final_output (natural language)
