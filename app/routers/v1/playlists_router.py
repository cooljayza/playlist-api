from fastapi import APIRouter, Depends, Query, HTTPException, Request, BackgroundTasks
from app.models.playlist import Playlist
from app.dependency import get_playlist_service, get_songs_service
from app.services.playlists_service import PlaylistsService
from app.services.songs_service import SongsService
from app.schemas.create_playlist import CreatePlaylistRequest, CreatePlaylistResponse
from app.schemas.paginated_response import PaginatedResponse
from app.schemas.playlist_swap import PlaylistSongSwap
from app.schemas.song_schema import SongResponse
from app.schemas.playlist_song import PlaylistSongResponse
from app.schemas.create_playlist_song import CreatePlaylistSongRequest, CreatePlaylistSongResponse
from typing import List, Optional
from app.services.workers.playlist_request_logger import log_playlist_songs


router = APIRouter(
    prefix='/playlists', tags=['Playlists']
)


async def playlist_validator(request: Request, service: PlaylistsService = Depends(get_playlist_service)):
    playlist_id = request.path_params['playlist_id'] if 'playlist_id' in request.path_params else None
    playlist = service.get_playlist_by_id(playlist_id)

    if playlist:
        return playlist
    else:
        raise HTTPException(404, 'Playlist not found')


@router.post('/', response_model=CreatePlaylistResponse)
async def create_playlist(playlist: CreatePlaylistRequest, service: PlaylistsService = Depends(get_playlist_service)):
    return service.add_playlist(Playlist(**playlist.dict()))


@router.post('/{playlist_id}/songs', response_model=CreatePlaylistSongResponse)
async def add_song_to_playlist(playlist_id, dto: CreatePlaylistSongRequest, playlist: Playlist = Depends(
    playlist_validator), pl_service: PlaylistsService = Depends(get_playlist_service), song_service: SongsService
                               = Depends(get_songs_service)):
    song = song_service.find_song_by_id(dto.song_id)
    if song:
        playlist_song = pl_service.add_song_to_playlist(playlist, song)
        return CreatePlaylistSongResponse(rank=playlist_song.rank, playlist=CreatePlaylistResponse(
            **playlist_song.playlist.dict()), song=SongResponse().from_model(playlist_song.song))
    else:
        raise HTTPException(404, 'Song not found')


@router.get('/', response_model=PaginatedResponse[CreatePlaylistResponse])
async def get_many_playlists(page: int = Query(1, ge=1), per_page: int = Query(100, ge=1),
                             name: Optional[str] = Query(None),
                             service: PlaylistsService = Depends(get_playlist_service)):
    response = service.get_many(page, per_page, name)
    response['items'] = [CreatePlaylistResponse(**pl.dict()) for pl in response['items']]
    return response


@router.get('/{playlist_id}/songs', response_model=List[PlaylistSongResponse])
async def get_playlist_songs(playlist_id, bg_tasks: BackgroundTasks, playlist: Playlist = Depends(playlist_validator),
                             service: PlaylistsService = Depends(get_playlist_service)):
    songs = [PlaylistSongResponse(rank=song.rank, song=SongResponse().from_model(song.song))
             for song in playlist.playlist_songs if song.isActive]
    bg_tasks.add_task(log_playlist_songs, playlist, service)
    return songs


@router.get('/{playlist_id}/shuffle', response_model=List[PlaylistSongResponse])
async def shuffle_playlist(playlist_id, bg_tasks: BackgroundTasks, playlist: Playlist = Depends(playlist_validator),
                           service: PlaylistsService = Depends(get_playlist_service)):
    playlist = service.shuffle_playlist(playlist)
    songs = [PlaylistSongResponse(rank=song.rank, song=SongResponse().from_model(song.song)) for song in
             playlist.playlist_songs]
    bg_tasks.add_task(log_playlist_songs, playlist, service)
    return songs


@router.delete('/{playlist_id}', response_model=CreatePlaylistResponse)
async def delete_playlist(playlist_id, playlist: Playlist = Depends(playlist_validator), service: PlaylistsService
= Depends(get_playlist_service)):
    return service.delete_playlist(playlist)


@router.put('/{playlist_id}', response_model=CreatePlaylistResponse)
async def update_playlist(playlist_id, updated: CreatePlaylistRequest, playlist: Playlist = Depends(playlist_validator),
                          service: PlaylistsService = Depends(get_playlist_service)):
    similar_pl = service.get_playlist_by_name(updated.name)
    if similar_pl:
        raise HTTPException(422, 'Name already exists')
    playlist.name = updated.name
    playlist = service.update_playlist(playlist)
    return playlist


@router.delete('/{playlist_id}/songs/{song_id}')
async def remove_song_from_playlist(playlist_id, song_id, playlist: Playlist = Depends(playlist_validator),
                                    service: PlaylistsService = Depends(get_playlist_service)):
    playlist_songs = [pl for pl in playlist.playlist_songs if pl.song_id == int(song_id)]
    if len(playlist_songs) > 0:
        playlist_song = playlist_songs[0]
        pl_dto = CreatePlaylistSongResponse(rank=playlist_song.rank, playlist=CreatePlaylistResponse(
            **playlist_song.playlist.dict()), song=SongResponse().from_model(playlist_song.song))
        service.remove_song_from_playlist(playlist_song)
        return pl_dto

    raise HTTPException(404, 'Song not found on playlist.')


@router.put('/{playlist_id}/swap', response_model=List[PlaylistSongResponse])
async def swap_playlist_songs(playlist_id, songs: PlaylistSongSwap, playlist: Playlist = Depends(playlist_validator),
                              service:
                              PlaylistsService = Depends(get_playlist_service)):
    songs_1 = [pl for pl in playlist.playlist_songs if pl.song_id == songs.song1_id]
    songs_2 = [pl for pl in playlist.playlist_songs if pl.song_id == songs.song2_id]

    if len(songs_1) > 0 and len(songs_2) > 0:
        service.swap_playlist_order(songs_1[0], songs_2[0])
        return [PlaylistSongResponse(rank=pl.rank, song=SongResponse().from_model(pl.song)) for pl in
                playlist.playlist_songs]

    raise HTTPException(422, 'Not all songs found in playlist')


@router.get('/search')
async def search_playlist(bg_tasks: BackgroundTasks, q: str = Query(), page: int = Query(1, ge=1),
                          per_page: int = Query(100, ge=1), service: PlaylistsService = Depends(get_playlist_service)):
    results = service.search_playlist(q, page, per_page)
    new_items = []
    for playlist in results['items']:
        new_items.append({
            'playlist': CreatePlaylistResponse(**playlist.dict()),
            'songs': [PlaylistSongResponse(rank=song.rank, song=SongResponse().from_model(song.song))
                      for song in playlist.playlist_songs if song.isActive]
        })
        bg_tasks.add_task(log_playlist_songs, playlist, service)
    results['items'] = new_items
    return results
