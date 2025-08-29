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

class BatchParseRequest(BaseModel):
    job_text: str = Field(min_length=10)
    resumes: List[str] = Field(min_items=1, max_items=200)

class BatchParseResult(BaseModel):
    items: List[ParseResult]
