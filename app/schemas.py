from pydantic import BaseModel
from typing import List, Optional

class Movie(BaseModel):
    title: str
    rating: float
    number: str
    directors: List[str]
    writers: List[str]
    cast: List[str]
    languages: List[str]
    genres: List[str]
    age_group: str
    series: bool
    length: str
    year: int   
    poster : str
    

class VerRequest(BaseModel):
    pwd : str
    
class MovieUpdate(BaseModel):
    input : str
    
class MovieUpdateResponse(BaseModel):
    movies : List[str]