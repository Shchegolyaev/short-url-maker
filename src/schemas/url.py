from pydantic import BaseModel


class UrlDataBase(BaseModel):
    long_url: str
