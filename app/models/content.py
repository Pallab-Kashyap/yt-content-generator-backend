from sqlalchemy import String, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class GeneratedContent(Base):
    __tablename__ = "generated_content"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    topic: Mapped[str] = mapped_column(String, index=True)

    titles: Mapped[list] = mapped_column(JSON)
    description: Mapped[str] = mapped_column(Text)
    tags: Mapped[list] = mapped_column(JSON)

    prompt_version: Mapped[str] = mapped_column(String, default="v1")

    user = relationship("User")
