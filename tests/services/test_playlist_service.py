import pytest
from unittest.mock import Mock, patch
from app.models.playlist import Playlist
from app.models.playlist_song import PlaylistSong
from app.models.song import Song
from app.services.playlists_service import PlaylistsService
from app.repositories.playlists_repository import PlaylistsRepository
from typing import Optional


@pytest.fixture
def playlists_service():
    mock_repo = Mock(spec=PlaylistsRepository)
    return PlaylistsService(repo=mock_repo)


def test_add_playlist(playlists_service):
    # Arrange
    playlist_to_add = Playlist(name="Test Playlist")

    # Mock the get_many method of the repository to return None (indicating no existing playlist with the same name)
    playlists_service._repo.get_many.return_value = {'items': None}

    # Act
    result = playlists_service.add_playlist(playlist_to_add)

    # Assert
    assert result == playlists_service._repo.add.return_value
    playlists_service._repo.add.assert_called_once_with(playlist_to_add)


def test_add_song_to_playlist(playlists_service):
    # Arrange
    playlist_to_add_song = Playlist(name="Test Playlist")
    song_to_add = Song(id=1, name="Test Song")

    # Mock the get_many and update methods of the repository
    playlists_service._repo.get_many.return_value = {'items': [playlist_to_add_song]}
    playlists_service._repo.update.return_value = playlist_to_add_song

    # Act
    result = playlists_service.add_song_to_playlist(playlist_to_add_song, song_to_add)

    # Assert
    assert result == playlists_service._repo.update.return_value.playlist_songs[-1]
    playlists_service._repo.update.assert_called_once_with(playlist_to_add_song)
    playlists_service._reorder_items.assert_called_once_with(playlist_to_add_song)


def test_get_playlist_by_id(playlists_service):
    # Arrange
    playlist_id_to_get = 1
    playlist_to_get = Playlist(id=playlist_id_to_get, name="Test Playlist")

    # Mock the get_by_id method of the repository
    playlists_service._repo.get_by_id.return_value.first.return_value = playlist_to_get

    # Act
    result = playlists_service.get_playlist_by_id(playlist_id_to_get)

    # Assert
    assert result == playlist_to_get
    playlists_service._repo.get_by_id.assert_called_once_with(playlist_id_to_get)
