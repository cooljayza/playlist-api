from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, DateTime


class BaseModel(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.utcnow))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.utcnow,
                                 onupdate=datetime.utcnow))
