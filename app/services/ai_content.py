from app.utils.scoring import seo_score

# TEMP: mock AI logic
# In Phase 3/4 we'll replace with real LLM calls

async def generate_content(topic: str):
    raw_titles = [
        f"How to grow on YouTube with {topic}",
        f"The ultimate guide to {topic}",
        f"{topic}: Everything you need to know",
        f"Why {topic} is changing YouTube forever",
    ]

    titles = [
        {"text": t, "seo_score": seo_score(t)}
        for t in raw_titles
    ]

    description = (
        f"In this video, we explore {topic} and explain how it can help "
        "you grow faster on YouTube. Learn actionable strategies, tips, "
        "and mistakes to avoid."
    )

    tags = [
        topic,
        "youtube growth",
        "content creator",
        "youtube tips",
    ]

    return {
        "titles": titles,
        "description": description,
        "tags": tags,
        "prompt_version": "v1",
    }
