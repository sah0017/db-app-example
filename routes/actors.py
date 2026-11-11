# Feature: Manage actors (spec: specs/features/01-actors.md)
# List, add and delete actors, plus a JSON list of actors with their films.

from flask import Blueprint, flash, redirect, render_template, request, url_for
from models import Actor, ActorInfo

# A Blueprint is a group of routes for one feature. 'actors' is its name,
# so url_for('actors.get_actors') builds the URL of get_actors below.
bp = Blueprint('actors', __name__)

# The link to this feature shown on every page: (label, endpoint)
NAV_LINK = ('Actors', 'actors.get_actors')

# sakila's actor.first_name and actor.last_name are VARCHAR(45)
MAX_NAME_LENGTH = 45

# ROUTE TO LIST ALL ACTORS
@bp.route('/get_actors')
def get_actors():
    actors = Actor.get_actors()
    return render_template('actors/list.html', actors=actors)

# ROUTE TO RENDER FORM TO ADD ACTOR DATA
@bp.route('/add_actor')
def add_actor_form():
    return render_template('actors/add.html', max_name_length=MAX_NAME_LENGTH)

# ROUTE TO CALL FUNCTION TO ADD ACTOR
@bp.route('/add', methods=["POST"])
def add_actor():

    # In this function we will input data from the
    # form page and store it in our database.
    # Remember that inside the get the name should
    # exactly be the same as that in the html
    # input fields
    first_name = (request.form.get("first_name") or "").strip()
    last_name = (request.form.get("last_name") or "").strip()

    # Send the user back to the form with a message if the input is invalid.
    # The '.' in '.add_actor_form' means "in this blueprint".
    if not first_name or not last_name:
        flash("Please enter both a first name and a last name.")
        return redirect(url_for('.add_actor_form'))
    if len(first_name) > MAX_NAME_LENGTH or len(last_name) > MAX_NAME_LENGTH:
        flash(f"Names can be at most {MAX_NAME_LENGTH} characters long.")
        return redirect(url_for('.add_actor_form'))

    # call model function that will store data as a row in our datatable
    Actor.add_actor(first_name, last_name)
    return redirect(url_for('.get_actors'))

# ROUTE TO CALL FUNCTION TO DELETE ACTOR
# POST only, so following a link or loading an image can't delete data
@bp.route('/delete/<int:id>', methods=["POST"])
def delete_actor(id):
    # Deletes the data on the basis of unique id and
    # redirects to actor page
    if not Actor.delete_actor(id):
        flash(f"Actor {id} can't be deleted because they appear in one or more films.")
    return redirect(url_for('.get_actors'))

# ROUTE TO CALL FUNCTION TO RETRIEVE AND RETURN ACTOR INFO
@bp.route('/actor_info')
def get_actor_info():
    return ActorInfo.get_actor_info()
