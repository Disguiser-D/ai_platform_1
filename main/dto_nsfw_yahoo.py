from pydantic import BaseModel, ByteSize


class NSFW(BaseModel):
    image: str
