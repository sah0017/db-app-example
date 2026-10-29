import os
import secrets

from core import app
from flask import abort, flash, redirect, request, session, url_for
from flask.templating import render_template
from models import Actor, ActorInfo

# sakila's actor.first_name and actor.last_name are VARCHAR(45)
MAX_NAME_LENGTH = 45

# Every form includes a token from the user's session, so a POST
# sent from another website (which can't read the token) is rejected
@app.context_processor
def add_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return {'csrf_token': session['csrf_token']}

@app.before_request
def check_csrf_token():
    if request.method == 'POST':
        expected = session.get('csrf_token', '')
        submitted = request.form.get('csrf_token', '')
        if not expected or not secrets.compare_digest(expected, submitted):
            abort(400, "This form has expired. Go back, reload the page and try again.")

# A decorator used to tell the application
# which URL is associated with which function
@app.route('/hello')
def hello():
    return 'HELLO'

# APP ROUTE TO GET RESULTS FOR SELECT QUERY
@app.route('/get_actors')
def get_results():
    actors = Actor.get_actors()
    return actors

# APP ROUTE TO RENDER HOME PAGE WITH LIST OF ACTORS
@app.route('/')
def index():
    # Query all data and then pass it to the template
    actors = Actor.get_actors()
    return render_template('index.html', actors=actors)

# APP ROUTE TO RENDER FORM TO ADD ACTOR DATA
@app.route('/add_data')
def add_data():
    return render_template('add_actor.html', max_name_length=MAX_NAME_LENGTH)

# APP ROUTE TO CALL FUNCTION TO ADD ACTOR
@app.route('/add', methods=["POST"])
def add_actor():

    # In this function we will input data from the
    # form page and store it in our database.
    # Remember that inside the get the name should
    # exactly be the same as that in the html
    # input fields
    first_name = (request.form.get("first_name") or "").strip()
    last_name = (request.form.get("last_name") or "").strip()

    # Send the user back to the form with a message if the input is invalid
    if not first_name or not last_name:
        flash("Please enter both a first name and a last name.")
        return redirect(url_for('add_data'))
    if len(first_name) > MAX_NAME_LENGTH or len(last_name) > MAX_NAME_LENGTH:
        flash(f"Names can be at most {MAX_NAME_LENGTH} characters long.")
        return redirect(url_for('add_data'))

    # call model function that will store data as a row in our datatable
    Actor.add_actor(first_name, last_name)
    return redirect(url_for('index'))

# APP ROUTE TO CALL FUNCTION TO DELETE ACTOR
# POST only, so following a link or loading an image can't delete data
@app.route('/delete/<int:id>', methods=["POST"])
def delete_actor(id):
    # Deletes the data on the basis of unique id and
    # redirects to home page
    if not Actor.delete_actor(id):
        flash(f"Actor {id} can't be deleted because they appear in one or more films.")
    return redirect(url_for('index'))

# APP ROUTE TO CALL FUNCTION TO RETRIEVE AND RETURN ACTOR INFO
@app.route('/actor_info')
def get_actor_info():
    return ActorInfo.get_actor_info()

if __name__=='__main__':
    # The debugger lets anyone who sees an error page run code, so it is
    # off unless FLASK_DEBUG=1 is set (for example in .env)
    app.run(port=8000, debug=os.environ.get('FLASK_DEBUG') == '1')

