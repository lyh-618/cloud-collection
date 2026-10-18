from fastapi import FastAPI

app = FastAPI(
    title="Cloud Collection API",
    description="云端收藏馆后端 API",
    version="0.1.0",
)


@app.get("/api/health")
def health_check() -> dict[str, str]:
    """Return a small response used by the frontend and deployment probes."""
    return {"status": "ok", "service": "cloud-collection-api"}

