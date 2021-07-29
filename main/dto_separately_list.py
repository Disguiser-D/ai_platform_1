from pydantic import BaseModel
from typing import List


class SeparatelyTextList(BaseModel):
    text: List[str]
