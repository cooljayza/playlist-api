from fastapi import APIRouter, Query, Depends
from app.schemas.paginated_response import PaginatedResponse
from app.schemas.album_response import AlbumResponse
from typing import Optional
from app.services.albums_service import AlbumsService
from app.dependency import get_albums_service


router = APIRouter(tags=['Albums'], prefix='/albums')


@router.get('/', response_model=PaginatedResponse[AlbumResponse])
async def get_many_albums(page: int = Query(1, ge=1), per_page: int = Query(100, ge=1),
                          title: Optional[str] = Query(None), service: AlbumsService = Depends(get_albums_service)):
    results = service.get_many_albums(page, per_page, title)
    results['items'] = [AlbumResponse(**album.dict(), year=album.artist_album[0].year) for album in results['items']]
    return results
