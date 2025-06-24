import uvicorn
from typing import Annotated
from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
)
from schemas import ShortUrl, Movie
from fastapi.responses import RedirectResponse
from movie_data import MOVIES_LIST


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


def prefetch_movie_data(movie_id: int):
    movie: Movie | None = next((m for m in MOVIES_LIST if m.movie_id == movie_id))
    return movie


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


@app.get("/movies-list")
def get_movies_list():
    return MOVIES_LIST


@app.get("/r/{slug}")
@app.get("/r/{slug}/")
def redirect_short_url(url: Annotated[ShortUrl, Depends(prefetch_short_url)]):
    if url:
        return RedirectResponse(url=url.target_url)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


@app.get("/movie/{movie_id}/")
def get_movie_data_by_id(movie_data: Annotated[Movie, Depends(prefetch_movie_data)]):
    if movie_data:
        return {"movie_data": movie_data}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie not found. Searched id: {movie_id!r}",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
