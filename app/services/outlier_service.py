def detect_outlier(
    views: int,
    avg_channel_views: int,
    title: str,
):
    if avg_channel_views == 0:
        return {
            "is_outlier": False,
            "performance_ratio": 0,
            "explanation": "Not enough data",
        }

    ratio = views / avg_channel_views

    if ratio >= 2.5:
        explanation = (
            f"This video performed {ratio:.1f}x better than your average. "
            "Strong indicator of an outlier. Analyze the title and thumbnail."
        )
        return {
            "is_outlier": True,
            "performance_ratio": ratio,
            "explanation": explanation,
        }

    return {
        "is_outlier": False,
        "performance_ratio": ratio,
        "explanation": "Performance is within normal range.",
    }
