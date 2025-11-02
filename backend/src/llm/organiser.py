from src.llm.gemini_client import client
from flask import jsonify
from src.firebase_client import db
import json

def organise_notes_with_gemini(data):
    model = "gemini-2.5-flash"
    try:
        notes = data.get("notes", [])
        if not notes:
            return {"error": "No notes found in Firebase"}, 404

        formatted_notes = "\n".join(
            f"- {n.get('author', 'User')} ({n.get('color', 'none')}): {n.get('text', '').strip()}"
            for n in notes if n.get("text")
        )

        prompt = (
            "You are an AI idea organiser that groups related sticky notes into categories.\n"
            "For each category, return a JSON object with:\n"
            "category: name of the category,\n"
            "notes: list of note texts in that category,\n"
            "summary: 1 sentence to describe the category.\n"
            "Return valid JSON with the following structure:\n"
            "{ 'categories': [ { 'category': str, 'notes': [str], 'summary': str } ], 'overview': str }\n\n"
            "Here are the sticky notes:\n"
            f"{formatted_notes}"
        )

        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        raw_text = response.text.strip()

        cleaned = raw_text.replace("```json", "").replace("```", "").strip()
        try:
            result = json.loads(cleaned)
        except json.JSONDecodeError:
            result = {"raw_response": cleaned}

        db.collection("organised_results").add(result)

        return result

    except Exception as e:
        return {"error": f"Gemini processing failed: {e}"}, 500


    return output