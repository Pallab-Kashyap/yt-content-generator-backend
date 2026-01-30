async def generate_thumbnail_prompt(topic: str, style: str):
    return (
        f"A high-contrast YouTube thumbnail about '{topic}', "
        f"bold text, expressive face, vibrant colors, {style} style, "
        "cinematic lighting, click-worthy composition"
    )


async def generate_image(prompt: str) -> bytes:
    # Placeholder for real image generation
    # Later: OpenAI Images / Stability / Midjourney proxy
    return b"FAKE_IMAGE_BYTES"
