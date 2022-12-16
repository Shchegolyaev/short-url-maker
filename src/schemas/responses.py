from pydantic import BaseModel


class RespMakeShort(BaseModel):
    short_url: str


class RespRedirect(BaseModel):
    long_url: str


class RespStats(BaseModel):
    stats: dict


class RespCheckDb(BaseModel):
    status: str


class DelUrl(BaseModel):
    deleted: str
