import os
import secrets

from core import app
from flask import abort, flash, redirect, request, session, url_for
from flask.templating import render_template
from models import Actor, ActorInfo, Film, Language, Queries

# sakila's actor.first_name and actor.last_name are VARCHAR(45)
MAX_NAME_LENGTH = 45

# sakila's film.title is VARCHAR(128) and film.release_year is a MySQL
# YEAR column, which only holds 1901 to 2155
MAX_TITLE_LENGTH = 128
MIN_RELEASE_YEAR = 1901
MAX_RELEASE_YEAR = 2155

# The only values sakila's film.rating ENUM column accepts
FILM_RATINGS = ['G', 'PG', 'PG-13', 'R', 'NC-17']

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

# APP ROUTE TO RENDER HOME PAGE 
@app.route('/')
def index():
    return render_template('index.html')

# APP ROUTE TO GET RESULTS FOR SELECT QUERY
@app.route('/get_actors')
def get_actors():
    actors = Actor.get_actors()
    return render_template('actors.html', actors=actors)
    


# APP ROUTE TO RENDER FORM TO ADD ACTOR DATA
@app.route('/add_actor')
def add_actor_form():
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
        return redirect(url_for('add_actor_form'))
    if len(first_name) > MAX_NAME_LENGTH or len(last_name) > MAX_NAME_LENGTH:
        flash(f"Names can be at most {MAX_NAME_LENGTH} characters long.")
        return redirect(url_for('add_actor_form'))

    # call model function that will store data as a row in our datatable
    Actor.add_actor(first_name, last_name)
    return redirect(url_for('get_actors'))

# APP ROUTE TO CALL FUNCTION TO DELETE ACTOR
# POST only, so following a link or loading an image can't delete data
@app.route('/delete/<int:id>', methods=["POST"])
def delete_actor(id):
    # Deletes the data on the basis of unique id and
    # redirects to actor page
    if not Actor.delete_actor(id):
        flash(f"Actor {id} can't be deleted because they appear in one or more films.")
    return redirect(url_for('get_actors'))

# APP ROUTE TO LIST ALL FILMS
@app.route('/get_films')
def get_films():
    films = Film.get_films()
    return render_template('films.html', films=films)

# APP ROUTE TO RENDER FORM TO ADD FILM DATA
@app.route('/add_film')
def add_film_form():
    return render_template('add_film.html',
                           languages=Language.get_languages(),
                           ratings=FILM_RATINGS,
                           max_title_length=MAX_TITLE_LENGTH,
                           min_release_year=MIN_RELEASE_YEAR,
                           max_release_year=MAX_RELEASE_YEAR)

# APP ROUTE TO CALL FUNCTION TO ADD FILM
# Same URL as the form, but this function only handles POST
@app.route('/add_film', methods=["POST"])
def add_film():
    title = (request.form.get("title") or "").strip()
    # An empty description is stored as NULL rather than ''
    description = (request.form.get("description") or "").strip() or None
    release_year = (request.form.get("release_year") or "").strip()
    language_id = (request.form.get("language_id") or "").strip()
    rating = request.form.get("rating") or None

    # Send the user back to the form with a message if the input is invalid
    if not title:
        flash("Please enter a title.")
        return redirect(url_for('add_film_form'))
    if len(title) > MAX_TITLE_LENGTH:
        flash(f"Titles can be at most {MAX_TITLE_LENGTH} characters long.")
        return redirect(url_for('add_film_form'))

    # Release year is optional, but if given it must be a whole number
    # that fits in MySQL's YEAR column
    if release_year:
        if not release_year.isdigit() or not MIN_RELEASE_YEAR <= int(release_year) <= MAX_RELEASE_YEAR:
            flash(f"Release year must be between {MIN_RELEASE_YEAR} and {MAX_RELEASE_YEAR}.")
            return redirect(url_for('add_film_form'))
        release_year = int(release_year)
    else:
        release_year = None

    # The form's dropdowns only offer valid choices, but a request
    # can be sent without using the form, so check them here too
    if not language_id.isdigit() or not Language.language_exists(int(language_id)):
        flash("Please choose a language from the list.")
        return redirect(url_for('add_film_form'))
    if rating is not None and rating not in FILM_RATINGS:
        flash("Please choose a rating from the list.")
        return redirect(url_for('add_film_form'))

    # call model function that will store data as a row in our datatable
    Film.add_film(title, description, release_year, int(language_id), rating)
    return redirect(url_for('get_films'))

# APP ROUTE TO CALL FUNCTION TO DELETE FILM
# POST only, so following a link or loading an image can't delete data
@app.route('/delete_film/<int:id>', methods=["POST"])
def delete_film(id):
    # Deletes the data on the basis of unique id and
    # redirects to film page
    if not Film.delete_film(id):
        flash(f"Film {id} can't be deleted because it has actors, categories or rental inventory.")
    return redirect(url_for('get_films'))

# APP ROUTE TO RENDER PAGE LISTING THE QUERIES
@app.route('/get_queries')
def get_queries():
    return render_template('queries.html')

# APP ROUTE TO SHOW THE TOP 5 CUSTOMERS BY AMOUNT SPENT
@app.route('/queries/top_customers')
def top_customers():
    customers = Queries.get_top5custs()
    return render_template('top_customers.html', customers=customers)

# APP ROUTE TO SHOW RENTAL AND REVENUE TOTALS FOR EACH STORE
@app.route('/queries/store_rentals')
def store_rentals():
    stores = Queries.get_avg_rental()
    return render_template('store_rentals.html', stores=stores)

# APP ROUTE TO CALL FUNCTION TO RETRIEVE AND RETURN ACTOR INFO
@app.route('/actor_info')
def get_actor_info():
    return ActorInfo.get_actor_info()

if __name__=='__main__':
    # The debugger lets anyone who sees an error page run code, so it is
    # off unless FLASK_DEBUG=1 is set (for example in .env)
    app.run(port=8000, debug=os.environ.get('FLASK_DEBUG') == '1')

