# Feature: Manage films
# List, add and delete films.

from flask import Blueprint, flash, redirect, render_template, request, url_for
from models import Film, Language

bp = Blueprint('films', __name__)

# The link to this feature shown on every page: (label, endpoint)
NAV_LINK = ('Films', 'films.get_films')

# sakila's film.title is VARCHAR(128) and film.release_year is a MySQL
# YEAR column, which only holds 1901 to 2155
MAX_TITLE_LENGTH = 128
MIN_RELEASE_YEAR = 1901
MAX_RELEASE_YEAR = 2155

# The only values sakila's film.rating ENUM column accepts
FILM_RATINGS = ['G', 'PG', 'PG-13', 'R', 'NC-17']

# ROUTE TO LIST ALL FILMS
@bp.route('/get_films')
def get_films():
    films = Film.get_films()
    return render_template('films/list.html', films=films)

# ROUTE TO RENDER FORM TO ADD FILM DATA
@bp.route('/add_film')
def add_film_form():
    return render_template('films/add.html',
                           languages=Language.get_languages(),
                           ratings=FILM_RATINGS,
                           max_title_length=MAX_TITLE_LENGTH,
                           min_release_year=MIN_RELEASE_YEAR,
                           max_release_year=MAX_RELEASE_YEAR)

# ROUTE TO CALL FUNCTION TO ADD FILM
# Same URL as the form, but this function only handles POST
@bp.route('/add_film', methods=["POST"])
def add_film():
    title = (request.form.get("title") or "").strip()
    # An empty description is stored as NULL rather than ''
    description = (request.form.get("description") or "").strip() or None
    # MySQL TEXT can hold at most 65,535 bytes, not characters.
    if description is not None and len(description.encode("utf-8")) > 65535:
        flash("Description is too long. Please use less text.")
        return redirect(url_for('.add_film_form'))
    release_year = (request.form.get("release_year") or "").strip()
    language_id = (request.form.get("language_id") or "").strip()
    rating = request.form.get("rating") or None

    # Send the user back to the form with a message if the input is invalid
    if not title:
        flash("Please enter a title.")
        return redirect(url_for('.add_film_form'))
    if len(title) > MAX_TITLE_LENGTH:
        flash(f"Titles can be at most {MAX_TITLE_LENGTH} characters long.")
        return redirect(url_for('.add_film_form'))

    # Release year is optional, but if given it must be a whole number
    # that fits in MySQL's YEAR column
    if release_year:
        try:
            release_year = int(release_year) if release_year.isdigit() else None
        except ValueError:
            release_year = None
        if release_year is None or not MIN_RELEASE_YEAR <= release_year <= MAX_RELEASE_YEAR:
            flash(f"Release year must be between {MIN_RELEASE_YEAR} and {MAX_RELEASE_YEAR}.")
            return redirect(url_for('.add_film_form'))
    else:
        release_year = None

    # The form's dropdowns only offer valid choices, but a request
    # can be sent without using the form, so check them here too
    try:
        language_id = int(language_id) if language_id.isdigit() else None
    except ValueError:
        language_id = None
    if language_id is None or not Language.language_exists(language_id):
        flash("Please choose a language from the list.")
        return redirect(url_for('.add_film_form'))
    if rating is not None and rating not in FILM_RATINGS:
        flash("Please choose a rating from the list.")
        return redirect(url_for('.add_film_form'))

    # call model function that will store data as a row in our datatable
    Film.add_film(title, description, release_year, int(language_id), rating)
    return redirect(url_for('.get_films'))

# ROUTE TO CALL FUNCTION TO DELETE FILM
# POST only, so following a link or loading an image can't delete data
@bp.route('/delete_film/<int:id>', methods=["POST"])
def delete_film(id):
    # Deletes the data on the basis of unique id and
    # redirects to film page
    if not Film.delete_film(id):
        flash(f"Film {id} can't be deleted because it has actors, categories or rental inventory.")
    return redirect(url_for('.get_films'))
