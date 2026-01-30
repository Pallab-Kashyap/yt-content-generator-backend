from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    clerk_user_id: Mapped[str] = mapped_column(String, unique=True, index=True)

    subscription = relationship("Subscription", back_populates="user", uselist=False)
    usage = relationship("Usage", back_populates="user", uselist=False)
