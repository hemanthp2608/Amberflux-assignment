# Amberflux Assignment API (FastAPI)

## Quickstart
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # then edit SECRET_KEY if needed
uvicorn app.main:app --reload
```

### Auth
- Register: `POST /api/auth/register` (json: email, name, password)
- Login: `POST /api/auth/login` (form fields: username=email, password=password) -> returns `access_token`

Use the Bearer token for the protected routes below.

### Assignments
- Create: `POST /api/assignments` (json: title, description, due_date) [auth required]
- List: `GET /api/assignments` [auth required]

### Submissions
- Create: `POST /api/submissions` (form-data: assignment_id, upload=<file>, comment?) [auth required]
- List by assignment: `GET /api/submissions/by-assignment/{assignment_id}` [auth required]
