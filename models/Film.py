from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from models.schemas import Film
from core import ma, db

def get_films():
    all_films = db.session.scalars(select(Film).order_by(Film.film_id)).all()
    return films_schema.dump(all_films)

def add_film(title, description, release_year, language_id, rating):
    f = Film(title=title, description=description, release_year=release_year,
             language_id=language_id, rating=rating, last_update=func.now())
    db.session.add(f)
    db.session.commit()

def delete_film(id):
    # Deletes the data on the basis of unique id.
    # Responds with 404 Not Found if there is no such film.
    # Returns False if the film is still referenced by other
    # tables (film_actor, film_category or inventory), since MySQL
    # blocks that delete.
    data = db.get_or_404(Film, id)
    db.session.delete(data)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return True

class FilmSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Film
        # include language_id in the output (foreign keys are left out by default)
        include_fk = True

film_schema = FilmSchema()
films_schema = FilmSchema(many=True)
