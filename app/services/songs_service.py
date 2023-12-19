from app.models.song import Song
from app.repositories.songs_repository import SongsRepository


class SongsService:
    def __init__(self, repo: SongsRepository):
        self._repo = repo

    def get_many(self, page: int, per_page: int, artist_id: int | None = None, album_id: int | None = None, year:
                 int | None = None):
        filters = []
        if artist_id:
            filters.append(Song.artist_album.artist_id == artist_id)
        if album_id:
            filters.append(Song.artist_album.album_id == album_id)
        if year:
            filters.append(Song.artist_album.year == year)

        return self._repo.get_many(*filters, per_page=per_page, page=page)

    def find_song_by_id(self, song_id):
        song: Song = self._repo.get_by_id(song_id).first()

        return song
