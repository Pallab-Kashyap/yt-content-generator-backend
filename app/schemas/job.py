from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    type: Mapped[str] = mapped_column(String)  # content / thumbnail
    status: Mapped[str] = mapped_column(String, default="PENDING")

    input: Mapped[dict] = mapped_column(JSON)
    output: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error: Mapped[str | None] = mapped_column(String, nullable=True)

    user = relationship("User")
