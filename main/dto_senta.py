from pydantic import BaseModel


class SentaText(BaseModel):
    text: str
