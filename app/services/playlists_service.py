from app.repositories.playlists_repository import PlaylistsRepository
from app.models.playlist import Playlist
from app.models.playlist_song import PlaylistSong
from app.models.song import Song
from typing import Optional
import random


class PlaylistsService:
    def __init__(self, repo: PlaylistsRepository):
        self._repo = repo

    def add_playlist(self, playlist: Playlist):
        old_playlist = self._repo.get_many(Playlist.name == playlist.name)['items'].first()
        if old_playlist:
            return old_playlist

        return self._repo.add(playlist)

    def add_song_to_playlist(self, playlist: Playlist, song: Song) -> PlaylistSong:
        to_add = True
        pl_song = None
        for ps in playlist.playlist_songs:
            if ps.song_id == song.id and ps.isActive:
                to_add = False
                pl_song = ps

        if to_add:
            next_number = (0 if len(playlist.playlist_songs) == 0 else max(playlist.playlist_songs, key=lambda x: x.rank).rank) + 1
            pl_song = PlaylistSong(song_id=song.id, rank=next_number)
            playlist.playlist_songs.append(pl_song)
            self._repo.update(playlist)
            self._reorder_items(playlist)

            return pl_song

        if pl_song:
            return pl_song

        raise LookupError('Song not found or already added')

    def get_playlist_by_id(self, playlist_id) -> Playlist:
        playlist: Playlist = self._repo.get_by_id(playlist_id).first()

        return playlist

    def remove_song_from_playlist(self, playlist_song: PlaylistSong) -> PlaylistSong:
        playlist_song.isActive = False
        playlist = playlist_song.playlist
        pl_song = self._repo.update(playlist_song)
        self._reorder_items(playlist)

        return pl_song

    def swap_playlist_order(self, song_1: PlaylistSong, song_2: PlaylistSong):
        tmp = song_1.rank
        song_1.rank = song_2.rank
        song_2.rank = tmp

        self._repo.update(song_1)
        self._repo.update(song_2)

        return [song_1, song_2]

    def shuffle_playlist(self, playlist: Playlist):
        random.shuffle(playlist.playlist_songs)

        return playlist

    def delete_playlist(self, playlist):
        return self._repo.delete(playlist)

    def get_many(self, page: int, per_page: int, name: Optional):
        filters = []
        if name:
            filters.append(Playlist.name == name)
        return self._repo.get_many(*filters, page=page, per_page=per_page)

    def get_playlist_by_name(self, name: str) -> Playlist:
        playlist = self._repo.get_many(Playlist.name == name)['items'].first()
        return playlist

    def update_playlist(self, playlist: Playlist) -> Playlist:
        return self._repo.update(playlist)

    def _reorder_items(self, playlist: Playlist):
        playlist.playlist_songs = sorted(playlist.playlist_songs, key=lambda x: x.rank)
        count = 0
        for item in playlist.playlist_songs:
            if item.isActive:
                count += 1
                item.rank = count
        return self._repo.update(playlist)
