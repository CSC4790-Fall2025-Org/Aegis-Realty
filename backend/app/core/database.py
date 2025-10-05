from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Use a safe in-memory SQLite database when DATABASE_URL is not set. This
# prevents import-time failures during local development or quick static
# checks where a real database isn't available.
db_url = settings.DATABASE_URL or "sqlite:///:memory:"
engine = create_engine(db_url, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
	"""FastAPI dependency that yields a DB session and closes it after use."""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()