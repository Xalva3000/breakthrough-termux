import uvicorn
from typing import Annotated
from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
)
from schemas.short_url import ShortUrl
from fastapi.responses import RedirectResponse

SHORT_URLS = [
    ShortUrl(
        target_url="http://google.com",
        slug="search",
    ),
    ShortUrl(
        target_url="http://rutube.ru",
        slug="video",
    ),
]


app = FastAPI(
    title="Breakthrough",
)


def prefetch_short_url(slug: str):
    url: ShortUrl | None = next((url for url in SHORT_URLS if url.slug == slug), None)

    return url


@app.get(
    "/",
    response_model=list[ShortUrl],
)
def greet(request: Request, name: str = "Alex"):
    docs_url = request.url.replace(path="/docs")
    return {
        "message": f"Hello, {name}",
        "docs": str(docs_url),
    }


@app.get("/short-urls")
def read_short_urls_list():
    return SHORT_URLS


@app.get("/r/{slug}")
@app.get("/r/{slug}/")
def redirect_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ]
):
    if url:
        return RedirectResponse(url=url.target_url)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
