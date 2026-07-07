---
id: pub-20260707-ingest-minimum
created: 2026-07-07
type: ingest-rule
status: experimental
---

# Ingest Minimum

During the experimental phase, PUNNARAJ records should start with the smallest useful structure.

```yaml
id:
created:
```

## Why only two fields?

`id` allows the record to be referenced.

`created` allows the record to be placed in history.

Without `id`, the system cannot link reliably.

Without `created`, the system cannot preserve historical sequence.

## When should a new field be added?

A new field should be added only when repeated real use creates pressure that `id` and `created` cannot handle.

Examples:

- repeated source confusion → consider `source`
- repeated revision confusion → consider `updated` or `revision`
- repeated fact/opinion confusion → consider `type`
- repeated uncertainty → consider `confidence`
- repeated sensitivity decisions → consider `sensitivity`
- repeated relationship tracking → consider `links`

## Rule

Structure must earn its existence.

Every new field, rule, template, or service should be able to explain:

- why it emerged
- what problem it solves
- whether it improves efficiency
- whether it reduces ambiguity
- whether it adds unnecessary friction
- when it should be revised or removed

## Status

This is an experimental rule. It should be changed only when real records prove that a change improves the system.
