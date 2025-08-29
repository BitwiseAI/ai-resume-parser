from pydantic import BaseModel, Field
from typing import List

class ParseResult(BaseModel):
    skills: List[str]
    score: int = Field(ge=0, le=100)
    reasons: str
