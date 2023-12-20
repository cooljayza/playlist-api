import pytest
from unittest.mock import Mock, patch, ANY
from app.models.song import Song
from app.services.songs_service import SongsService
from app.repositories.songs_repository import SongsRepository


@pytest.fixture
def songs_service():
    mock_repo = Mock(spec=SongsRepository)
    return SongsService(repo=mock_repo)


def test_get_many_songs_with_artist_id(songs_service):
    # Arrange
    artist_id_to_search = 1
    page = 1
    per_page = 10

    # Act
    with patch.object(songs_service._repo, 'get_many_with_join') as mock_get_many:
        songs_service.get_many(page=page, per_page=per_page, artist_id=artist_id_to_search)

    # Assert
    mock_get_many.assert_called_once()


def test_get_many_songs_with_album_id(songs_service):
    # Arrange
    album_id_to_search = 2
    page = 1
    per_page = 10

    # Act
    with patch.object(songs_service._repo, 'get_many_with_join') as mock_get_many:
        songs_service.get_many(page=page, per_page=per_page, album_id=album_id_to_search)

    # Assert
    mock_get_many.assert_called_once()


def test_get_many_songs_with_year(songs_service):
    # Arrange
    year_to_search = 2022
    page = 1
    per_page = 10

    # Act
    with patch.object(songs_service._repo, 'get_many_with_join') as mock_get_many:
        songs_service.get_many(page=page, per_page=per_page, year=year_to_search)

    # Assert
    mock_get_many.assert_called_once()


def test_find_song_by_id(songs_service):
    # Arrange
    song_id_to_search = 123
    expected_song = Song(id=song_id_to_search)

    # Mock the get_by_id method of the repository to return the expected song
    songs_service._repo.get_by_id.return_value.first.return_value = expected_song

    # Act
    result = songs_service.find_song_by_id(song_id_to_search)

    # Assert
    assert result == expected_song
