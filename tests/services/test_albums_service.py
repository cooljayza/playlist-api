import pytest
from unittest.mock import Mock, patch, ANY
from app.models.album import Album
from app.services.albums_service import AlbumsService
from app.repositories.albums_repositories import AlbumsRepositories


@pytest.fixture
def albums_service():
    mock_repo = Mock(spec=AlbumsRepositories)
    return AlbumsService(repo=mock_repo)


def test_get_many_albums_with_title(albums_service):
    # Arrange
    title_to_search = "Test Album"
    page = 1
    per_page = 10

    # Act
    with patch.object(albums_service._repo, 'get_many') as mock_get_many:
        albums_service.get_many_albums(page=page, per_page=per_page, title=title_to_search)

    # Assert
    mock_get_many.assert_called_once_with(ANY, page=page, per_page=per_page)


def test_get_many_albums_without_title(albums_service):
    # Arrange
    page = 1
    per_page = 10

    # Act
    with patch.object(albums_service._repo, 'get_many') as mock_get_many:
        albums_service.get_many_albums(page=page, per_page=per_page)

    # Assert
    mock_get_many.assert_called_once_with(ANY, page=page, per_page=per_page)