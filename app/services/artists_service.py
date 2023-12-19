from app.repositories.artists_repository import ArtistsRepository
from typing import Optional
from app.models.artist import Artist


class ArtistsService:
    def __init__(self, repo: ArtistsRepository):
        self._repo = repo

    def get_many_artists(self, page: int, per_page: int, name: Optional[str] = None):
        filters = []
        if name:
            filters.append(Artist.name == name)
        return self._repo.get_many(*filters, page=page, per_page=per_page)
