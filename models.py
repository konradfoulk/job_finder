from enum import Enum
from pydantic import BaseModel


class Experience(str, Enum):
    entry = 'entry'
    mid = 'mid'
    senior = 'senior'


class AiResponse(BaseModel):
    remote: bool
    experience: Experience
