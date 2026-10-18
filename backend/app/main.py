from datetime import datetime, timedelta, timezone
import base64
import hashlib
import hmac
import json
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Cloud Collection API", description="云端收藏馆后端 API", version="0.2.0")
bearer = HTTPBearer(auto_error=False)
TOKEN_SECRET = b"cloud-collection-local-demo-secret"


class Recommendation(BaseModel):
    id: int
    category: str
    title: str
    subtitle: str
    description: str
    accent: str


class User(BaseModel):
    id: int
    username: str
    password_hash: str
    is_admin: bool = False


class RegisterInput(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)
    confirm_password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not value.strip() or any(ch.isspace() for ch in value):
            raise ValueError("用户名不能包含空格")
        return value.strip()

    def check_passwords(self) -> None:
        if self.password != self.confirm_password:
            raise ValueError("两次密码不一致")


class LoginInput(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool


class AuthResponse(BaseModel):
    token: str
    user: UserOut


class Content(BaseModel):
    id: int
    type: str
    title: str
    description: str
    cover_url: str
    external_url: str | None = None
    author: str
    tags: list[str]
    like_count: int = 0
    favorite_count: int = 0
    view_count: int = 0
    created_at: datetime
    status: str = "approved"
    rejection_reason: str | None = None
    liked: bool = False
    favorited: bool = False


class ContentCreate(BaseModel):
    type: str
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=5000)
    cover_url: str = ""
    external_url: str | None = None
    tags: list[str] = Field(default_factory=list, max_length=5)

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str) -> str:
        if value not in {"film", "dance", "image", "song", "fanwork"}:
            raise ValueError("不支持的内容分类")
        return value

    @field_validator("external_url")
    @classmethod
    def validate_external_url(cls, value: str | None) -> str | None:
        if value and not any(host in value.lower() for host in ("bilibili.com", "y.qq.com", "kugou.com", "weibo.com")):
            raise ValueError("外部链接仅支持哔哩哔哩、QQ 音乐、酷狗或微博")
        return value


class CommentCreate(BaseModel):
    body: str = Field(min_length=1, max_length=1000)
    parent_id: int | None = None


class Comment(BaseModel):
    id: int
    content_id: int
    user_id: int
    username: str
    body: str
    parent_id: int | None = None
    created_at: datetime
    reported: bool = False


class ReportCreate(BaseModel):
    reason: str = Field(min_length=2, max_length=200)


RECOMMENDATIONS = [
    Recommendation(id=1, category="影视入坑", title="从一部剧认识她", subtitle="角色塑造 · 氛围感", description="适合第一次了解鞠婧祎的你：从角色、造型和情绪表达，慢慢发现她的独特气质。", accent="01"),
    Recommendation(id=2, category="舞台安利", title="看见舞台上的光", subtitle="舞台表现 · 音乐现场", description="把镜头交给舞台，感受轻盈的动作、稳定的状态和属于她的闪光时刻。", accent="02"),
    Recommendation(id=3, category="作品收藏", title="建立你的作品清单", subtitle="影视作品 · 个人偏好", description="收藏喜欢的角色与片段，记录每一次心动，也欢迎写下你自己的推荐理由。", accent="03"),
]


def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)
    return f"{salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    salt_hex, digest_hex = stored.split("$", 1)
    expected = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), 120_000).hex()
    return hmac.compare_digest(expected, digest_hex)


def make_token(user_id: int) -> str:
    payload = base64.urlsafe_b64encode(json.dumps({"user_id": user_id}).encode()).decode().rstrip("=")
    signature = hmac.new(TOKEN_SECRET, payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{signature}"


def get_user_from_token(credentials: HTTPAuthorizationCredentials | None) -> User | None:
    if not credentials or credentials.scheme.lower() != "bearer" or "." not in credentials.credentials:
        return None
    payload, signature = credentials.credentials.split(".", 1)
    expected = hmac.new(TOKEN_SECRET, payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return None
    try:
        return USERS.get(int(json.loads(base64.urlsafe_b64decode(payload + "===")).get("user_id")))
    except (ValueError, TypeError, json.JSONDecodeError):
        return None


def current_user(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]) -> User:
    user = get_user_from_token(credentials)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="请先登录")
    return user


USERS: dict[int, User] = {1: User(id=1, username="admin", password_hash=hash_password("admin12345"), is_admin=True)}
CONTENTS: list[Content] = [
    Content(id=1, type="film", title="影视作品精选", description="从角色、造型和情绪表达开始，认识她在镜头里的不同侧面。", cover_url="/assets/portrait-film.jpg", author="收藏馆编辑部", tags=["影视", "角色", "入坑推荐"], like_count=128, favorite_count=96, view_count=860, created_at=datetime.now(timezone.utc) - timedelta(days=3)),
    Content(id=2, type="film", title="值得回看的角色片段", description="整理适合新朋友入坑的角色观察笔记，欢迎写下你的第一印象。", cover_url="/assets/hero-collage.jpg", author="蓝色放映室", tags=["影视", "片段", "安利"], like_count=96, favorite_count=72, view_count=510, created_at=datetime.now(timezone.utc) - timedelta(days=12)),
    Content(id=3, type="dance", title="舞台上的高光时刻", description="记录舞台动作、音乐和灯光交汇的瞬间，感受现场表现力。", cover_url="/assets/hero-collage.jpg", author="舞台观察员", tags=["舞蹈", "舞台", "现场"], like_count=156, favorite_count=110, view_count=1030, created_at=datetime.now(timezone.utc) - timedelta(days=5)),
    Content(id=4, type="image", title="蓝色胶片视觉手记", description="用一组蓝色调画面，收藏那些安静又有力量的瞬间。", cover_url="/assets/portrait-film.jpg", author="BCXG", tags=["图片", "胶片", "视觉"], like_count=210, favorite_count=188, view_count=1400, created_at=datetime.now(timezone.utc) - timedelta(days=2)),
    Content(id=5, type="song", title="单曲循环推荐", description="从旋律开始，记录适合不同心情反复聆听的歌曲和现场。", cover_url="/assets/illustration.png", author="耳机收藏家", tags=["歌曲", "音乐", "循环"], like_count=88, favorite_count=65, view_count=430, created_at=datetime.now(timezone.utc) - timedelta(days=35)),
    Content(id=6, type="fanwork", title="给喜欢留一张手写卡片", description="粉丝视角的图文二创示例，欢迎未来发布你的作品和推荐理由。", cover_url="/assets/illustration.png", author="星星邮局", tags=["二创", "图文", "粉丝作品"], like_count=174, favorite_count=132, view_count=920, created_at=datetime.now(timezone.utc) - timedelta(days=8)),
]
LIKES: set[tuple[int, int]] = set()
FAVORITES: set[tuple[int, int]] = set()
COMMENTS: list[Comment] = []
REPORTS: list[dict] = []


def public_user(user: User) -> UserOut:
    return UserOut(id=user.id, username=user.username, is_admin=user.is_admin)


def visible_content(item: Content, user: User | None = None) -> Content:
    return item.model_copy(update={"liked": bool(user and (user.id, item.id) in LIKES), "favorited": bool(user and (user.id, item.id) in FAVORITES)})


def find_content(content_id: int) -> Content:
    for item in CONTENTS:
        if item.id == content_id:
            return item
    raise HTTPException(status_code=404, detail="内容不存在")


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "cloud-collection-api"}


@app.get("/api/recommendations", response_model=list[Recommendation])
def list_recommendations() -> list[Recommendation]:
    return RECOMMENDATIONS


@app.post("/api/auth/register", response_model=AuthResponse, status_code=201)
def register(payload: RegisterInput) -> AuthResponse:
    try:
        payload.check_passwords()
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if any(user.username == payload.username for user in USERS.values()):
        raise HTTPException(status_code=409, detail="用户名已存在")
    user = User(id=max(USERS) + 1, username=payload.username, password_hash=hash_password(payload.password))
    USERS[user.id] = user
    return AuthResponse(token=make_token(user.id), user=public_user(user))


@app.post("/api/auth/login", response_model=AuthResponse)
def login(payload: LoginInput) -> AuthResponse:
    user = next((item for item in USERS.values() if item.username == payload.username), None)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return AuthResponse(token=make_token(user.id), user=public_user(user))


@app.get("/api/auth/me", response_model=UserOut)
def me(user: Annotated[User, Depends(current_user)]) -> UserOut:
    return public_user(user)


@app.get("/api/contents", response_model=list[Content])
def list_contents(content_type: str | None = Query(default=None, alias="type"), keyword: str | None = None, sort: str = Query(default="latest", pattern="^(latest|popular)$"), period: str = Query(default="all", pattern="^(all|week|month)$"), page: int = Query(default=1, ge=1), page_size: int = Query(default=6, ge=1, le=30), credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)] = None) -> list[Content]:
    user = get_user_from_token(credentials)
    results = [item for item in CONTENTS if item.status == "approved"]
    if content_type:
        results = [item for item in results if item.type == content_type]
    if keyword:
        query = keyword.casefold()
        results = [item for item in results if query in f"{item.title} {item.description} {' '.join(item.tags)}".casefold()]
    if period != "all":
        days = 7 if period == "week" else 30
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        results = [item for item in results if item.created_at >= cutoff]
    if sort == "popular":
        results.sort(key=lambda item: item.like_count * 0.5 + item.favorite_count * 0.3 + item.view_count * 0.2, reverse=True)
    else:
        results.sort(key=lambda item: item.created_at, reverse=True)
    start = (page - 1) * page_size
    return [visible_content(item, user) for item in results[start:start + page_size]]


@app.get("/api/contents/{content_id}", response_model=Content)
def get_content(content_id: int, credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)] = None) -> Content:
    item = find_content(content_id)
    if item.status != "approved":
        raise HTTPException(status_code=404, detail="内容不存在")
    item.view_count += 1
    return visible_content(item, get_user_from_token(credentials))


@app.get("/api/contents/{content_id}/related", response_model=list[Content])
def related_contents(content_id: int) -> list[Content]:
    item = find_content(content_id)
    return [candidate for candidate in CONTENTS if candidate.id != item.id and candidate.status == "approved" and (candidate.type == item.type or set(candidate.tags) & set(item.tags))][:4]


@app.post("/api/contents/{content_id}/like")
def toggle_like(content_id: int, user: Annotated[User, Depends(current_user)]) -> dict[str, bool | int]:
    item = find_content(content_id)
    key = (user.id, item.id)
    if key in LIKES:
        LIKES.remove(key); item.like_count = max(0, item.like_count - 1); liked = False
    else:
        LIKES.add(key); item.like_count += 1; liked = True
    return {"liked": liked, "like_count": item.like_count}


@app.post("/api/contents/{content_id}/favorite")
def toggle_favorite(content_id: int, user: Annotated[User, Depends(current_user)]) -> dict[str, bool | int]:
    item = find_content(content_id)
    key = (user.id, item.id)
    if key in FAVORITES:
        FAVORITES.remove(key); item.favorite_count = max(0, item.favorite_count - 1); favorited = False
    else:
        FAVORITES.add(key); item.favorite_count += 1; favorited = True
    return {"favorited": favorited, "favorite_count": item.favorite_count}


@app.get("/api/contents/{content_id}/comments", response_model=list[Comment])
def list_comments(content_id: int) -> list[Comment]:
    find_content(content_id)
    return [comment for comment in COMMENTS if comment.content_id == content_id and not comment.reported]


@app.post("/api/contents/{content_id}/comments", response_model=Comment, status_code=201)
def create_comment(content_id: int, payload: CommentCreate, user: Annotated[User, Depends(current_user)]) -> Comment:
    find_content(content_id)
    comment = Comment(id=len(COMMENTS) + 1, content_id=content_id, user_id=user.id, username=user.username, body=payload.body, parent_id=payload.parent_id, created_at=datetime.now(timezone.utc))
    COMMENTS.append(comment)
    return comment


@app.post("/api/comments/{comment_id}/report")
def report_comment(comment_id: int, payload: ReportCreate, user: Annotated[User, Depends(current_user)]) -> dict[str, str]:
    comment = next((item for item in COMMENTS if item.id == comment_id), None)
    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")
    REPORTS.append({"comment_id": comment_id, "user_id": user.id, "reason": payload.reason})
    comment.reported = True
    return {"status": "reported"}


@app.post("/api/contents", response_model=Content, status_code=201)
def create_content(payload: ContentCreate, user: Annotated[User, Depends(current_user)]) -> Content:
    item = Content(id=max((content.id for content in CONTENTS), default=0) + 1, type=payload.type, title=payload.title, description=payload.description, cover_url=payload.cover_url, external_url=payload.external_url, author=user.username, tags=payload.tags, created_at=datetime.now(timezone.utc), status="pending")
    CONTENTS.append(item)
    return item


@app.get("/api/admin/pending", response_model=list[Content])
def pending_contents(user: Annotated[User, Depends(current_user)]) -> list[Content]:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return [item for item in CONTENTS if item.status == "pending"]


@app.post("/api/admin/contents/{content_id}/review", response_model=Content)
def review_content(content_id: int, user: Annotated[User, Depends(current_user)], approved: bool, reason: str | None = None) -> Content:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    item = find_content(content_id)
    item.status = "approved" if approved else "rejected"
    item.rejection_reason = None if approved else (reason or "未通过审核")
    return item
