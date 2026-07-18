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
    "private-storage.example.invalid/" + "item/",
    "SYNTHETIC_INTERNAL_" + "JOURNAL_PATH",
)
PROHIBITED_PUBLIC_PATTERNS = (
    ("email address", re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)),
    ("long numeric account identifier", re.compile(r"(?<![A-Z0-9])\d{10,}(?![A-Z0-9])", re.I)),
    (
        "literal credential assignment",
        re.compile(r"(?:token|password|secret)\s*[:=]\s*[\"']?[A-Z0-9/+]{16,}", re.I),
    ),
    ("private storage URL", re.compile(r"https?://[^\s)>\"']+/(?:files?|folders?)/", re.I)),
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
    def test_readme_documents_learning_root_and_test_command(self) -> None:
        readme = read_page("README.md")
        self.assertIn("learning/", readme)
        self.assertIn("python3 -m unittest tests/test_learning_site.py -v", readme)
        self.assertIn("sanitized", readme.lower())

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

    def test_shared_styles_do_not_override_the_home_width(self) -> None:
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("body { font-family:", css)
        self.assertIn("max-width: 920px;", css)
        self.assertNotRegex(
            css,
            r"body\s*\{\s*max-width:\s*var\(--page-max\);\s*\}",
        )

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

    def test_learning_design_is_accepted(self) -> None:
        design = read_page(
            "docs/superpowers/specs/2026-07-18-learning-from-work-design.md"
        )
        self.assertRegex(design, r"(?m)^status: accepted$")


if __name__ == "__main__":
    unittest.main()
