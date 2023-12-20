import pytest
from unittest.mock import Mock, patch, ANY
from app.services.artists_service import ArtistsService
from app.repositories.artists_repository import ArtistsRepository


@pytest.fixture
def artists_service():
    mock_repo = Mock(spec=ArtistsRepository)
    return ArtistsService(repo=mock_repo)


def test_get_many_artists_with_name(artists_service):
    # Arrange
    name_to_search = "Test Artist"
    page = 1
    per_page = 10

    # Act
    with patch.object(artists_service._repo, 'get_many') as mock_get_many:
        artists_service.get_many_artists(page=page, per_page=per_page, name=name_to_search)

    # Assert
    mock_get_many.assert_called_once_with(ANY, page=page, per_page=per_page)


def test_get_many_artists_without_name(artists_service):
    # Arrange
    page = 1
    per_page = 10
    expected_filters = []

    # Act
    with patch.object(artists_service._repo, 'get_many') as mock_get_many:
        artists_service.get_many_artists(page=page, per_page=per_page)

    # Assert
    mock_get_many.assert_called_once_with(*expected_filters, page=page, per_page=per_page)
