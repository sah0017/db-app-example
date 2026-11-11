# Specifications

This project is built with **specification-driven development**: you write
specs, and an AI coding assistant writes the code from them. The specs are
the source of truth. When the app does the wrong thing, fix the spec and have
the AI regenerate the code, rather than editing the code by hand.

| File | What it is |
|---|---|
| `00-project.md` | The team's project spec: topic, users, schema, and the list of features with their owners |
| `feature-template.md` | The template to copy for each new feature |
| `features/NN-name.md` | One spec per feature, numbered to match the list in `00-project.md` |
| `features/01-actors.md` | An example spec for the starter app's actor feature |

## The header of a feature spec

Every feature spec starts with a header between `---` lines:

```
---
feature: Manage actors
owner: you@mail.lipscomb.edu
status: draft
paths:
  - routes/actors.py
  - templates/actors/*
  - tests/test_actors.py
---
```

- `owner` is the email in your git config, so the course's stats tool can
  match the feature to the commits that built it.
- `status` moves from `draft` to `approved` (spec reviewed and merged) to
  `building` to `done` (code reviewed and merged).
- `paths` lists every file the feature creates or changes. The AI should only
  change these files. `*` matches any file name.

## Asking the AI to build a feature

From the project folder, on your feature branch, ask your AI assistant:

> Implement `specs/features/NN-name.md`. Read `specs/00-project.md` and
> `CLAUDE.md` first. Write a test for every acceptance criterion before
> writing the code, then make all the tests pass. Only change the files listed
> in the spec's `paths`. If anything in the spec is unclear, ask me instead of
> guessing.
