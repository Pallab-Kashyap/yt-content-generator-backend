from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Usage(Base):
    __tablename__ = "usage"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    used_credits: Mapped[int] = mapped_column(Integer, default=0)

    user = relationship("User", back_populates="usage")
