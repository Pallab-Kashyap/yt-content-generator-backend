from fastapi import FastAPI
from app.api.routes import user, billing, content
from app.api.routes import jobs
from app.workers import inngest_handler
from app.api.routes import thumbnails
from app.api.routes import analytics
from app.middleware.logging import logging_middleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="YouTube Content Generator API")

app.include_router(user.router)
app.include_router(billing.router)


@app.get("/health")
async def health():
    return {"status": "ok"}

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(content.router)
app.include_router(jobs.router)
app.include_router(inngest_handler.router)
app.include_router(thumbnails.router)
app.include_router(analytics.router)
app.middleware("http")(logging_middleware)



