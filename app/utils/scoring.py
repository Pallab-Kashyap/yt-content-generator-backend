import math


def seo_score(title: str) -> int:
    length_score = max(0, 100 - abs(len(title) - 60))
    keyword_bonus = 10 if ":" in title or "|" in title else 0
    power_words = ["best", "how", "why", "top", "ultimate"]
    power_bonus = sum(5 for w in power_words if w.lower() in title.lower())

    score = length_score + keyword_bonus + power_bonus
    return min(100, max(0, score))
