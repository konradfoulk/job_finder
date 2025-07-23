from enum import Enum
from pydantic import BaseModel


# enum for experience level to be passed to ai structured response
class Experience(str, Enum):
    entry = 'entry'
    mid = 'mid'
    senior = 'senior'


# response model for a consistent structured response from the OpenAI API
class AiResponse(BaseModel):
    remote: bool
    experience: Experience
