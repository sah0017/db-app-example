# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A small teaching Flask app (course example) that reads and writes actor and film data in the MySQL `sakila` sample database. Code is intentionally simple and heavily commented for students; keep that style and keep README.md's step-by-step setup instructions accurate for beginners on macOS and Windows when changing setup or configuration.

## Specification-driven development

Students build this project by writing specs in `specs/` and asking an AI assistant to implement them. **The specs are the source of truth.**

- Before implementing a feature, read `specs/00-project.md` and the feature's spec in `specs/features/`.
- Write a test for every acceptance criterion first, with a comment naming it (`# AC3`), then write the code that makes the tests pass.
- Only create or change the files listed in the spec's `paths` header. If the feature seems to need another file changed (for example `models/schemas.py` or another feature's files), stop and say so, so the spec can be updated.
- Build only what the spec describes. Don't add features, pages or fields it doesn't mention, and don't implement anything listed under "Out of scope".
- If the spec is ambiguous or contradicts this file, ask the student instead of guessing. Suggest the exact wording to add to the spec.
- When the student reports a bug, check the spec first. If the spec allows the wrong behavior, propose a spec change before changing code.
- Never change git configuration or commit as anyone other than the student running you.

## Commands

```
source venv/bin/activate          # required; the app exits if not in a venv
pip install -r requirements.txt   # versions are pinned
python app.py                     # serves http://127.0.0.1:8000
pytest                            # run all tests
pytest tests/test_actors.py::test_add_actor   # run one test
```

There is no linter or build step. After adding a package, regenerate `requirements.txt` with `pip freeze > requirements.txt` from inside the venv.

## Tests

pytest with Flask's `test_client()`; `pytest.ini` sets `pythonpath = .` so tests import `app`, `core`, `models`, `routes` directly. Each feature has its own test file, `tests/test_<feature>.py`. Tests run against the real MySQL database from `.env` (not SQLite: the models map onto sakila's existing tables and the `actor_info` view, and delete behaviour relies on MySQL's foreign keys from `film_actor`, `film_category` and `inventory`). Shared fixtures in `tests/conftest.py` (only fixtures every feature needs belong there):
- `app` pushes an app context; `client` is a Flask test client.
- `csrf_client` pre-seeds the session with `CSRF_TOKEN`; POSTs must send it as the `csrf_token` form field or they get a 400.

Feature-specific fixtures live in the feature's own test file. Every test must delete any rows it adds, following the pattern in `tests/test_actors.py`: a `created_actor_ids` fixture yields a list, the test appends the ID of each actor it adds (with last name `TEST_LAST_NAME`), and teardown deletes them. `tests/test_films.py` does the same with `created_film_ids` and `TEST_FILM_TITLE_PREFIX`. Count assertions compare against a count taken at the start of the test rather than assuming zero.

Configuration comes from `.env` (git-ignored): `PASSWORD` (required; the app exits with a message if missing), optional `DB_USER` (default `root`), `DB_NAME` (default `sakila`), and `FLASK_DEBUG=1` to enable the reloader/debugger. Host and port (`127.0.0.1:3306`) are hard-coded in `db_cred` in `core/__init__.py`. Running requires a local MySQL with sakila installed.

## Architecture

- `core/__init__.py` does all setup at import time, in this order: virtualenv check (must stay before any third-party imports), `.env` loading and validation, Flask app creation (`template_folder="../templates"`), DB URI via `sqlalchemy.URL.create` (escapes special characters in the password), and the `db` (Flask-SQLAlchemy, SQLAlchemy 2.0 `DeclarativeBase`) and `ma` (Marshmallow) instances. Everything else imports `app`, `db`, `ma` from `core`.
- `models/schemas.py` holds the ORM classes, mapped onto existing sakila objects (no migrations or `create_all`). Table names come from Flask-SQLAlchemy's automatic CamelCase→snake_case naming: `Actor` → `actor` table, `Film` → `film`, `Language` → `language`, `ActorInfo` → the `actor_info` view (read-only). `Film` maps only some of `film`'s columns; the rest get MySQL defaults on insert, and `rating` is mapped as a string (MySQL ENUM) validated in `routes/films.py` against `FILM_RATINGS`.
- `models/Actor.py`, `models/Film.py`, `models/Language.py` and `models/ActorInfo.py` are per-entity data-access modules (no `models/__init__.py`; route modules import them as modules, e.g. `from models import Actor, ActorInfo`). Each defines query functions plus a `SQLAlchemyAutoSchema`; functions return schema-dumped dicts, so JSON routes can return them directly.
- `models/Queries.py` holds read-only reporting queries that join many tables; they use raw SQL via `text()` and return `.mappings().all()` (a list of dict-like rows) rather than a schema dump. Each has a route under `/queries/...` in `routes/queries.py` and its own template in `templates/queries/`, linked from the `/get_queries` page.
- `app.py` holds only what every feature shares: the CSRF hooks, the `nav_links` context processor and the home page (`/`). It calls `register_blueprints(app)` from `routes/__init__.py`, which imports every module in `routes/`, registers its Flask Blueprint `bp`, and collects its optional `NAV_LINK = (label, endpoint)`. **Adding a feature never requires editing `app.py`, `routes/__init__.py`, `templates/base.html` or `templates/index.html`.**
- Each feature has `routes/<feature>.py` (a Blueprint named after the feature, e.g. `bp = Blueprint('actors', __name__)`, plus its constants), its templates in `templates/<feature>/`, and `tests/test_<feature>.py`. Inside a blueprint, `url_for('.name')` refers to a route in the same blueprint; elsewhere use `url_for('<blueprint>.<name>')`.
- Every page template starts with `{% extends "base.html" %}` and puts its content in `{% block content %}` (and its page title in `{% block title %}`). `base.html` renders the navigation bar and flashed messages, so page templates don't. Use `url_for` for links and form actions, never hard-coded URLs.
- Conventions every feature follows:
  - Hand-rolled CSRF protection: a `context_processor` puts `csrf_token` into every template and a `before_request` hook rejects any POST without a matching `csrf_token` form field. Every new POST form must include `<input type="hidden" name="csrf_token" value="{{ csrf_token }}">`.
  - State-changing routes are POST-only; validation errors use `flash()` + redirect (templates render `get_flashed_messages()`).
  - Length/range constants mirror the column types and live in the feature's routes module: `MAX_NAME_LENGTH = 45` (`VARCHAR(45)`) in `routes/actors.py`; `MAX_TITLE_LENGTH = 128`, `MIN_RELEASE_YEAR`/`MAX_RELEASE_YEAR` (MySQL `YEAR`, 1901–2155) and `FILM_RATINGS` in `routes/films.py`.
  - `Actor.delete_actor` and `Film.delete_film` return `False` on `IntegrityError` (row still referenced by another table) so the route can flash a message instead of a 500; they use `db.get_or_404` for missing IDs. Every stock sakila film is referenced, so only films added through the app can actually be deleted.
  - Each entity has a list page (`/get_actors`, `/get_films`), a GET form page, a POST add route and a POST delete route; add and delete redirect back to the list page. URLs stay unprefixed (blueprints are registered without `url_prefix`), so routes in different features must not reuse a URL.
- `app.secret_key` is regenerated each run, so sessions/CSRF tokens don't survive a restart (intended for local use).
