# PocketSmart AI — Complete Project

FastAPI + Jinja2 + Gemini-ready budget recommendation assistant for Home, Party, Jewelry, Travel, Meal and Shopping planning.

## Run in VS Code
1. Open this folder.
2. `py -m venv .venv` (Windows) or `python3 -m venv .venv`.
3. Activate: `.venv\\Scripts\\activate` (Windows) or `source .venv/bin/activate`.
4. `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`.
6. First run: keep `MOCK_AI=true`.
7. `uvicorn app.main:app --reload`
8. Open http://127.0.0.1:8000

## Gemini
Set `GEMINI_API_KEY`, set `MOCK_AI=false`, and choose the model in `GEMINI_MODEL`.
The project document specifies Gemini 1.5 Flash Pro; the model is configurable because model availability can change.
Never commit `.env`.

## Test
`pytest -q`

## API
POST `/register`, `/login`, `/logout`, `/token`
GET `/session-info`, `/session-data`, `/history`, `/health`, `/startup`
POST `/generate-home`, `/generate-party`, `/generate-jewelry`, `/generate-travel`, `/generate-meal`, `/generate-shopping`
GET `/recommendations-details/{id}`

External platforms named in the project documentation are represented by platform search links. No website scraping is performed.
