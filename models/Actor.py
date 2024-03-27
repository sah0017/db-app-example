
from sqlalchemy import func
from models.schemas import Actor
from core import ma, db

def get_actors(): 
    all_actors = Actor.query.all()
    return actors_schema.dump(all_actors)

def add_actor(first_name, last_name):
    a = Actor(first_name=first_name, last_name=last_name, last_update=func.now())
    db.session.add(a)
    db.session.commit()

def delete_actor(id):
	# Deletes the data on the basis of unique id and 
	# redirects to home page
	data = Actor.query.get(id)
	db.session.delete(data)
	db.session.commit()
     
class ActorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Actor

actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)

