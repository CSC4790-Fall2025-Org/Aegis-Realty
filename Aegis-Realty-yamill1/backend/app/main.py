from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
from app.core.database import Base, engine
from app.core.config import settings
from app.core.firebase_utils import firebase_creds_path
from app.api.property import router as property_router
from app.api.user import router as user_router

cred = credentials.Certificate(firebase_creds_path)
firebase_admin.initialize_app(cred)
app = FastAPI(title=settings.PROJECT_NAME)

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
