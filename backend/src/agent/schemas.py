from typing import List
from pydantic import BaseModel, Field

class SearchQueryList(BaseModel):
    query: List[str] = Field(
        description="A list of search queries to be used for web research."
    )