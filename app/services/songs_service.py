from sqlalchemy.orm import relationship

from app.models.song import Song
from app.repositories.songs_repository import SongsRepository
from app.models.artist_album import ArtistAlbum
from app.models.artist import Artist
from app.models.album import Album

Song.artist_album = relationship(ArtistAlbum, back_populates='songs')
ArtistAlbum.songs = relationship(Song, back_populates='artist_album')
ArtistAlbum.artist = relationship(Artist, back_populates='artist_albums')
Artist.artist_albums = relationship(ArtistAlbum, back_populates='artist')
ArtistAlbum.album = relationship(Album, back_populates='artist_album')
Album.artist_album = relationship(ArtistAlbum, back_populates='album')


class SongsService:
    def __init__(self, repo: SongsRepository):
        self._repo = repo

    def get_many(self, page: int, per_page: int, artist_id: int | None = None, album_id: int | None = None, year:
                 int | None = None, title: str | None = None):
        filters = []

        if artist_id:
            filters.append(ArtistAlbum.artist_id == artist_id)
        if album_id:
            filters.append(ArtistAlbum.album_id == album_id)
        if year:
            filters.append(ArtistAlbum.year == year)
        if title:
            filters.append(Song.title.ilike(f'%{title}%'))

        return self._repo.get_many_with_join(ArtistAlbum, 'artist_album', *filters, per_page=per_page, page=page)

    def find_song_by_id(self, song_id):
        song: Song = self._repo.get_by_id(song_id).first()

        return song
