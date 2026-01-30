from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import get_current_user_id
from app.core.database import get_db
from app.models.user import User
from app.models.subscription import Subscription
from app.models.usage import Usage


async def get_current_user(
    user_id: str = get_current_user_id,
    db: AsyncSession = get_db,
) -> User:
    result = await db.execute(
        select(User).where(User.clerk_user_id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        user = User(clerk_user_id=user_id)
        db.add(user)
        await db.flush()

        db.add(Subscription(user_id=user.id))
        db.add(Usage(user_id=user.id))
        await db.commit()

    return user
