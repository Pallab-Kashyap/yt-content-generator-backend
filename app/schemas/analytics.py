from pydantic import BaseModel
from typing import List


class TrendingKeyword(BaseModel):
    keyword: str
    score: int


class OutlierVideoRequest(BaseModel):
    views: int
    avg_channel_views: int
    title: str


class OutlierVideoResponse(BaseModel):
    is_outlier: bool
    performance_ratio: float
    explanation: str
