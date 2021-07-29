from pydantic import BaseModel
from typing import List, Optional


class SentaTextList(BaseModel):
    text: List[str]