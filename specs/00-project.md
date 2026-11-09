# Project spec

> Your team writes this file together in the first week. It's the spec every
> feature spec builds on, and the AI reads it before building any feature.
> Replace every section below; delete these quoted instructions when done.

## Topic

What the app is for, in two or three sentences.

## Users

Who uses the app and what each kind of user needs to do.

| User | Needs to |
|---|---|
| | |

## Database schema

Your tables, their columns (with types and limits), keys and foreign keys.
Put the `CREATE TABLE` statements in `sql/schema.sql` and summarize them here.
Note which tables are read-only lookups and which the app changes.

## Scope

What the finished app will do, and what it deliberately won't.

## Features

Each feature is a slice of the app that one student owns from spec to
working, tested code. Every student owns at least two: at least one that
changes data (add, edit, delete) and at least one that reads or reports.

| # | Feature | Owner | Reviewer | Spec |
|---|---|---|---|---|
| 00 | Foundation: connect to our schema, navigation, home page | | | [00-foundation](features/00-foundation.md) |
| 01 | | | | |
| 02 | | | | |

Owner and Reviewer are school emails, matching each student's git config.

## Shared rules

Decisions every feature follows, beyond those in `CLAUDE.md`. For example:
how names are displayed, date formats, what every list page shows.
