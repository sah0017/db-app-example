from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from core import db

# Models
class Actor(db.Model):

    actor_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    last_update: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"Actor(actor_id={self.actor_id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"

class ActorInfo(db.Model):

    actor_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    film_info: Mapped[Optional[str]] = mapped_column(String(255))

    def __repr__(self):
        return f"ActorInfo(actor_id={self.actor_id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"
