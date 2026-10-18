from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Cloud Collection API",
    description="云端收藏馆后端 API",
    version="0.1.0",
)


class Recommendation(BaseModel):
    id: int
    category: str
    title: str
    subtitle: str
    description: str
    accent: str


RECOMMENDATIONS = [
    Recommendation(id=1, category="影视入坑", title="从一部剧认识她", subtitle="角色塑造 · 氛围感", description="适合第一次了解鞠婧祎的你：从角色、造型和情绪表达，慢慢发现她的独特气质。", accent="01"),
    Recommendation(id=2, category="舞台安利", title="看见舞台上的光", subtitle="舞台表现 · 音乐现场", description="把镜头交给舞台，感受轻盈的动作、稳定的状态和属于她的闪光时刻。", accent="02"),
    Recommendation(id=3, category="作品收藏", title="建立你的作品清单", subtitle="影视作品 · 个人偏好", description="收藏喜欢的角色与片段，记录每一次心动，也欢迎写下你自己的推荐理由。", accent="03"),
]


@app.get("/api/health")
def health_check() -> dict[str, str]:
    """Return a small response used by the frontend and deployment probes."""
    return {"status": "ok", "service": "cloud-collection-api"}


@app.get("/api/recommendations", response_model=list[Recommendation])
def list_recommendations() -> list[Recommendation]:
    """Return editorial recommendation cards for the fan site homepage."""
    return RECOMMENDATIONS

