from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Cloud Collection API",
    description="云端收藏馆后端 API",
    version="0.1.0",
)


class Pet(BaseModel):
    id: int
    name: str
    attribute: str
    rarity: str
    description: str
    emoji: str


PETS = [
    Pet(id=1, name="火花", attribute="火系", rarity="稀有", description="喜欢温暖阳光的小火焰，进化后拥有更强的爆发力。", emoji="🔥"),
    Pet(id=2, name="喵喵", attribute="草系", rarity="普通", description="森林里的绿色精灵，性格温顺但十分机灵。", emoji="🌿"),
    Pet(id=3, name="水蓝蓝", attribute="水系", rarity="稀有", description="来自湖泊的水之精灵，擅长使用水流进行攻击。", emoji="💧"),
    Pet(id=4, name="小翼龙", attribute="翼系", rarity="史诗", description="拥有远古血脉的飞行宠物，喜欢在云层中穿梭。", emoji="🪽"),
]


@app.get("/api/health")
def health_check() -> dict[str, str]:
    """Return a small response used by the frontend and deployment probes."""
    return {"status": "ok", "service": "cloud-collection-api"}


@app.get("/api/pets", response_model=list[Pet])
def list_pets() -> list[Pet]:
    """Return the first batch of catalogue data until a database is introduced."""
    return PETS

