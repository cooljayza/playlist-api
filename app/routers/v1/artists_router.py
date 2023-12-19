from fastapi import APIRouter, Depends, Query
from app.services.artists_service import ArtistsService
from app.dependency import get_artists_service
from typing import Optional
from app.schemas.artist_response import ArtistResponse
from app.schemas.paginated_response import PaginatedResponse


router = APIRouter(tags=['Artists'], prefix='/artists')


@router.get('/', response_model=PaginatedResponse[ArtistResponse])
async def get_many_artists(page: int = Query(1, ge=1), per_page: int = Query(100, ge=1),
                           name: Optional[str] = Query(None), service: ArtistsService = Depends(get_artists_service)):
    results = service.get_many_artists(page, per_page, name)

    results['items'] = [ArtistResponse(**artist.dict()) for artist in results['items']]

    return results
