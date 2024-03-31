from api.routes import embed, embed_judge, health, judge
from fastapi.routing import APIRouter

router = APIRouter()
router.include_router(health.router, tags=["Health"])
router.include_router(embed.router, tags=["object"])
router.include_router(judge.router, tags=["object"])
router.include_router(embed_judge.router, tags=["object"])
