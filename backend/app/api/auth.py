from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import auth as firebase_auth

router = APIRouter()

class TokenPayload(BaseModel):
    idToken: str

@router.post("/session")
async def create_session(payload: TokenPayload):
    try:
        decoded = firebase_auth.verify_id_token(payload.idToken)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid ID token: {e}")

    # Here you would create or fetch a user in your database and create a server session
    uid = decoded.get('uid')
    return {"status": "success", "uid": uid, "claims": decoded}
