from fastapi import FastAPI
from app.routers.v1 import songs_router, playlists_router, albums_router, artists_router


app = FastAPI()

app.include_router(songs_router.router, prefix='/api/v1')
app.include_router(albums_router.router, prefix='/api/v1')
app.include_router(artists_router.router, prefix='/api/v1')
app.include_router(playlists_router.router, prefix='/api/v1')


@app.get("/api/health_check")
async def root():
    return {"message": "Hello World"}



