from app.stores.sql_store import SqlStore
from app.repositories.songs_repository import SongsRepository
from app.services.songs_service import SongsService
from app.repositories.playlists_repository import PlaylistsRepository
from app.repositories.albums_repositories import AlbumsRepositories
from app.services.albums_service import AlbumsService
from app.repositories.artists_repository import ArtistsRepository
from app.services.artists_service import ArtistsService
from app.services.playlists_service import PlaylistsService
from fastapi import Depends
import os


DATABASE_URL = os.environ["DATABASE_URL"]


def get_store():
    store = SqlStore(DATABASE_URL)
    store.connect()

    yield store


def get_songs_service(store: SqlStore = Depends(get_store)):
    repo = SongsRepository(store)
    service = SongsService(repo)

    yield service


def get_artists_service(store: SqlStore = Depends(get_store)):
    repo = ArtistsRepository(store)
    service = ArtistsService(repo)

    yield service


def get_albums_service(store: SqlStore = Depends(get_store)):
    repo = AlbumsRepositories(store)
    service = AlbumsService(repo)

    yield service


def get_playlist_service(store: SqlStore = Depends(get_store)):
    repo = PlaylistsRepository(store)
    service = PlaylistsService(repo)

    yield service

