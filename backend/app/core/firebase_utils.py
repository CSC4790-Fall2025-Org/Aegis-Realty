import os
from .config import settings

if os.path.exists("/etc/secrets/firebase-adminsdk.json"):
    firebase_creds_path = "/etc/secrets/firebase-adminsdk.json"
else:
    firebase_creds_path = settings.FIREBASE_CREDENTIALS