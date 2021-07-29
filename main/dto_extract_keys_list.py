from pydantic import BaseModel
from typing import List

class DataExtractList(BaseModel):
    text: List[str]
    topK: int