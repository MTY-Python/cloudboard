import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from dotenv import dotenv_values

config = dotenv_values(".env")

private_key_id = config.get("FIREBASE_PRIVATE_KEY_ID", "")
private_key = config.get("FIREBASE_PRIVATE_KEY", "")

account_key = {
  "type": "service_account",
  "project_id": "cloudboard-581de",
  "private_key_id": private_key_id,
  "private_key": private_key,
  "client_email": "firebase-adminsdk-fbsvc@cloudboard-581de.iam.gserviceaccount.com",
  "client_id": "103127509436913410442",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40cloudboard-581de.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


cred = credentials.Certificate(account_key)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def add_notes(author, color, text, guest_id, board="default_board", x=0, y=0):
    note_ref = db.collection("notes").document()
    note = {
        "author": author,
        "color": color,
        "text": text,
        "guest_id": guest_id,
        "board": board,
        "x": x,
        "y": y,
        "created_at": SERVER_TIMESTAMP,
        "updated_at": SERVER_TIMESTAMP
    }
    note_ref.set(note)
    return note_ref.id

def get_notes(board="default_board"):
    notes_ref = db.collection("notes").where("board", "==", board).order_by("created_at", direction=firestore.Query.DESCENDING)
    docs = notes_ref.stream()
    return [doc.to_dict() for doc in docs]

def delete_note(note_id, board="default_board"):
    notes_ref = db.collection("notes").where("board", "==", board)
    for doc in notes_ref.stream():
        if doc.id == note_id:
            doc.reference.delete()
            return True

    return False

def edit_note(note_id, new_text):
    note_ref = db.collection("notes").document(note_id)
    note_ref.update({
        "text": new_text,
        "updated_at": SERVER_TIMESTAMP
    })
    return True

