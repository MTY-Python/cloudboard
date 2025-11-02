import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def add_notes(author, color, text, guest_id, board="default_board"):
    note_ref = db.collection("notes").document()
    note = {
        "author": author,
        "color": color,
        "text": text,
        "guest_id": guest_id,
        "board": board,
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

def edit_node(note_id, new_text):
    note_ref = db.collection("notes").document(note_id)
    note_ref.update({
        "text": new_text,
        "updated_at": SERVER_TIMESTAMP
    })
    return True

