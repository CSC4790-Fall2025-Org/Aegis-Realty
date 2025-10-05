from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
from app.core.database import Base, engine
from app.core.config import settings
from app.core.firebase_utils import firebase_creds_path
from app.api.property import router as property_router
from app.api.user import router as user_router

import os
app = FastAPI(title=settings.PROJECT_NAME)

# Initialize Firebase only when credentials file is present. This allows the
# app to be imported in environments (like CI or local static checks) where
# Firebase credentials are not available.
if firebase_creds_path and os.path.exists(firebase_creds_path):
    cred = credentials.Certificate(firebase_creds_path)
    firebase_admin.initialize_app(cred)
else:
    # Defer initialization; routes that require Firebase auth should handle
    # absence of the admin SDK or missing credentials via the dependency layer.
    print("Firebase credentials not found; skipping firebase_admin initialization")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(property_router, prefix="/api")
app.include_router(user_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}!"}
