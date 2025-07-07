from fastapi import APIRouter
from .short_urls import router as router_short_urls
from .movies import router as router_movies


router = APIRouter(prefix="/v1")

router.include_router(router_short_urls)
router.include_router(router_movies)

