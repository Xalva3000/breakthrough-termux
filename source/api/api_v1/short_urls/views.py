from typing import Annotated
from .schemas import ShortUrl
from fastapi.responses import RedirectResponse
from .dependencies import prefetch_short_url
from fastapi import Request, HTTPException, status, Depends, APIRouter


router = APIRouter(prefix="/short-urls")



@router.get("/list/")
def read_short_urls_list():
    return SHORT_URLS
