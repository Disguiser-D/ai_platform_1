from pydantic import BaseModel
from typing import List, Optional

class DataFenciList(BaseModel):
    text: List[str]
    mode: str