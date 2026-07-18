---
id: pub-20260718-learning-from-work-design
created: 2026-07-18
title: Learning from Work — Public Learning Root Design
type: design-specification
status: accepted
version: 0.1
decision_id: CG001-DJ-20260718T025541Z-002
---

# Learning from Work — Public Learning Root Design

## 1. Purpose

Create a public learning root that turns failures observed during real work into
reusable lessons, changes to working methods, and measurable evidence of
improvement.

The project does not claim to discover final truth. Its purpose is iterative
clarification: remove misunderstanding, reduce ambiguity, and sharpen a method
through repeated contact with evidence.

The guiding statement is:

> การทำผิดไม่ใช่ปัญหาที่ร้ายที่สุด การทำผิดแล้วไม่สร้างบทเรียนต่างหากที่ทำให้
> ความผิดเดิมกลับมาอีก เราไม่ได้หาความจริงสุดท้าย เราทำสิ่งที่เคยทื่อให้คมขึ้น
> ด้วยการลบความเข้าใจผิดและความกำกวม จนสิ่งที่ต้องการสื่อเด่นชัดขึ้น

Working English rendering:

> Making a mistake is not the worst failure. Failing to turn it into a lesson
> allows the same mistake to return. We are not searching for final truth; we
> sharpen what was blunt by removing misunderstanding and ambiguity until the
> meaning becomes clearer.

The English text is an explanatory rendering, not a replacement for the Thai
source statement.

## 2. Relationship to the Existing Public Page

The existing page remains the small public entry point for shared PUNNARAJ
understanding. It gains one clearly named path: **Learning from Work**.

The learning material lives under `/learning/`. It does not turn the home page
into a journal, a course catalog, or an operational dashboard. It is a sibling
public concern with its own navigation and explanatory context.

```text
Public home
└── Learning from Work
    ├── Why We Learn
    ├── How a Mistake Becomes a Lesson
    ├── Lessons
    ├── Skill Evolution
    ├── Measurement
    └── Use This Method
```

## 3. Audience and Reader Promise

The primary reader is a person or team that has experienced a recurring process
failure and wants a practical way to make recurrence less damaging.

The site promises that every published lesson will answer:

1. What failed?
2. How could someone detect it?
3. What working rule changed because of it?
4. How was the changed rule tested?
5. What will be measured if the problem returns?
6. What remains uncertain or incomplete?

The reader must not need access to private systems, private journals, or the
original conversation to understand or apply the method.

## 4. Information Architecture

### 4.1 `/learning/index.html` — Learning root

The root explains the sharpening model and gives a short map of the learning
cycle. It links to the method, published lessons, skill evolution, measurement,
and reuse guide.

The first viewport should establish three ideas without hype:

- mistakes are evidence;
- a lesson is a changed future gate, not merely a written memory;
- improvement means earlier detection, lower impact, or both.

### 4.2 `/learning/method/index.html` — How learning works

This page presents a repeatable cycle:

```text
work → observe failure → preserve evidence → extract lesson
     → change a working gate → pressure-test → measure recurrence → revise
```

Each stage explains its input, output, and stop condition. The cycle is
deliberately iterative. A lesson can be revised when later evidence reveals
ambiguity, excessive cost, or a weaker prevention rule.

### 4.3 `/learning/lessons/index.html` — Lesson registry

The registry lists lessons by stable ID, title, status, introduced version, and
last evidence state. Version numbers remain visible so later revisions do not
erase earlier understanding.

### 4.4 `/learning/lessons/001-shared-understanding-discontinuity/index.html`

The first lesson explains the failure in which work remains coherent inside an
agent's private context while the owner loses the causal path between shared
states.

It includes:

- failure description;
- observable signals;
- required prevention;
- recall question;
- pressure-test summary;
- measurement fields;
- current limitations;
- links to the affected skill version and the general method.

It excludes names, account identifiers, private Box paths, raw transcripts,
credentials, and private operational evidence.

### 4.5 `/learning/skills/index.html` — Skill evolution registry

This registry shows which working skills changed because of published lessons.
The first entry is `shared-understanding-gateway` version `0.1.0`.

### 4.6 `/learning/skills/shared-understanding-gateway/index.html`

The page explains the public behavior of the skill:

- 8-minute soft checkpoint;
- 10-minute hard stop;
- stop after 7 material steps;
- explicit lesson recall;
- decision readback before material action;
- separate outcome after action;
- recurrence measurement.

It also states the known limitation: version `0.1.0` defines a procedural timer
but does not yet include an independently interrupting alarm. Candidate changes
must remain candidates until a new version is tested and published.

### 4.7 `/learning/measurement/index.html` — Evidence of sharpening

This page defines the common measures and impact scale. It explains that a
later version is not automatically better because its number is higher.
Improvement requires evidence of earlier detection, reduced impact, less owner
reconstruction, or lower prevention cost without losing protection.

### 4.8 `/learning/use-this-method/index.html` — Reader reuse guide

The guide gives readers a minimal lesson template and an example workflow they
can adapt without adopting PUNNARAJ terminology or infrastructure.

## 5. Lesson Record Model

Every public lesson uses a stable record with these fields:

| Field | Purpose |
| --- | --- |
| Lesson ID | Stable address across revisions |
| Title | Human-readable failure name |
| Status | Proposed, active, superseded, or retired |
| Introduced version | First skill or method version changed by the lesson |
| Failure | Bounded description of what went wrong |
| Detection signals | Evidence visible before or during recurrence |
| Prevention | Concrete change to a future gate or behavior |
| Recall question | Short prompt used at the relevant gate |
| Pressure test | Scenario that attempts to reproduce the failure |
| Measures | Fields used to compare recurrence |
| Limitations | Known gaps and costs |
| Revisions | Links between earlier and later versions |

A narrative without a changed future gate is an observation, not yet a lesson.
A lesson without a recurrence measure is active but unproven.

## 6. Measurement Model

The first release uses:

- `unshared_interval_minutes`
- `material_steps_since_checkpoint`
- `detection_phase`
- `owner_reconstruction_needed`
- `prevented_material_action`
- `recurrence_count`
- `time_to_detection_minutes`
- `impact_level`

Impact levels:

| Level | Meaning |
| --- | --- |
| 0 | No shared-state action occurred before understanding was restored |
| 1 | Reversible local effect |
| 2 | Shared state changed and required recovery |
| 3 | Irreversible effect, exposure, or evidence loss |

The site must never claim improvement when required fields are unknown. Unknown
measurements remain visible as instrumentation gaps and candidate work.

## 7. Public-Safety Boundary

Publish reusable method, sanitized evidence, version history, limitations, and
measures. Do not publish:

- raw private journals or transcripts;
- personal account identifiers;
- private file or connector paths;
- credentials, tokens, or access topology;
- unreviewed claims about people;
- private incident detail that is unnecessary to apply the lesson.

Public pages may state that an immutable decision and outcome were verified,
but they must not link to a private record unless its owner deliberately makes
that record public in a later, separately reviewed action.

## 8. Visual and Interaction Design

The learning root should look related to the current public page while gaining
enough hierarchy for a growing body of material.

- Continue using fast, dependency-free static HTML and CSS.
- Use readable system typography and the existing light/dark color behavior.
- Introduce a restrained accent for learning links, lesson IDs, and statuses.
- Keep line length suitable for long-form reading.
- Use semantic landmarks, visible focus states, and skip navigation.
- Provide breadcrumb navigation below the learning root.
- Avoid animation that competes with reading.
- Avoid tracking, advertising, external fonts, and client-side frameworks.
- Make every page usable on narrow mobile screens and with keyboard navigation.

The home page receives only a concise Learning from Work card or document link.
The detailed navigation appears inside the learning root.

## 9. Content and Data Flow

The first release is file-first and manually published:

1. Work produces an observed problem.
2. Private evidence is preserved in its governed system.
3. A sanitized lesson is drafted from that evidence.
4. The lesson changes a skill or working gate.
5. Pressure tests record failures and passes.
6. A public lesson page and skill-version page present only the reusable layer.
7. Later recurrence updates the measures and may introduce a new version.

No database, form submission, analytics service, or automated private-to-public
pipeline is introduced in this release.

## 10. Failure Handling

- If a measurement is unavailable, publish it as unknown rather than estimate.
- If a lesson exposes private context, block publication and rewrite the lesson
  at the method level.
- If a lesson has no changed future gate, label it an observation and keep it
  out of the active lesson registry.
- If a later lesson contradicts an earlier one, preserve both versions and mark
  the relationship; do not silently rewrite history.
- If the home page becomes crowded, keep one learning entry point and move all
  internal navigation under `/learning/`.

## 11. Initial Publication Scope

The first implementation includes:

1. a shared stylesheet update that preserves the current visual character;
2. one Learning from Work entry on the public home page;
3. the learning root;
4. the method page;
5. the lesson registry and Lesson 001;
6. the skill registry and `shared-understanding-gateway` v0.1.0;
7. the measurement page;
8. the reader reuse guide;
9. updated README documentation describing the new public root.

Future lesson authoring automation, independent timer instrumentation, search,
feeds, translations beyond the opening statement, and contribution workflows
are outside the first implementation.

## 12. Verification and Acceptance Criteria

The implementation is acceptable when:

- every route resolves through plain static hosting;
- the existing home page remains recognizable and gains one clear learning
  entry point;
- a reader can move from Lesson 001 to its prevention, skill version, measures,
  and reuse template without private context;
- the Thai source statement and English rendering are both present;
- Lesson 001 explicitly names the v0.1.0 timer limitation;
- every required metric is defined and unknown values are not fabricated;
- no personal account identifiers, Box links, secrets, or raw private records
  appear in the public source;
- pages pass an automated internal-link check;
- HTML landmarks, headings, focus states, and mobile layout are reviewed;
- the public build is inspected before publication;
- publication occurs only after a separate implementation Decision is written
  to Box and read back.

## 13. Versioning and Revision

This design begins at version `0.1`. The public learning root and each lesson
retain their own visible version history. Revisions must state what ambiguity
was removed, what prevention changed, and which evidence justified the change.

The desired direction is not “more documentation.” It is a progressively
sharper method whose effects can be observed when the same class of problem
returns.
