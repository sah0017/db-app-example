---
# Copy this file to specs/features/NN-short-name.md (NN = the feature's
# number in specs/00-project.md) and fill in every section. Delete these
# comment lines when you're done.
feature: Short feature name
owner: you@mail.lipscomb.edu        # the email in your git config
status: draft                       # draft -> approved -> building -> done
paths:                              # every file this feature creates or changes
  - routes/short_name.py
  - models/ShortName.py
  - templates/short_name/*
  - tests/test_short_name.py
---

# NN. Feature name

## Goal

As a **(kind of user)**, I want **(to do something)** so that **(reason)**.

One or two sentences on what this feature adds to the app.

## Data

Tables and columns this feature reads or writes. Say which columns are
required, their types and limits (for example `VARCHAR(45)`), and any
foreign keys. If the feature needs a schema change, give the exact SQL.

| Table | Columns used | Read / write |
|---|---|---|
| | | |

## Pages and routes

| URL | Method | What it does |
|---|---|---|
| | GET | |
| | POST | |

For each page, list what it shows and, for forms, every field (its label,
whether it's required and what values it accepts).

## Acceptance criteria

Numbered, testable statements in Given / When / Then form. Each one becomes
at least one test, and the test's comment names the criterion (`# AC3`).

1. **Given** ..., **when** ..., **then** ...
2. **Given** ..., **when** ..., **then** ...

## Validation and errors

What happens with bad or missing input, a record that doesn't exist, or a
delete that the database refuses. Give the exact message the user sees.

| Situation | What happens | Message shown |
|---|---|---|
| | | |

## Out of scope

What this feature does NOT do, so the AI doesn't build it (and doesn't
build another student's feature).

-

## Test data and cleanup

How tests create the rows they need and delete them afterwards, so the
database is left unchanged (see `created_actor_ids` in `tests/test_actors.py`).
