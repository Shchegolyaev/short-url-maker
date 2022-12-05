from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

# Импортируем базовый класс для моделей.
from db.db import Base


class UrlData(Base):
    __tablename__ = "UrlData"
    id = Column(Integer, primary_key=True)
    url_id = Column(String, unique=True)
    long_url = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
