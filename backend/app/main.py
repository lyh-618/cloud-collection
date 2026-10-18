from fastapi import FastAPI, HTTPException, Query
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


class Content(BaseModel):
    id: int
    type: str
    title: str
    description: str
    cover_url: str
    external_url: str | None = None
    author: str
    tags: list[str]
    like_count: int
    favorite_count: int
    view_count: int


RECOMMENDATIONS = [
    Recommendation(id=1, category="影视入坑", title="从一部剧认识她", subtitle="角色塑造 · 氛围感", description="适合第一次了解鞠婧祎的你：从角色、造型和情绪表达，慢慢发现她的独特气质。", accent="01"),
    Recommendation(id=2, category="舞台安利", title="看见舞台上的光", subtitle="舞台表现 · 音乐现场", description="把镜头交给舞台，感受轻盈的动作、稳定的状态和属于她的闪光时刻。", accent="02"),
    Recommendation(id=3, category="作品收藏", title="建立你的作品清单", subtitle="影视作品 · 个人偏好", description="收藏喜欢的角色与片段，记录每一次心动，也欢迎写下你自己的推荐理由。", accent="03"),
]


CONTENTS = [
    Content(id=1, type="film", title="影视作品精选", description="从角色、造型和情绪表达开始，认识她在镜头里的不同侧面。", cover_url="/assets/portrait-film.jpg", author="收藏馆编辑部", tags=["影视", "角色", "入坑推荐"], like_count=128, favorite_count=96, view_count=860),
    Content(id=2, type="film", title="值得回看的角色片段", description="整理适合新朋友入坑的角色观察笔记，欢迎写下你的第一印象。", cover_url="/assets/hero-collage.jpg", author="蓝色放映室", tags=["影视", "片段", "安利"], like_count=96, favorite_count=72, view_count=510),
    Content(id=3, type="dance", title="舞台上的高光时刻", description="记录舞台动作、音乐和灯光交汇的瞬间，感受现场表现力。", cover_url="/assets/hero-collage.jpg", author="舞台观察员", tags=["舞蹈", "舞台", "现场"], like_count=156, favorite_count=110, view_count=1030),
    Content(id=4, type="image", title="蓝色胶片视觉手记", description="用一组蓝色调画面，收藏那些安静又有力量的瞬间。", cover_url="/assets/portrait-film.jpg", author="BCXG", tags=["图片", "胶片", "视觉"], like_count=210, favorite_count=188, view_count=1400),
    Content(id=5, type="song", title="单曲循环推荐", description="从旋律开始，记录适合不同心情反复聆听的歌曲和现场。", cover_url="/assets/illustration.png", author="耳机收藏家", tags=["歌曲", "音乐", "循环"], like_count=88, favorite_count=65, view_count=430),
    Content(id=6, type="fanwork", title="给喜欢留一张手写卡片", description="粉丝视角的图文二创示例，欢迎未来发布你的作品和推荐理由。", cover_url="/assets/illustration.png", author="星星邮局", tags=["二创", "图文", "粉丝作品"], like_count=174, favorite_count=132, view_count=920),
]


@app.get("/api/health")
def health_check() -> dict[str, str]:
    """Return a small response used by the frontend and deployment probes."""
    return {"status": "ok", "service": "cloud-collection-api"}


@app.get("/api/recommendations", response_model=list[Recommendation])
def list_recommendations() -> list[Recommendation]:
    """Return editorial recommendation cards for the fan site homepage."""
    return RECOMMENDATIONS


@app.get("/api/contents", response_model=list[Content])
def list_contents(
    content_type: str | None = Query(default=None, alias="type"),
    keyword: str | None = None,
    sort: str = Query(default="latest", pattern="^(latest|popular)$"),
) -> list[Content]:
    """List catalogue content with optional category, keyword and sort filters."""
    results = CONTENTS[:]
    if content_type:
        results = [item for item in results if item.type == content_type]
    if keyword:
        query = keyword.casefold()
        results = [item for item in results if query in f"{item.title} {item.description} {' '.join(item.tags)}".casefold()]
    if sort == "popular":
        results.sort(key=lambda item: (item.like_count, item.view_count), reverse=True)
    else:
        results.sort(key=lambda item: item.id, reverse=True)
    return results


@app.get("/api/contents/{content_id}", response_model=Content)
def get_content(content_id: int) -> Content:
    """Return one content item for the detail page."""
    for item in CONTENTS:
        if item.id == content_id:
            return item
    raise HTTPException(status_code=404, detail="内容不存在")

