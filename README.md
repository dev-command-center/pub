---
id: pub-20260707-root
created: 2026-07-07
title: PUNNARAJ Public Mutual Understanding
type: project-root
version: 0.03
aliases:
  - PUNNARAJ
  - index
  - home_page
  - mutual_understanding
  - dev_command_center
---

# PUNNARAJ Public Mutual Understanding

This repository is a public, low-sensitivity working surface for PUNNARAJ shared understanding.

It is hosted under the GitHub organization currently named `dev-command-center`, which is treated as a development command center: a provider-hosted working area for coordination, public reference material, and low-sensitivity development scaffolds.

It is not the root of PUNNARAJ. It is not ZERO. It is not a final doctrine.

Purpose:

- keep a simple public page that humans and agents can inspect
- preserve current working meanings of key PUNNARAJ terms
- use plain files that can be moved, mirrored, rebuilt, or replaced
- avoid custom infrastructure until the structure proves useful

Current minimum record rule:

```yaml
id:
created:
```

Every extra field must earn its existence by solving a repeated real problem.

## Files

- `index.html` — public landing page / shared reference
- `docs/MUTUAL_UNDERSTANDING.md` — current mutual-understanding snapshot
- `docs/INGEST_MINIMUM.md` — minimum document/record rule
- `docs/OPERATING_MODEL.md` — current operating model summary
- `docs/ORG_IDENTITY.md` — current GitHub organization role and boundary
- `learning/index.html` — public learning root
- `learning/method/index.html` — learning method
- `learning/lessons/index.html` — public lesson index
- `learning/lessons/001-shared-understanding-discontinuity/index.html` — Lesson 001
- `learning/skills/index.html` — working-skill index
- `learning/skills/shared-understanding-gateway/index.html` — public skill evolution record
- `learning/measurement/index.html` — recurrence measures
- `learning/use-this-method/index.html` — reuse guide
- `.nojekyll` — lets static hosting serve files directly

## Learning from Work

`learning/` is a public, sanitized learning root. It turns observed work
failures into reusable lessons, changes to working skills, and recurrence
measures. It does not publish private journals, raw transcripts, account
identifiers, credentials, or private operational paths.

The first release contains Lesson 001 — Shared Understanding Discontinuity and
the public evolution record for `shared-understanding-gateway` version `0.1.0`.

Run the static-site contract before publication:

```bash
python3 -m unittest tests/test_learning_site.py -v
```

## Working stance

PUNNARAJ does not preserve fixed final truth. It preserves inspectable records, links, context, provenance, corrections, and the ability to revise understanding.

## Status

Experimental public scaffold. Safe to replace, revise, or archive if it stops being useful.
