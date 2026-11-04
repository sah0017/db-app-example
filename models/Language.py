from sqlalchemy import select
from models.schemas import Language
from core import ma, db

def get_languages():
    data = db.session.scalars(select(Language).order_by(Language.name)).all()
    return languages_schema.dump(data)

def language_exists(id):
    return db.session.get(Language, id) is not None

class LanguageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Language

language_schema = LanguageSchema()
languages_schema = LanguageSchema(many=True)
