import uuid
from pathlib import Path

BASE_PATH = Path("static/thumbnails")
BASE_PATH.mkdir(parents=True, exist_ok=True)


async def save_image(data: bytes) -> str:
    filename = f"{uuid.uuid4()}.png"
    path = BASE_PATH / filename

    with open(path, "wb") as f:
        f.write(data)

    return f"/static/thumbnails/{filename}"
