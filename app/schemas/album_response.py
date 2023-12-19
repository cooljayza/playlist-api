from pydantic import BaseModel


class AlbumResponse(BaseModel):
    title: str
    year: int
    id: int

