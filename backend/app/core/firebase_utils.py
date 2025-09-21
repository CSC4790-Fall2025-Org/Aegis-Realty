import os

if os.path.exists("/etc/secrets/firebase-adminsdk.json"):
    firebase_creds_path = "/etc/secrets/firebase-adminsdk.json"
else:
    firebase_creds_path = os.getenv("FIREBASE_CREDENTIALS")