from src.llm.gemini_client import client
from src.firebase_client import db
import json

def organise_notes_with_gemini(data):
    model="gemini-2.5-pro"
    try:
        notes = data.get("notes", [])
        if not notes:
            return {"error": "No notes found in firebase"}, 404
        
        result = organise_notes_with_gemini(notes, model)
        db.collection("organised_results").add(result)
        return jsonify({"organised_notes": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    formatted_notes = "\n".join(
        [f"- {n.get('author', 'User')} ({n.get('color', 'none')}): {n.get('text', '').strip()}"
         for n in notes if n.get("text")]
    )

    prompt=(
        "You are an AI idea organiser that groups related sticky notes into categories.\n"
        "For each category, return a JSON object with:\n"
        "category: name of the category,\n"
        "notes: list of note texts in that category,\n"
        "summary: 1 sentence to describe the category.\n"
        "Return valid JSON with the follow structure:\n"
        "{ 'categories': [ { 'category': str, 'notes': [str], 'summary' : str}], 'overview': str}\n\n"
        "Here are the sticky notes: \n"
        f"{formatted_notes}"
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        raw_text = response.text.strip()
    except Exception as e:
        return{"error": f"Gemini API call failed: {e}"}
    
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()
    
    try:
        output = json.loads(cleaned)
    except json.JSONDecodeError:
        output = {"raw_response": cleaned}
    

    return output