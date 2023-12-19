from app.models.playlist import Playlist
from app.services.playlists_service import PlaylistsService


def log_playlist_songs(playlist: Playlist, service: PlaylistsService):
    for song in playlist.playlist_songs:
        song.play_count += 1
    service.update_playlist(playlist)
