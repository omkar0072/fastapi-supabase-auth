# 🔐 Supabase Auth API

A production-ready FastAPI backend with **Supabase authentication**, **JWT verification**, **protected routes**, and **Swagger UI**.

## 📋 Project Description

This project demonstrates a secure REST API built with FastAPI that leverages Supabase for user authentication. It implements JWT verification locally using the Supabase JWT secret, providing fast and reliable token validation without round-trips to Supabase servers.

### Features

- ✅ User signup, login, and logout via Supabase Auth
- ✅ Local JWT verification (HS256) — no external round-trips
- ✅ Reusable authentication dependency for protected routes
- ✅ Swagger UI with Bearer/JWT authorization and lock icons
- ✅ Automatic token validation and error handling (expired, invalid, tampered)
- ✅ Public and protected endpoint separation

## 🛠 Technologies Used

| Technology | Purpose |
|---|---|
| **FastAPI** | High-performance async web framework |
| **Supabase** | Authentication and user management |
| **PyJWT** | JWT decoding and verification |
| **Uvicorn** | ASGI server |
| **Pydantic** | Request/response validation |
| **pytest + httpx** | Automated testing |

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.10+
- A [Supabase](https://supabase.com) account and project
- `pip` or `uv`

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/fastapi-supabase-auth.git
cd fastapi-supabase-auth
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your Supabase credentials:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret
```

**Where to find these values in Supabase:**

| Variable | Location |
|---|---|
| `SUPABASE_URL` | Project Settings → General → Project ID |
| `SUPABASE_ANON_KEY` | Project Settings → API → Project API Keys |
| `SUPABASE_JWT_SECRET` | Project Settings → API → JWT Settings → JWT Secret |

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

## 🚀 How to Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- **API Base:** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 📡 API Endpoint Table

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| POST | `/auth/signup` | ❌ No | Register a new user |
| POST | `/auth/login` | ❌ No | Login and receive access token |
| POST | `/auth/logout` | ❌ No | Sign out the current user |
| GET | `/public/info` | ❌ No | Public information endpoint |
| GET | `/protected/profile` | ✅ Yes | Get authenticated user profile |
| GET | `/protected/dashboard` | ✅ Yes | Get dashboard data for user |

## 🔒 Which Endpoints Require Authentication

Endpoints under `/protected/*` require a valid JWT in the `Authorization` header:

```
Authorization: Bearer <your_access_token>
```

Without a token, the API returns `401 Unauthorized`. With an invalid or modified token, it also returns `401`. With a valid token, it returns `200` and the protected data.

## 📸 Swagger UI

![Swagger UI Screenshot](swagger-screenshot.png)

> **Screenshot instructions:** Run the server, open `http://localhost:8000/docs`, click the **Authorize** button, paste a valid JWT, and take a screenshot showing:
> 1. The “Authorize” button with a lock icon
> 2. Protected routes with lock icons
> 3. The expanded `/protected/profile` endpoint

## 🧪 Proof / Testing

### Manual Testing Flow

| Step | Action | Expected Result |
|---|---|---|
| 1 | `POST /auth/signup` with valid email/password | `201 Created` |
| 2 | `POST /auth/login` with same credentials | `200 OK` + `access_token` |
| 3 | `GET /public/info` (no token) | `200 OK` |
| 4 | `GET /protected/profile` (no token) | `401 Unauthorized` |
| 5 | `GET /protected/profile` (valid token) | `200 OK` |
| 6 | `GET /protected/profile` (modified token) | `401 Unauthorized` |
| 7 | `POST /auth/logout` | `204 No Content` |

### Automated Tests

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_api.py::test_public_route_no_token PASSED
tests/test_api.py::test_protected_route_without_token PASSED
tests/test_api.py::test_invalid_token PASSED
tests/test_api.py::test_signup PASSED
tests/test_api.py::test_login PASSED
tests/test_api.py::test_logout PASSED
```

## 🧠 AI vs Me (Optional Bonus — Stage 7)

### What AI Generated

An AI-generated version of this API might include:

- A single `main.py` with all routes mixed together
- Hardcoded JWT secrets or weak defaults
- No reusable dependency pattern
- No token expiration or audience checks
- Swagger UI without Bearer auth configuration

### Key Differences & Security Issues in AI Output

| Aspect | AI-Generated | This Project |
|---|---|---|
| **JWT verification** | May skip signature verification or use `verify=False` | Full local HS256 verification with audience check |
| **Secret management** | Hardcoded secrets | `.env` + `.gitignore` |
| **Middleware** | Inline token parsing per route | Reusable `get_current_user` dependency |
| **Error handling** | Generic 500 errors | Specific 401 with `WWW-Authenticate` headers |
| **Token expiry** | Often ignored | Explicit `ExpiredSignatureError` handling |
| **Swagger auth** | No Bearer scheme | Custom OpenAPI with Bearer/JWT + lock icons |
| **Structure** | Monolithic file | Modular routers, config, auth separation |

**Critical security issues in typical AI output:**
1. **No signature verification** — allows forged tokens
2. **Hardcoded secrets** — leaked in version control
3. **Missing audience validation** — tokens from other apps accepted
4. **No expiry handling** — expired tokens still work
5. **No `WWW-Authenticate` header** — breaks OAuth compliance

## 📄 License

MIT
