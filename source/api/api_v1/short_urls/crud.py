from json import JSONDecodeError

from .schemas import ShortUrl, ShortUrlCreate, ShortUrlUpdate, ShortUrlPartialUpdate
from pydantic import BaseModel, ValidationError
import json
import os


class ShortUrlStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def __init__(self, **data):
        super().__init__(**data)
        self.slug_to_short_url = self._load_json_file()

    def _load_json_file(self) -> dict[str, ShortUrl]:
        data = {}
        print(os.listdir())
        if 'storage_short_url.json' in os.listdir():
            try:
                with open('storage_short_url.json', 'r', encoding='utf-8') as file:
                    loaded_data = json.load(file)
                    for slug, obj in loaded_data.items():
                        data[slug] = ShortUrl.model_validate_json(obj)
                    print(data)
            except JSONDecodeError:
                return data
        return data

    def _save_to_file(self):
        with open('storage_short_url.json', 'w', encoding='utf-8') as file:
            print(self.slug_to_short_url.items())
            data = {slug: url.model_dump_json() for slug, url in self.slug_to_short_url.items()}
            print(data)
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_all(self) -> list[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_short_url.get(slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump()
        )
        self.slug_to_short_url[short_url.slug] = short_url
        self._save_to_file()

        return short_url

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ):
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)

        self._save_to_file()
        return short_url

    def update_partial(
            self,
            short_url: ShortUrl,
            short_url_in: ShortUrlPartialUpdate,
        ):
        new_data = short_url_in.model_dump(exclude_unset=True).items()
        for field_name, value in new_data:
            setattr(short_url, field_name, value)

        self._save_to_file()
        return short_url


    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_short_url.pop(slug, None)
        self._save_to_file()

    def delete(self, short_url: ShortUrl):
        self.delete_by_slug(short_url.slug)


storage = ShortUrlStorage()

# SHORT_URLS = [
#     ShortUrl(
#         target_url="http://google.com",
#         slug="search",
#     ),
#     ShortUrl(
#         target_url="http://rutube.ru",
#         slug="video",
#     ),
# ]

u1 = ShortUrlCreate(
    target_url="http://google.com",
    slug="search",
)

u2 = ShortUrlCreate(
    target_url="http://rutube.ru",
    slug="video",
)

if u1.slug not in storage.slug_to_short_url:
    storage.create(short_url_in=u1)
if u2.slug not in storage.slug_to_short_url:
    storage.create(short_url_in=u2)


