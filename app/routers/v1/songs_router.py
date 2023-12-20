from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.songs_service import SongsService
from app.dependency import get_songs_service
from app.schemas.song_schema import SongResponse
from app.schemas.paginated_response import PaginatedResponse
from typing import Optional

router = APIRouter(
    prefix='/songs', tags=['Songs']
)


@router.get('/', response_model=PaginatedResponse[SongResponse])
def get_all_songs(service: SongsService = Depends(get_songs_service), page: int = Query(1, ge=1), per_page:
                  int = Query(100, ge=1), artist_id: Optional[int] = Query(None, ge=1), album_id:
                  Optional[int] = Query(None, ge=1), release_year: Optional[int] = Query(None, ge=1800)):

    results = service.get_many(page, per_page, artist_id, album_id, release_year)
    results['items'] = [SongResponse().from_model(song) for song in results['items']]

    return results


@router.get('/search', response_model=PaginatedResponse[SongResponse])
def search_songs(service: SongsService = Depends(get_songs_service), page: int = Query(1, ge=1),
                 per_page: int = Query(100, ge=1), q: str = Query()):

    results = service.get_many(page, per_page, title=q)

    results['items'] = [SongResponse().from_model(song) for song in results['items']]
    return results
