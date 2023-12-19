from typing import Generic, TypeVar, List
from pydantic import Field
from pydantic.generics import GenericModel


M = TypeVar('M')


class PaginatedResponse(GenericModel, Generic[M]):
    count: int = Field(description='Total number of items in the database')
    items: List[M] = Field(description='List of items returned in the response')
