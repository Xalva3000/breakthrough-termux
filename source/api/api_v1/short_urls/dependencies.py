import logging

from fastapi import HTTPException, BackgroundTasks
from starlette import status
from .schemas import ShortUrl
from .crud import storage


logger = logging.getLogger(__name__)

def prefetch_short_url(
        slug: str
) -> ShortUrl:

    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    # next((url for url in SHORT_URLS if url.slug == slug), None))

    if url:
        return url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )

def save_storage_state(
        background_tasks: BackgroundTasks,
):
    yield
    background_tasks.add_task(storage.save_state)
    logger.info("Storage save state task is added to pool")
