from fastapi import HTTPException

MAX_TOKENS_PER_REQUEST = 4000
MAX_IMAGES_PER_DAY = 50


def enforce_token_limit(prompt: str):
    approx_tokens = len(prompt) // 4
    if approx_tokens > MAX_TOKENS_PER_REQUEST:
        raise HTTPException(
            status_code=400,
            detail="Prompt too large",
        )


def enforce_image_limit(images_today: int):
    if images_today >= MAX_IMAGES_PER_DAY:
        raise HTTPException(
            status_code=403,
            detail="Daily image limit reached",
        )
