from pydantic import BaseModel


class ArtistResponse(BaseModel):
    id: int
    name: str
