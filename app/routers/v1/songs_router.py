from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.songs_service import SongsService
from app.dependency import get_songs_service
from app.schemas.song_schema import SongResponse
from app.models.song import Song
from app.schemas.paginated_response import PaginatedResponse
from app.models.album import Album
from app.models.artist import Artist
from app.models.artist_album import ArtistAlbum
from sqlalchemy.orm import relationship
from typing import Optional

Song.artist_album = relationship(ArtistAlbum, back_populates='songs')
ArtistAlbum.songs = relationship(Song, back_populates='artist_album')
ArtistAlbum.artist = relationship(Artist, back_populates='artist_albums')
Artist.artist_albums = relationship(ArtistAlbum, back_populates='artist')
ArtistAlbum.album = relationship(Album, back_populates='artist_album')
Album.artist_album = relationship(ArtistAlbum, back_populates='album')


router = APIRouter(
    prefix='/songs', tags=['Songs']
)


@router.get('/', response_model=PaginatedResponse[SongResponse])
def get_all_songs(service: SongsService = Depends(get_songs_service), page: int = Query(1, ge=1), per_page:
                  int = Query(100, ge=1), artist_id: Optional[int] = Query(None, ge=1), album_id:
                  Optional[int] = Query(None, ge=1), release_year: Optional[int] = Query(None, ge=1800)):

    results = service.get_many(page=page, per_page=per_page, artist_id=artist_id, album_id=album_id, year=release_year)
    results['items'] = [SongResponse().from_model(song) for song in results['items']]

    return results
