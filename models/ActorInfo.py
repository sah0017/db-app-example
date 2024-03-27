from models.schemas import ActorInfo
from core import ma, db

def get_actor_info():
     data = ActorInfo.query.all()
     return actors_info_schema.dump(data)

class ActorInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ActorInfo

actor_info_schema = ActorInfoSchema()
actors_info_schema = ActorInfoSchema(many=True)