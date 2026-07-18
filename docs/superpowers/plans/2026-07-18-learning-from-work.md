# Learning from Work Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a dependency-free public learning root that turns observed work failures into reusable lessons, skill changes, and measurable recurrence evidence.

**Architecture:** Keep the existing static GitHub Pages surface and add an isolated `/learning/` route tree made of semantic HTML files sharing the root `styles.css`. A standard-library Python contract test verifies routes, internal links, required copy, accessibility landmarks, metrics, and public-safety exclusions before any publication action.

**Tech Stack:** HTML5, CSS, Python 3 standard library `unittest`, GitHub Pages static hosting.

## Global Constraints

- Preserve the existing home page as the small public entry point and add only one clear Learning from Work entry.
- Keep one visual family across the home page and every learning route: extract the current embedded home styles into the canonical root `styles.css`, preserve the existing system font stack and familiar typography, and extend that stylesheet without introducing a competing theme.
- Use dependency-free static HTML and CSS; do not add a framework, database, analytics, external fonts, or client-side build step.
- Preserve light/dark behavior, readable line length, keyboard focus, semantic landmarks, skip navigation, and narrow-screen usability.
- Keep the Thai source statement and label the English text as an explanatory rendering.
- Publish reusable method and sanitized evidence only; never publish private Box links, account identifiers, credentials, raw transcripts, or private operational paths.
- Lesson 001 must name the procedural-timer limitation in `shared-understanding-gateway` version `0.1.0`.
- Unknown measurements must remain unknown; do not estimate or fabricate them.
- Use the accepted design at `docs/superpowers/specs/2026-07-18-learning-from-work-design.md` as the content authority.

---

## File Map

| File | Responsibility |
| --- | --- |
| `tests/test_learning_site.py` | Static route, link, content, accessibility, and public-safety contract |
| `styles.css` | Shared visual system for home and learning pages |
| `index.html` | Existing public home plus one learning entry point |
| `learning/index.html` | Learning-root explanation and route map |
| `learning/method/index.html` | Repeatable sharpening cycle |
| `learning/lessons/index.html` | Versioned lesson registry |
| `learning/lessons/001-shared-understanding-discontinuity/index.html` | First public lesson |
| `learning/skills/index.html` | Skill-evolution registry |
| `learning/skills/shared-understanding-gateway/index.html` | Public behavior and limitation of v0.1.0 |
| `learning/measurement/index.html` | Common recurrence measures and impact scale |
| `learning/use-this-method/index.html` | Minimal reusable lesson template |
| `README.md` | Repository map and verification instructions |

## Shared Page Contract

Every learning page must contain the same shell. This learning-root example
uses base-path-safe relative URLs; nested pages adjust the number of `../`
segments for their directory depth:

```html
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <p class="eyebrow"><a href="../">PUNNARAJ Public Mutual Understanding</a></p>
  <nav class="learning-nav" aria-label="Learning navigation">
    <ul>
      <li><a href="./">Learning home</a></li>
      <li><a href="method/">Method</a></li>
      <li><a href="lessons/">Lessons</a></li>
      <li><a href="skills/">Skill evolution</a></li>
      <li><a href="measurement/">Measurement</a></li>
      <li><a href="use-this-method/">Use this method</a></li>
    </ul>
  </nav>
</header>
<nav class="breadcrumbs" aria-label="Breadcrumb">
  <ul>
    <li><a href="../">Home</a></li>
    <li><a href="./">Learning from Work</a></li>
  </ul>
</nav>
<main id="main"></main>
<footer class="site-footer">
  <p>Accepted-for-now understanding. Open to correction and evidence-led revision.</p>
</footer>
```

Internal links use depth-correct relative directory URLs such as `method/` or
`../measurement/` so GitHub Pages serves the matching `index.html` under any
project-site base path without exposing file names.

---

### Task 1: Add the Public-Site Contract Test

**Files:**
- Create: `tests/test_learning_site.py`

**Interfaces:**
- Consumes: repository-relative static HTML paths and links.
- Produces: `python3 -m unittest tests/test_learning_site.py -v` as the deterministic release gate.

- [ ] **Step 1: Write the failing contract test**

Create `tests/test_learning_site.py` with:

```python
from __future__ import annotations

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PAGES = (
    "index.html",
    "learning/index.html",
    "learning/method/index.html",
    "learning/lessons/index.html",
    "learning/lessons/001-shared-understanding-discontinuity/index.html",
    "learning/skills/index.html",
    "learning/skills/shared-understanding-gateway/index.html",
    "learning/measurement/index.html",
    "learning/use-this-method/index.html",
)
REQUIRED_METRICS = (
    "unshared_interval_minutes",
    "material_steps_since_checkpoint",
    "detection_phase",
    "owner_reconstruction_needed",
    "prevented_material_action",
    "recurrence_count",
    "time_to_detection_minutes",
    "impact_level",
)
SYNTHETIC_PRIVATE_SENTINELS = (
    "synthetic-user@" + "example.invalid",
    "123456" + "789012",
    "private-storage.example.invalid/" + "item/",
)
PROHIBITED_PUBLIC_PATTERNS = (
    ("email address", re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)),
    ("long numeric account identifier", re.compile(r"(?<![A-Z0-9])\d{10,}(?![A-Z0-9])", re.I)),
    ("literal credential assignment", re.compile(r"(?:token|password|secret)\s*[:=]\s*[\"']?[A-Z0-9/+]{16,}", re.I)),
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.references: list[tuple[str, str]] = []
        self.stylesheets: list[str] = []
        self.ids: set[str] = set()
        self.tags: list[str] = []
        self.skip_links: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        self.tags.append(tag)
        if values.get("id"):
            self.ids.add(values["id"])
        for attribute in ("href", "src"):
            reference = values.get(attribute)
            if reference:
                self.references.append((attribute, reference))
        href = values.get("href")
        if tag == "link" and href and "stylesheet" in values.get("rel", "").split():
            self.stylesheets.append(href)
        if tag == "a" and href:
            self.links.append(href)
            if "skip-link" in values.get("class", "").split():
                self.skip_links.append(href)


def read_page(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def iter_public_source_files():
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if not path.is_file() or relative.parts[0] in {".git", ".superpowers"}:
            continue
        try:
            yield relative, path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue


def resolve_internal_link(source: Path, href: str) -> Path | None:
    if href.startswith("/"):
        raise ValueError(f"root-absolute reference is not base-path-safe: {href}")
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc or href.startswith(("mailto:", "#")):
        return None
    raw_path = parsed.path
    target = source.parent / raw_path
    if raw_path.endswith("/"):
        target = target / "index.html"
    elif not target.suffix:
        target = target / "index.html"
    return target.resolve()


class LearningSiteContractTest(unittest.TestCase):
    def test_required_pages_exist(self) -> None:
        for page in REQUIRED_PAGES:
            with self.subTest(page=page):
                self.assertTrue((ROOT / page).is_file(), page)

    def test_all_internal_links_resolve(self) -> None:
        for page in REQUIRED_PAGES:
            source = ROOT / page
            if not source.exists():
                continue
            parser = PageParser()
            parser.feed(source.read_text(encoding="utf-8"))
            for attribute, reference in parser.references:
                with self.subTest(page=page, attribute=attribute, reference=reference):
                    self.assertFalse(reference.startswith("/"), reference)
                    target = resolve_internal_link(source, reference)
                    if target is not None:
                        self.assertTrue(target.is_file(), str(target))

    def test_pages_use_base_path_safe_resolving_stylesheets(self) -> None:
        for page in REQUIRED_PAGES:
            source = ROOT / page
            parser = PageParser()
            parser.feed(source.read_text(encoding="utf-8"))
            with self.subTest(page=page):
                self.assertEqual(len(parser.stylesheets), 1)
                stylesheet = parser.stylesheets[0]
                self.assertFalse(stylesheet.startswith("/"), stylesheet)
                target = resolve_internal_link(source, stylesheet)
                self.assertIsNotNone(target)
                self.assertTrue(target.is_file(), str(target))

    def test_learning_pages_have_accessible_landmarks(self) -> None:
        for page in REQUIRED_PAGES[1:]:
            if not (ROOT / page).exists():
                continue
            parser = PageParser()
            parser.feed(read_page(page))
            with self.subTest(page=page):
                self.assertIn("main", parser.tags)
                self.assertIn("header", parser.tags)
                self.assertIn("nav", parser.tags)
                self.assertIn("footer", parser.tags)
                self.assertIn("main", parser.ids)
                self.assertIn("#main", parser.skip_links)

    def test_home_has_one_learning_entry(self) -> None:
        html = read_page("index.html")
        self.assertEqual(html.count('href="learning/"'), 1)

    def test_home_uses_the_single_shared_stylesheet(self) -> None:
        html = read_page("index.html")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn('<link rel="stylesheet" href="styles.css">', html)
        self.assertNotIn("<style>", html)
        self.assertIn('font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif', css)
        self.assertIn("color-scheme: light dark", css)

    def test_source_statement_and_rendering_are_present(self) -> None:
        html = read_page("learning/index.html")
        self.assertIn("เราไม่ได้หาความจริงสุดท้าย", html)
        self.assertIn("Working English rendering", html)
        self.assertIn("sharpen what was blunt", html)

    def test_lesson_and_skill_contract_are_explicit(self) -> None:
        lesson = read_page(
            "learning/lessons/001-shared-understanding-discontinuity/index.html"
        )
        skill = read_page(
            "learning/skills/shared-understanding-gateway/index.html"
        )
        for phrase in (
            "Shared Understanding Discontinuity",
            "8-minute soft",
            "10-minute hard",
            "7 material steps",
            "procedural timer",
            "independently interrupting alarm",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, lesson + skill)

    def test_every_metric_is_defined(self) -> None:
        measurement = read_page("learning/measurement/index.html")
        for metric in REQUIRED_METRICS:
            with self.subTest(metric=metric):
                self.assertIn(metric, measurement)
        for level in range(4):
            self.assertRegex(measurement, rf">\s*{level}\s*<")

    def test_private_identifiers_are_absent(self) -> None:
        for path, source in iter_public_source_files():
            for sentinel in SYNTHETIC_PRIVATE_SENTINELS:
                with self.subTest(path=str(path), sentinel=sentinel):
                    self.assertNotIn(sentinel, source)
            for label, pattern in PROHIBITED_PUBLIC_PATTERNS:
                with self.subTest(path=str(path), pattern=label):
                    self.assertIsNone(pattern.search(source))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify the expected failure**

Run:

```bash
python3 -m unittest tests/test_learning_site.py -v
```

Expected: `test_required_pages_exist` fails because `learning/index.html` and
the other learning routes do not exist. The private-identifier test must pass.

- [ ] **Step 3: Commit the red contract**

```bash
git add tests/test_learning_site.py
git commit -m "test: define learning site contract"
```

---

### Task 2: Add the Shared Learning Visual System and Home Entry

**Files:**
- Modify: `styles.css`
- Modify: `index.html`

**Interfaces:**
- Consumes: existing home-page classes and `learning/` route contract.
- Produces: shared `.site-header`, `.breadcrumbs`, `.lesson-card`, `.status`, `.metric-table`, `.skip-link`, and focus styles used by all learning pages.

- [ ] **Step 1: Add a focused failing home-entry assertion if needed**

Confirm the existing `test_home_has_one_learning_entry` fails:

```bash
python3 -m unittest tests.test_learning_site.LearningSiteContractTest.test_home_has_one_learning_entry -v
```

Expected: FAIL because `index.html` has no `href="learning/"`.

- [ ] **Step 2: Replace the unused alternate theme with the current home style**

Copy the complete contents of the current `index.html` `<style>` block into
`styles.css` first, without changing its font stack, width, line height,
light/dark behavior, card radius, or spacing. Delete the pre-existing unused
dark-theme contents of `styles.css`. Then append this exact learning extension:

```css
:root {
  --page-max: 72rem;
  --reading-max: 46rem;
  --learning-accent: #2563eb;
  --accent-soft: color-mix(in srgb, var(--learning-accent) 12%, transparent);
  --border: color-mix(in srgb, currentColor 22%, transparent);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { max-width: var(--page-max); }
a { text-underline-offset: 0.18em; }
a:focus-visible, summary:focus-visible {
  outline: 3px solid var(--learning-accent);
  outline-offset: 3px;
}
.skip-link {
  position: absolute;
  left: 1rem;
  top: -5rem;
  padding: 0.65rem 0.9rem;
  color: Canvas;
  background: CanvasText;
  z-index: 10;
}
.skip-link:focus { top: 1rem; }
.site-header, .site-footer { border-color: var(--border); }
.breadcrumbs ul, .learning-nav ul {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem 1rem;
  list-style: none;
  padding: 0;
}
.breadcrumbs li:not(:last-child)::after { content: "/"; margin-left: 1rem; opacity: 0.5; }
.reading { max-width: var(--reading-max); }
.eyebrow, .status { font-size: 0.82rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; }
.status { display: inline-block; border: 1px solid var(--border); border-radius: 999px; padding: 0.2rem 0.55rem; }
.lesson-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); gap: 1rem; }
.lesson-card { border: 1px solid var(--border); border-radius: 0.8rem; padding: 1rem; background: var(--accent-soft); }
.lesson-card > :first-child { margin-top: 0; }
.metric-table { width: 100%; border-collapse: collapse; }
.metric-table th, .metric-table td { text-align: left; vertical-align: top; border-bottom: 1px solid var(--border); padding: 0.65rem; }
.cycle { border-left: 0.3rem solid var(--learning-accent); padding-left: 1rem; }
.source-statement { font-size: clamp(1.2rem, 3vw, 1.8rem); line-height: 1.45; }
.site-footer { border-top: 1px solid var(--border); margin-top: 3rem; padding-top: 1rem; opacity: 0.78; }
@media (max-width: 40rem) {
  body { padding: 1.25rem 1rem; }
  .metric-table { display: block; overflow-x: auto; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
}
```

- [ ] **Step 3: Link the shared stylesheet and add exactly one learning entry**

Replace the complete embedded style element in `index.html` with:

```html
<link rel="stylesheet" href="styles.css">
```

Inside the existing Documents list, add exactly:

```html
<li><a href="learning/">Learning from Work</a> — lessons that change future work</li>
```

Do not add any other `href="learning/"` link to the home page.

- [ ] **Step 4: Run the focused test**

```bash
python3 -m unittest \
  tests.test_learning_site.LearningSiteContractTest.test_home_has_one_learning_entry \
  tests.test_learning_site.LearningSiteContractTest.test_home_uses_the_single_shared_stylesheet -v
```

Expected: PASS.

- [ ] **Step 5: Commit the shared shell**

```bash
git add index.html styles.css
git commit -m "feat: add learning entry and shared styles"
```

---

### Task 3: Publish the Learning Root and Sharpening Method

**Files:**
- Create: `learning/index.html`
- Create: `learning/method/index.html`

**Interfaces:**
- Consumes: root `/styles.css` and the shared page contract.
- Produces: reader entry point and the canonical eight-stage learning cycle linked by later pages.

- [ ] **Step 1: Confirm the source-statement test fails**

```bash
python3 -m unittest tests.test_learning_site.LearningSiteContractTest.test_source_statement_and_rendering_are_present -v
```

Expected: ERROR or FAIL because `learning/index.html` does not exist.

- [ ] **Step 2: Create the learning root with the approved copy**

Create `learning/index.html` as a complete semantic page. Its `<main id="main">`
must contain this exact source and rendering block:

```html
<p class="eyebrow">Learning from Work · version 0.1</p>
<h1>Make the method sharper</h1>
<blockquote class="source-statement" lang="th">
  <p>การทำผิดไม่ใช่ปัญหาที่ร้ายที่สุด การทำผิดแล้วไม่สร้างบทเรียนต่างหากที่ทำให้ความผิดเดิมกลับมาอีก เราไม่ได้หาความจริงสุดท้าย เราทำสิ่งที่เคยทื่อให้คมขึ้น ด้วยการลบความเข้าใจผิดและความกำกวม จนสิ่งที่ต้องการสื่อเด่นชัดขึ้น</p>
</blockquote>
<section aria-labelledby="rendering-title" class="reading">
  <h2 id="rendering-title">Working English rendering</h2>
  <p>Making a mistake is not the worst failure. Failing to turn it into a lesson allows the same mistake to return. We are not searching for final truth; we sharpen what was blunt by removing misunderstanding and ambiguity until the meaning becomes clearer.</p>
  <p class="meta">The English text explains the Thai source statement. It does not replace it.</p>
</section>
```

Below it, create five `.lesson-card` links to `/learning/method/`,
`/learning/lessons/`, `/learning/skills/`, `/learning/measurement/`, and
`/learning/use-this-method/`; combine “Why We Learn” with the introductory
section so no additional route is required.

- [ ] **Step 3: Create the method page**

Create `learning/method/index.html` with an ordered list containing these exact
stages and outputs:

```html
<ol class="cycle">
  <li><strong>Work:</strong> act within a bounded task and authority.</li>
  <li><strong>Observe failure:</strong> name the gap without rewriting it as success.</li>
  <li><strong>Preserve evidence:</strong> keep enough governed evidence to reconstruct the event.</li>
  <li><strong>Extract a lesson:</strong> define signals, prevention, and a recall question.</li>
  <li><strong>Change a gate:</strong> make the lesson alter future behavior.</li>
  <li><strong>Pressure-test:</strong> reproduce the failure conditions before trusting the change.</li>
  <li><strong>Measure recurrence:</strong> compare detection time and impact, including unknown values.</li>
  <li><strong>Revise:</strong> remove new ambiguity and publish a new version when evidence warrants it.</li>
</ol>
```

Add the rule: “A narrative without a changed future gate is an observation, not
yet a lesson.” Link the rule to `/learning/use-this-method/`.

- [ ] **Step 4: Run route, link, landmark, and statement tests**

```bash
python3 -m unittest \
  tests.test_learning_site.LearningSiteContractTest.test_required_pages_exist \
  tests.test_learning_site.LearningSiteContractTest.test_all_internal_links_resolve \
  tests.test_learning_site.LearningSiteContractTest.test_learning_pages_have_accessible_landmarks \
  tests.test_learning_site.LearningSiteContractTest.test_source_statement_and_rendering_are_present -v
```

Expected: statement test passes; route test still fails only for later-task
pages. Existing links on the two new pages must resolve.

- [ ] **Step 5: Commit the learning foundation**

```bash
git add learning/index.html learning/method/index.html
git commit -m "feat: explain the public learning method"
```

---

### Task 4: Publish Lesson 001

**Files:**
- Create: `learning/lessons/index.html`
- Create: `learning/lessons/001-shared-understanding-discontinuity/index.html`

**Interfaces:**
- Consumes: canonical method stages and measurement route.
- Produces: stable lesson ID `PUNNARAJ-WAY-LESSON-001` and links to the affected skill.

- [ ] **Step 1: Confirm the lesson contract fails**

```bash
python3 -m unittest tests.test_learning_site.LearningSiteContractTest.test_lesson_and_skill_contract_are_explicit -v
```

Expected: ERROR or FAIL because the lesson and skill pages are absent.

- [ ] **Step 2: Create the lesson registry**

Create `learning/lessons/index.html` with one registry card containing:

```html
<article class="lesson-card">
  <p class="status">Active · introduced in skill v0.1.0</p>
  <h2><a href="001-shared-understanding-discontinuity/">Lesson 001 — Shared Understanding Discontinuity</a></h2>
  <p>Work can remain coherent inside a private agent context while its owner loses the causal path between shared states.</p>
  <p><strong>Evidence state:</strong> baseline reproduced; revised gate passed a forward pressure test; recurrence evidence remains open.</p>
</article>
```

- [ ] **Step 3: Create Lesson 001**

Create the lesson page with these exact sections and facts:

```html
<p class="eyebrow">PUNNARAJ-WAY-LESSON-001 · active</p>
<h1>Shared Understanding Discontinuity</h1>
<section><h2>Failure</h2><p>Work continued coherently inside an agent's private context while the owner lost the causal path between shared states.</p></section>
<section><h2>Detection signals</h2><ul><li>Long user-visible silence during active work</li><li>Many rapid tool calls or material steps</li><li>A decision request without its causal bridge</li><li>Reasons preserved only in transient notes</li><li>Conflicting current state, journal, identity, or storage location</li></ul></section>
<section><h2>Prevention that changed future work</h2><ul><li>Prepare a checkpoint at the 8-minute soft limit</li><li>Stop at the 10-minute hard limit</li><li>Stop after 7 material steps</li><li>Name the active Lesson ID and prevention rule</li><li>Verify the decision record before material action</li><li>Record a separate outcome and recurrence measures</li></ul></section>
<section><h2>Recall question</h2><blockquote><p>Can the owner reconstruct why this is the next action from the shared surface alone?</p></blockquote></section>
<section><h2>Pressure-test evidence</h2><p>The baseline stopped without a durable decision, explicit lesson recall, or measures. The first revised run still omitted explicit lesson and metric recall. The second revision passed before shared action. This is evidence that the gate behaves differently under the test, not proof that recurrence is impossible.</p></section>
<section><h2>Known limitation</h2><p>Version 0.1.0 uses a procedural timer. It does not yet provide an independently interrupting alarm. Timing that was not instrumented remains unknown.</p></section>
```

Finish with depth-correct relative links to
`../../skills/shared-understanding-gateway/`, `../../measurement/`, and
`../../use-this-method/`.

- [ ] **Step 4: Run lesson and safety tests**

```bash
python3 -m unittest \
  tests.test_learning_site.LearningSiteContractTest.test_lesson_and_skill_contract_are_explicit \
  tests.test_learning_site.LearningSiteContractTest.test_private_identifiers_are_absent -v
```

Expected: lesson phrases are present; the combined test may still fail only
because the skill page is absent. The safety test passes.

- [ ] **Step 5: Commit Lesson 001**

```bash
git add learning/lessons
git commit -m "feat: publish shared-understanding lesson"
```

---

### Task 5: Publish Skill Evolution

**Files:**
- Create: `learning/skills/index.html`
- Create: `learning/skills/shared-understanding-gateway/index.html`

**Interfaces:**
- Consumes: Lesson 001 and measurement links.
- Produces: public version record for `shared-understanding-gateway` v0.1.0.

- [ ] **Step 1: Create the skill registry**

Create `learning/skills/index.html` with:

```html
<article class="lesson-card">
  <p class="status">v0.1.0 · active pilot</p>
  <h2><a href="shared-understanding-gateway/">Shared Understanding Gateway</a></h2>
  <p>Introduced because Lesson 001 showed that accurate private work can still fail owner governance.</p>
</article>
```

- [ ] **Step 2: Create the skill-version page**

Create `learning/skills/shared-understanding-gateway/index.html` with:

```html
<p class="eyebrow">Skill evolution · v0.1.0</p>
<h1>Shared Understanding Gateway</h1>
<section><h2>Behavior introduced</h2><ul><li>8-minute soft checkpoint</li><li>10-minute hard stop</li><li>Stop after 7 material steps</li><li>Explicit Lesson ID and prevention recall</li><li>Decision verification before material action</li><li>Separate outcome and recurrence measurement</li></ul></section>
<section><h2>Why this version exists</h2><p>Lesson 001 showed that private coherence is not shared understanding. The gateway creates an observable boundary before decisions, commits, mutations, handoffs, and other material actions.</p></section>
<section><h2>Current evidence</h2><p>A baseline reproduced the gap. One forward test exposed missing explicit lesson and metric recall. A revised forward test passed before shared action.</p></section>
<section><h2>Known limitation</h2><p>The v0.1.0 timer is a procedural timer, not an independently interrupting alarm. Independent timing instrumentation is a candidate for a later version, not a completed feature.</p></section>
<section><h2>Revision rule</h2><p>A higher version is not automatically better. A revision must state which ambiguity was removed, what gate changed, and what evidence supports earlier detection, lower impact, or lower prevention cost without lost protection.</p></section>
```

Link back to Lesson 001 and forward to measurement.

- [ ] **Step 3: Run the lesson/skill contract**

```bash
python3 -m unittest tests.test_learning_site.LearningSiteContractTest.test_lesson_and_skill_contract_are_explicit -v
```

Expected: PASS.

- [ ] **Step 4: Commit skill evolution**

```bash
git add learning/skills
git commit -m "feat: publish gateway skill evolution"
```

---

### Task 6: Publish Measurement and Reader Reuse

**Files:**
- Create: `learning/measurement/index.html`
- Create: `learning/use-this-method/index.html`

**Interfaces:**
- Consumes: stable metrics defined by Lesson 001.
- Produces: public comparison contract and infrastructure-neutral reuse template.

- [ ] **Step 1: Confirm the metric test fails**

```bash
python3 -m unittest tests.test_learning_site.LearningSiteContractTest.test_every_metric_is_defined -v
```

Expected: ERROR because `learning/measurement/index.html` is absent.

- [ ] **Step 2: Create the measurement page**

Create a `.metric-table` with these exact rows:

```html
<tbody>
  <tr><th><code>unshared_interval_minutes</code></th><td>Minutes since the last meaningful shared checkpoint; unknown when not instrumented.</td></tr>
  <tr><th><code>material_steps_since_checkpoint</code></th><td>Material steps taken after the last shared checkpoint.</td></tr>
  <tr><th><code>detection_phase</code></th><td>before-decision, before-action, after-action, or owner-detected.</td></tr>
  <tr><th><code>owner_reconstruction_needed</code></th><td>Whether the owner had to rebuild the missing causal path.</td></tr>
  <tr><th><code>prevented_material_action</code></th><td>Whether the gate stopped a material action before shared understanding was restored.</td></tr>
  <tr><th><code>recurrence_count</code></th><td>Number of linked recurrences after lesson activation.</td></tr>
  <tr><th><code>time_to_detection_minutes</code></th><td>Elapsed minutes from recurrence start to detection; unknown when not instrumented.</td></tr>
  <tr><th><code>impact_level</code></th><td>Observed impact on the common 0–3 scale.</td></tr>
</tbody>
```

Add an impact table containing `<td>0</td>` through `<td>3</td>` with the
accepted definitions, plus this rule:

```html
<p><strong>Comparison rule:</strong> claim improvement only when evidence shows earlier detection, lower impact, less owner reconstruction, or lower prevention cost without weaker protection. A higher version number alone is not improvement.</p>
```

- [ ] **Step 3: Create the reuse guide**

Create `learning/use-this-method/index.html` with this copyable template:

```html
<pre><code>Lesson ID:
Title:
Status:
Introduced version:
Failure:
Detection signals:
Prevention that changes a future gate:
Recall question:
Pressure test:
Measures:
Known limitations:
Revision links:</code></pre>
```

Then give the reader the eight method stages from Task 3 and explicitly state:
“You do not need PUNNARAJ terminology, Box, or an AI agent to use this method.
You need governed evidence, a changed future gate, and honest recurrence
measurement.”

- [ ] **Step 4: Run metric, route, link, landmark, and safety tests**

```bash
python3 -m unittest tests/test_learning_site.py -v
```

Expected: all tests pass except any failure caused by incomplete README work;
the current test file does not yet inspect README, so the expected result is
`OK`.

- [ ] **Step 5: Commit measurement and reuse**

```bash
git add learning/measurement learning/use-this-method
git commit -m "feat: publish learning measures and reuse guide"
```

---

### Task 7: Document, Inspect, and Prepare Publication

**Files:**
- Modify: `README.md`
- Modify: `tests/test_learning_site.py`

**Interfaces:**
- Consumes: the complete public route tree.
- Produces: contributor verification instructions and final release gate.

- [ ] **Step 1: Add the README contract test**

Add this method to `LearningSiteContractTest`:

```python
def test_readme_documents_learning_root_and_test_command(self) -> None:
    readme = read_page("README.md")
    self.assertIn("learning/", readme)
    self.assertIn("python3 -m unittest tests/test_learning_site.py -v", readme)
    self.assertIn("sanitized", readme.lower())
```

- [ ] **Step 2: Run the new test and verify failure**

```bash
python3 -m unittest tests.test_learning_site.LearningSiteContractTest.test_readme_documents_learning_root_and_test_command -v
```

Expected: FAIL because the README does not yet document the learning root.

- [ ] **Step 3: Update README**

Add this section after the existing Files section:

````markdown
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
````

Add the new learning routes to the README Files list.

- [ ] **Step 4: Run the complete automated gate**

```bash
python3 -m unittest tests/test_learning_site.py -v
git diff --check
```

Expected: all tests PASS, final line `OK`, and `git diff --check` emits no
output.

- [ ] **Step 5: Serve and inspect the static site**

Run:

```bash
python3 -m http.server 8000 --directory .
```

Inspect these routes at desktop and narrow mobile widths:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/learning/
http://127.0.0.1:8000/learning/lessons/001-shared-understanding-discontinuity/
http://127.0.0.1:8000/learning/skills/shared-understanding-gateway/
http://127.0.0.1:8000/learning/measurement/
http://127.0.0.1:8000/learning/use-this-method/
```

Expected: no horizontal page overflow; keyboard focus remains visible; skip
links move focus to `#main`; all learning navigation and breadcrumbs resolve;
the home page remains recognizable with exactly one learning entry.

- [ ] **Step 6: Commit the release documentation**

```bash
git add README.md tests/test_learning_site.py
git commit -m "docs: add learning site verification"
```

- [ ] **Step 7: Stop at the publication gate**

Before merging or publishing, create and read back a separate Box Decision that
names the exact source branch, commit, target branch, expected public URL,
verification evidence, rollback method, Lesson 001 recall, and recurrence
metrics. Do not merge, deploy, or claim publication before that gate passes.
