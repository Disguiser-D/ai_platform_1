from pydantic import BaseModel

class DataExtractStr(BaseModel):
    text: str
    topK: int