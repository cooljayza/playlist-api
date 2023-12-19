from pydantic import BaseModel


class CreatePlaylistRequest(BaseModel):
    name: str


class CreatePlaylistResponse(CreatePlaylistRequest):
    id: int
