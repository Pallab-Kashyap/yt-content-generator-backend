from fastapi import APIRouter, Request, HTTPException
import stripe

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.subscription import Subscription

router = APIRouter(prefix="/billing", tags=["Billing"])

stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Stripe event")

    if event["type"] == "customer.subscription.updated":
        sub = event["data"]["object"]

        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Subscription).where(
                    Subscription.stripe_subscription_id == sub["id"]
                )
            )
            subscription = result.scalar_one_or_none()

            if subscription:
                subscription.status = sub["status"]
                subscription.plan = "pro" if sub["status"] == "active" else "free"
                await db.commit()

    return {"ok": True}
