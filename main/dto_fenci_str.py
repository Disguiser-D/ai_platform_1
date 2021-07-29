from pydantic import BaseModel

class DataFenciStr(BaseModel):
    text: str
    mode: str