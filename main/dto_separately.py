from pydantic import BaseModel


class SeparatelyText(BaseModel):
    text: str
