---
feature: Manage actors
owner: sahammond@lipscomb.edu
status: done
paths:
  - routes/actors.py
  - models/Actor.py
  - models/ActorInfo.py
  - templates/actors/*
  - tests/test_actors.py
---

# 01. Manage actors

> **Example spec.** This describes the actor feature that already exists in
> the starter code. Compare it with `routes/actors.py`, `models/Actor.py`,
> `templates/actors/` and `tests/test_actors.py` to see how each part of a
> spec turns into code and tests.

## Goal

As a **store manager**, I want **to see, add and remove actors** so that
**the actor list matches the films we carry**.

## Data

| Table | Columns used | Read / write |
|---|---|---|
| `actor` | `actor_id` (key), `first_name` `VARCHAR(45)` required, `last_name` `VARCHAR(45)` required, `last_update` | read and write |
| `actor_info` (view) | `actor_id`, `first_name`, `last_name`, `film_info` | read only |

`film_actor.actor_id` is a foreign key to `actor`, so MySQL refuses to delete
an actor who appears in a film. No schema changes.

## Pages and routes

| URL | Method | What it does |
|---|---|---|
| `/get_actors` | GET | Lists every actor: ID, first name, last name, last update, and a Delete button |
| `/add_actor` | GET | Form with First Name and Last Name, both required, at most 45 characters |
| `/add` | POST | Adds the actor, then returns to `/get_actors` |
| `/delete/<id>` | POST | Deletes the actor, then returns to `/get_actors` |
| `/actor_info` | GET | JSON list of actors with the films they appear in |

The Delete button asks "Delete *first last*?" before sending. The navigation
bar gets an **Actors** link to `/get_actors`.

## Acceptance criteria

1. **Given** any page, **when** it loads, **then** the navigation bar links to `/get_actors`.
2. **Given** the actors page, **when** it loads, **then** it lists the stock sakila actors (for example PENELOPE GUINESS).
3. **Given** the add form, **when** a first and last name are submitted, **then** one actor with those names is added and the user is sent to `/get_actors`.
4. **Given** the add form, **when** either name is blank or only spaces, **then** no actor is added and the form shows "Please enter both a first name and a last name."
5. **Given** the add form, **when** either name is longer than 45 characters, **then** no actor is added and the form shows "Names can be at most 45 characters long."
6. **Given** an actor who appears in no films, **when** Delete is pressed, **then** the actor is removed and the user returns to `/get_actors`.
7. **Given** an actor who appears in a film, **when** Delete is pressed, **then** the actor is kept and the page shows "Actor *id* can't be deleted because they appear in one or more films."
8. **Given** an actor ID that doesn't exist, **when** a delete is sent, **then** the response is 404 Not Found.
9. **Given** a GET request to `/delete/<id>`, **then** the response is 405 Method Not Allowed and nothing is deleted.
10. **Given** a POST with a missing or wrong `csrf_token`, **then** the response is 400 and nothing changes.

## Validation and errors

| Situation | What happens | Message shown |
|---|---|---|
| Blank first or last name | Back to the form, nothing saved | Please enter both a first name and a last name. |
| Name over 45 characters | Back to the form, nothing saved | Names can be at most 45 characters long. |
| Actor appears in a film | Back to the list, actor kept | Actor *id* can't be deleted because they appear in one or more films. |
| No such actor | 404 Not Found | (Flask's standard page) |

Names are trimmed of spaces at the start and end before they're checked and saved.

## Out of scope

- Editing an actor's name.
- Adding or removing an actor's films.
- Searching or paging the actor list.

## Test data and cleanup

Every actor a test adds has the last name `PYTEST-TEMP`, and the test appends
its `actor_id` to the `created_actor_ids` fixture, which deletes those actors
after the test.
