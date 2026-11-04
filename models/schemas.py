from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from core import db

# Models
class Actor(db.Model):

    actor_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(45))
    last_name: Mapped[str] = mapped_column(String(45))
    last_update: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"Actor(actor_id={self.actor_id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"

class ActorInfo(db.Model):

    actor_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(45))
    last_name: Mapped[str] = mapped_column(String(45))
    film_info: Mapped[Optional[str]] = mapped_column(String(255))

    def __repr__(self):
        return f"ActorInfo(actor_id={self.actor_id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"

# sakila's film table has more columns than this (rental_rate,
# special_features, ...). Columns we don't list here are left out of
# our queries, and MySQL fills in their default values when we add a film.
class Film(db.Model):

    film_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[Optional[str]] = mapped_column(Text)
    release_year: Mapped[Optional[int]]
    language_id: Mapped[int] = mapped_column(ForeignKey("language.language_id"))
    # In MySQL this is an ENUM; app.py checks the value against FILM_RATINGS
    rating: Mapped[Optional[str]] = mapped_column(String(5))
    last_update: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"Film(film_id={self.film_id!r}, title={self.title!r})"

# Every film must have a language, so the add form lists these
class Language(db.Model):

    language_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))

    def __repr__(self):
        return f"Language(language_id={self.language_id!r}, name={self.name!r})"
