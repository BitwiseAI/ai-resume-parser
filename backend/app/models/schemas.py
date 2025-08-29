from pydantic import BaseModel, Field
from typing import List, Optional

class ParseRequest(BaseModel):
    resume_text: str = Field(min_length=10)
    job_text: str = Field(min_length=10)
    model: Optional[str] = None
    temperature: Optional[float] = None

class ParseResult(BaseModel):
    skills: List[str]
    score: int = Field(ge=0, le=100)
    reasons: str
