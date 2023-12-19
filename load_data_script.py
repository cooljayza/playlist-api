import json
import os
import sys
from dotenv import load_dotenv
from app.stores.sql_store import SqlStore
from app.models import song, artist_album, album, artist
from app.repositories import songs_repository, artists_repository, artist_albums_repositories, albums_repositories


BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

DATABASE_URL = os.environ["DATABASE_URL"]

store = SqlStore(DATABASE_URL)
store.connect()
songs_repo = songs_repository.SongsRepository(store)
artists_repo = artists_repository.ArtistsRepository(store)
albums_repo = albums_repositories.AlbumsRepositories(store)
artist_albums_repo = artist_albums_repositories.ArtistAlbumsRepositories(store)


with open('songs.json') as file:
    json_data = json.load(file)
    user_len = os.environ.get('SONG_COUNT')
    length = len(json_data['songs']) if not user_len else int(user_len)
    count = 0
    for song_dict in json_data['songs'][:length]:
        _artist: artist.Artist = artists_repo.get_many(artist.Artist.name == song_dict['artist'])['items'].first()
        if not _artist:
            _artist = artists_repo.add(artist.Artist(name=song_dict['artist']))
        _album: album.Album = albums_repo.get_many(album.Album.title == song_dict['album'])['items'].first()
        if not _album:
            _album = albums_repo.add(album.Album(title=song_dict['album']))

        _artist_album: artist_album.ArtistAlbum = artist_albums_repo.get_many(artist_album.ArtistAlbum.artist_id == _artist.id,
                                                    artist_album.ArtistAlbum.album_id == _album.id,
                                                    artist_album.ArtistAlbum.year == int(song_dict['year']))['items'].first()
        if not _artist_album:
            _artist_album = artist_albums_repo.add(artist_album.ArtistAlbum(artist_id=_artist.id, album_id=_album.id,
                                                                            year=int(song_dict['year'])))

        _song = songs_repo.get_many(song.Song.title == song_dict['title'],
                                      song.Song.artist_album_id == _artist_album.id)['items'].first()
        if not _song:
            _song = songs_repo.add(song.Song(title=song_dict['title'], artist_album_id=_artist_album.id,
                                             rank=song_dict['rank']))
            count += 1

    print(f'{count} Songs added.')
