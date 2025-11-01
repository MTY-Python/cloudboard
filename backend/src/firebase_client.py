import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def add_notes(author, color, text, board="default_board"):
    note_ref = db.collection("notes").document()
    note = {
        "author": author,
        "color": color,
        "text": text
    }
    note_ref.set(note)
    return note_ref.id

def get_notes(board="default_board"):
    notes_ref = db.collection("notes")
    docs = notes_ref.stream()
    notes = []
    for doc in docs:
        notes.append(doc.to_dict())
    return notes

def delete_note(note_id, board="default_board"):
    notes_ref = db.collection("notes").where("board", "==", board)
    for doc in notes_ref.stream():
        if doc.id == note_id:
            doc.reference.delete()
            return True

    return False


