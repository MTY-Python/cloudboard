from flask import Flask, jsonify, request
from flask_cors import CORS
from src.llm.organiser import organise_notes_with_gemini
from src.firebase_client import add_notes, get_notes, delete_note
from dotenv import load_dotenv
from google import genai
import os
import json 

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to the CloudBoard Backend!"})
    
    @app.route("/notes", methods=["GET", "POST", "DELETE"])
    def notes():
        if request.method == "POST":
            data = request.get_json()
            author = data.get("author", "Anonymous")
            color = data.get("color", "white")
            text = data.get("text", "")
            board = data.get("board", "default_board")
            note_id = add_notes(author, color, text, board)
            return jsonify({"message": "Note added", "note_id": note_id}), 201
        
        elif request.method == "GET":
            board = request.args.get("board", "default_board")
            notes = get_notes(board)
            return jsonify({"notes": notes}), 200
        
        elif request.method == "DELETE":
            data = request.get_json()
            note_id = data.get("note_id")
            board = data.get("board", "default_board")
            if not note_id:
                return jsonify({"error": "note_id is required"}), 400
            success = delete_note(note_id, board)
            if success:
                return jsonify({"message": "Note deleted"}), 200
            else:
                return jsonify({"error": "Note not found"}), 404
            

        

    @app.route("/organise-firebase", methods=["GET"])
    def organise_firebase_notes():
        try:
            notes = get_notes()
            if not notes:
                return jsonify({"error": "No notes found in Firebase"}), 404
            
            result = organise_notes_with_gemini({"notes": notes})
            return jsonify({"organised_notes": result})
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/organise", methods=["POST"])
    def organise_notes():   
        try:
            data = request.get_json()
            if isinstance(data, list):
                notes = data
            else:
              notes = data.get("notes", [])
            if not notes:
                return jsonify({"error": "No notes provided"}), 400
            
            result = organise_notes_with_gemini({"notes": notes})
            return jsonify({"organised_notes": result})
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route("/test-gemini")
    def test_organise():
        test_data = {
             "notes": [
        {"author": "Yusuf", "color": "yellow", "text": "Ferrari"},
        {"author": "Tom", "color": "brown", "text": "Hilton"},
        {"author": "Monty", "color": "black", "text": "Marriot"}
                ]
        }
        
        result = organise_notes_with_gemini(test_data)
        raw = result.get("raw_response") or result
        if isinstance(raw, str):
            raw = raw.replace("```json", "").replace("```", "").replace("\\n", "\n").strip()
            try:
                raw = json.loads(raw)
            except json.JSONDecodeError:
                pass

        formatted_output = json.dumps(result, indent=4, ensure_ascii=False)

        return f"""
        <html>
            <head>
            <title>Cloudboard backend test</title>
            <style>
                body {{
                background:#0b0b0b;
                color:#eee;
                font-family:Consolas, monospace;
                margin:2em;
                }}
                h1, h2 {{ color:#065535; }}
                pre {{
                background:#1a1a1a;
                padding:1em;
                border-radius:8px;
                overflow-x:auto;
                white-space:pre-wrap;
                }}
                .box {{
                margin-bottom:2em;
                }}
            </style>
            </head>
            <body>
            <h1>cloudboard test</h1>

            <div class="box">
                <h2>Input Notes</h2>
                <pre>{json.dumps(test_data, indent=4)}</pre>
            </div>

            <div class="box">
                <h2>AI Output</h2>
                <pre>{formatted_output}</pre>
            </div>
            </body>
        </html>
        """

            

    return app

