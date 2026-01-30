from collections import Counter


COMMON_KEYWORDS = [
    "how to",
    "best",
    "why",
    "top",
    "ai",
    "youtube",
    "growth",
    "2025",
]


async def get_trending_keywords(topics: list[str]) -> list[dict]:
    counter = Counter()

    for topic in topics:
        words = topic.lower().split()
        for w in words:
            if len(w) > 3:
                counter[w] += 1

    for k in COMMON_KEYWORDS:
        counter[k] += 2

    trends = counter.most_common(10)

    return [
        {"keyword": k, "score": v * 10}
        for k, v in trends
    ]
