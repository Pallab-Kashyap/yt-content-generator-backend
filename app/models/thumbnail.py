from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Thumbnail(Base):
    __tablename__ = "thumbnails"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    topic: Mapped[str] = mapped_column(String, index=True)
    prompt: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String)

    user = relationship("User")
