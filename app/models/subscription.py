from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    stripe_customer_id: Mapped[str | None] = mapped_column(String, nullable=True)
    stripe_subscription_id: Mapped[str | None] = mapped_column(String, nullable=True)

    plan: Mapped[str] = mapped_column(String, default="free")
    status: Mapped[str] = mapped_column(String, default="active")

    user = relationship("User", back_populates="subscription")
