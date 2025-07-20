from typing import Annotated

# from pydantic import AnyHttpUrl
# from annotated_types import Len

from api.api_v1.short_urls.schemas import ShortUrl, ShortUrlCreate, ShortUrlRead
# from fastapi.responses import RedirectResponse
from api.api_v1.short_urls.dependencies import prefetch_short_url, storage
from fastapi import Request, HTTPException, status, Depends, APIRouter, Form


router = APIRouter(prefix="/short-urls")


@router.get(
    "/list/",
    response_model=list[ShortUrlRead]
)
def read_short_urls_list() -> list[ShortUrl]:
    return storage.get_all()



@router.post(
    "/",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: ShortUrlCreate,
):
    new_url = ShortUrl(
        **short_url_create.model_dump(),
    )

    storage.create(new_url)

    return new_url



