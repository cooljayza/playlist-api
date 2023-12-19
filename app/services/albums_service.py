from app.models.album import Album
from app.repositories.albums_repositories import AlbumsRepositories


class AlbumsService:
    def __init__(self, repo: AlbumsRepositories):
        self._repo = repo

    def get_many_albums(self, page: int, per_page: int, title: str = None):
        filters = []
        if title:
            filters.append(Album.title == title)
        return self._repo.get_many(*filters, page=page, per_page=per_page)
