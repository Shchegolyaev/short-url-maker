from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.db import Base


class UrlInfo(Base):
    __tablename__ = "urlinfo"

    id = Column(Integer, primary_key=True)
    url_id = Column(String, unique=True)
    long_url = Column(String, unique=True, nullable=False)
    deleted = Column(Boolean, unique=False, default=False)
    redirects = relationship("Redirect")


class Redirect(Base):
    __tablename__ = "redirect"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    person_info = Column(String)
    url_info_id = Column(ForeignKey("urlinfo.id"))
    url_info = relationship("UrlInfo", back_populates="redirects")
