from uuid import uuid4

import pytest
from sqlalchemy import delete, func, select, text

from conftest import CSRF_TOKEN
from core import db
from models.schemas import Film
from routes.films import MAX_RELEASE_YEAR, MAX_TITLE_LENGTH

# Every film a test adds has a title starting with this prefix
TEST_FILM_TITLE_PREFIX = "PYTEST-TEMP"

# Tests append the ID of each film they add; the films are
# deleted again once the test finishes, so the sakila data is unchanged
@pytest.fixture
def created_film_ids(app):
    film_ids = []
    yield film_ids
    db.session.rollback()
    if film_ids:
        db.session.execute(delete(Film).where(Film.film_id.in_(film_ids)))
        db.session.commit()

ENGLISH_LANGUAGE_ID = 1

def unique_title():
    # A new title each time, so a test can find exactly the film it added
    return f'{TEST_FILM_TITLE_PREFIX} {uuid4().hex[:12]}'

def count_films():
    return db.session.scalar(select(func.count()).select_from(Film))

def find_film_id(title):
    return db.session.scalar(select(Film.film_id).where(Film.title == title))

def film_form(**changes):
    # The data a filled-in add form would send; a test can change any field
    data = {
        'title': unique_title(),
        'description': 'Added by a test',
        'release_year': '2006',
        'language_id': str(ENGLISH_LANGUAGE_ID),
        'rating': 'PG',
        'csrf_token': CSRF_TOKEN,
    }
    data.update(changes)
    return data

# PAGES THAT ONLY READ DATA

def test_home_page_links_to_films(client):
    response = client.get('/')
    assert b'href="/get_films"' in response.data

def test_films_page_lists_films(client):
    # Look up a real film so we can check its title appears in the table
    title = db.session.scalar(select(Film.title).limit(1))

    response = client.get('/get_films')
    assert response.status_code == 200
    assert b'<h3>Films</h3>' in response.data
    assert title.encode() in response.data

def test_add_film_form_lists_languages(client):
    response = client.get('/add_film')
    assert response.status_code == 200
    assert b'English' in response.data

# ADDING A FILM

def test_add_film(csrf_client, created_film_ids):
    form = film_form()
    response = csrf_client.post('/add_film', data=form)
    film_id = find_film_id(form['title'])
    if film_id is not None:
        created_film_ids.append(film_id)

    # After adding, the user is sent to the list of films
    assert response.status_code == 302
    assert response.location.endswith('/get_films')
    film = db.session.get(Film, film_id)
    assert film.release_year == 2006
    assert film.language_id == ENGLISH_LANGUAGE_ID
    assert film.rating == 'PG'

def test_add_film_with_only_required_fields(csrf_client, created_film_ids):
    form = film_form(description='', release_year='', rating='')
    response = csrf_client.post('/add_film', data=form)
    film_id = find_film_id(form['title'])
    if film_id is not None:
        created_film_ids.append(film_id)

    assert response.status_code == 302
    film = db.session.get(Film, film_id)
    assert film.description is None
    assert film.release_year is None

def test_add_film_with_blank_title_is_rejected(csrf_client):
    film_count = count_films()
    response = csrf_client.post('/add_film', data=film_form(title='   '), follow_redirects=True)
    assert b'Please enter a title.' in response.data
    assert count_films() == film_count

def test_add_film_with_long_title_is_rejected(csrf_client):
    film_count = count_films()
    response = csrf_client.post('/add_film', data=film_form(title='A' * (MAX_TITLE_LENGTH + 1)),
                                follow_redirects=True)
    assert b'Titles can be at most' in response.data
    assert count_films() == film_count

def test_add_film_with_bad_release_year_is_rejected(csrf_client):
    film_count = count_films()
    for year in ['abc', '1900', str(MAX_RELEASE_YEAR + 1)]:
        response = csrf_client.post('/add_film', data=film_form(release_year=year),
                                    follow_redirects=True)
        assert b'Release year must be between' in response.data
    assert count_films() == film_count

def test_add_film_with_unknown_language_is_rejected(csrf_client):
    film_count = count_films()
    response = csrf_client.post('/add_film', data=film_form(language_id='9999'),
                                follow_redirects=True)
    assert b'Please choose a language from the list.' in response.data
    assert count_films() == film_count

def test_add_film_with_unknown_rating_is_rejected(csrf_client):
    film_count = count_films()
    response = csrf_client.post('/add_film', data=film_form(rating='XXX'), follow_redirects=True)
    assert b'Please choose a rating from the list.' in response.data
    assert count_films() == film_count

def test_add_film_without_csrf_token_is_rejected(csrf_client):
    film_count = count_films()
    form = film_form()
    del form['csrf_token']
    response = csrf_client.post('/add_film', data=form)
    assert response.status_code == 400
    assert count_films() == film_count

# DELETING A FILM

def test_delete_film(csrf_client, created_film_ids):
    film = Film(title=unique_title(), language_id=ENGLISH_LANGUAGE_ID, last_update=func.now())
    db.session.add(film)
    db.session.commit()
    created_film_ids.append(film.film_id)

    response = csrf_client.post(f'/delete_film/{film.film_id}', data={'csrf_token': CSRF_TOKEN})
    assert response.status_code == 302
    assert response.location.endswith('/get_films')
    assert find_film_id(film.title) is None

def test_delete_film_with_actors_shows_message(csrf_client):
    film_id = db.session.scalar(text("SELECT film_id FROM film_actor LIMIT 1"))

    response = csrf_client.post(f'/delete_film/{film_id}', data={'csrf_token': CSRF_TOKEN},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"can&#39;t be deleted" in response.data
    assert db.session.get(Film, film_id) is not None

def test_delete_missing_film_returns_404(csrf_client):
    missing_id = db.session.scalar(select(func.max(Film.film_id))) + 1000
    response = csrf_client.post(f'/delete_film/{missing_id}', data={'csrf_token': CSRF_TOKEN})
    assert response.status_code == 404

def test_delete_film_is_post_only(client):
    response = client.get('/delete_film/1')
    assert response.status_code == 405
