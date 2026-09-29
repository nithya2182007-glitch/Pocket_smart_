import json
from .recommendation_service import fallback_recommendation

def build_prompt(planner,data):
    return f'''You are PocketSmart AI, a budget-aware recommendation assistant.
Planner: {planner}
Input: {json.dumps(data)}
Return ONLY JSON with summary, allocation, recommendations, total_estimated.
Each recommendation must have category,name,description,estimated_price,platform,search_url.
Respect the budget. Do not claim live inventory or live prices unless supplied.'''

def generate_with_gemini(planner,data,image_bytes=None,image_mime=None):
    from ..config import get_settings
    s=get_settings()
    if s.mock_ai or not s.gemini_api_key: return fallback_recommendation(planner,data)
    try:
        from google import genai
        from google.genai import types
        client=genai.Client(api_key=s.gemini_api_key)
        contents=[build_prompt(planner,data)]
        if image_bytes: contents.append(types.Part.from_bytes(data=image_bytes,mime_type=image_mime or "image/jpeg"))
        r=client.models.generate_content(model=s.gemini_model,contents=contents,config=types.GenerateContentConfig(temperature=.4))
        t=r.text.strip().replace("```json","").replace("```","").strip()
        result=json.loads(t[t.find("{"):t.rfind("}")+1])
        result["source"]="Gemini"
        return result
    except Exception:
        result=fallback_recommendation(planner,data); result["source"]="Fallback (Gemini unavailable)"; return result
