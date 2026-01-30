# YouTube Content Generator – Backend

An **AI-powered backend** for helping YouTube creators generate **SEO-optimized content**, **AI thumbnails**, and **creator analytics**.  
Built with **FastAPI**, designed for **scalable SaaS**, and ready for real-world deployment.

---

## Features

### Core
- Authentication via **Clerk (JWT)**
- Subscription & billing via **Stripe**
- Credit-based usage limits (Free / Pro)
- Async background jobs (Inngest-style)

### AI
- SEO-optimized titles (with scores)
- Video descriptions & tags
- AI thumbnail generation
- Content & thumbnail history

### Analytics
- Trending keyword discovery
- Outlier video detection
- Thumbnail search

### Production Ready
- Dockerized
- Rate limiting & cost guards
- Job retries & failure handling
- Request logging
- Cloud-ready architecture

---

## Tech Stack

| Layer | Technology |
|-----|-----------|
| API | FastAPI (async) |
| Auth | Clerk |
| Billing | Stripe |
| DB | PostgreSQL |
| ORM | SQLAlchemy 2.0 (async) |
| Background Jobs | Inngest-style workers |
| AI | Pluggable (OpenAI / others) |
| Containerization | Docker & Docker Compose |

---

## Project Structure
```
app/
├── main.py
├── core/ # config, db, auth, stripe
├── api/ # HTTP routes
├── models/ # database models
├── schemas/ # request/response schemas
├── services/ # business & AI logic
├── workers/ # background job handlers
├── utils/ # rate limit, scoring, storage
├── middleware/ # logging, guards
└── static/ # generated thumbnails
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/yt_content

CLERK_JWT_ISSUER=https://your-clerk-issuer
CLERK_JWT_AUDIENCE=your-clerk-audience

STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

FREE_MONTHLY_CREDITS=20
PRO_MONTHLY_CREDITS=500

ENABLE_AI_GENERATION=true
```
## Build & start services
```
docker compose build
docker compose up
```

