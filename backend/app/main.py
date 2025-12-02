from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
from app.core.database import Base, engine
from app.core.config import settings
from app.core.firebase_utils import firebase_creds_path
from app.api import user_router, property_router

cred = credentials.Certificate(firebase_creds_path)
firebase_admin.initialize_app(cred)
app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aegis-realty.vercel.app",
                   "http://localhost:5173",
                   "http://localhost:3000"
                   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(property_router, prefix="/api")
app.include_router(user_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}!"}
