from pydantic import BaseModel, Field
from typing import Literal


Algorithm = Literal["fixed_window", "sliding_log", "sliding_counter", "token_bucket"]


class Rule(BaseModel):
    name: str
    algorithm: Algorithm
    limit: int = Field(gt=0)
    window_ms: int = Field(gt=0)

class CheckRequest(BaseModel):
    rule: str
    identifier: str = Field(min_length=1, max_length=256)
    cost: int = Field(default=1, ge=1)

class CheckResponse(BaseModel):
    allowed: bool
    remaining: int
    retry_after_ms: int
    limit: str
    rule: str