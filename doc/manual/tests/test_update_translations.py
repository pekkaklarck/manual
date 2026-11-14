"""Verify translation fidelity and safe updates of marked Markdown sections."""

import importlib.util
import os
import re
import runpy
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from types import SimpleNamespace
from typing import cast
from unittest.mock import patch

import markdown
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs_gen_files.editor import FilesEditor

SCRIPT = Path(__file__).resolve().parents[1] / "docs/appendix/update_translations.py"
spec = importlib.util.spec_from_file_location("update_translations", SCRIPT)
assert spec is not None and spec.loader is not None
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


class RenderedTables(HTMLParser):

    def __init__(self, content):
        super().__init__()
        self.tables = []
        self.rows = []
        self.cells = []
        self.cell = None
        self.feed(markdown.markdown(content, extensions=["tables"]))

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.rows = []
        elif tag == "tr":
            self.cells = []
        elif tag in {"td", "th"}:
            self.cell = ""

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += data

    def handle_endtag(self, tag):
        if tag in {"td", "th"}:
            self.cells.append(self.cell)
            self.cell = None
        elif tag == "tr":
            self.rows.append(self.cells)
        elif tag == "table":
            self.tables.append(self.rows)


class TestSourceFidelity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.languages = updater.load_languages()

    def test_language_order_coverage_and_links(self):
        from robot.api import Language

        expected = sorted(
            (lang for lang in Language.__subclasses__() if lang.code != "en"),
            key=lambda lang: cast(str, lang.code),
        )
        self.assertEqual(self.languages, expected)
        docs = "\n".join(updater.generate_docs(self.languages))
        rendered = markdown.markdown(docs, extensions=["tables", "toc"])
        links = "\n".join(updater.list_translations(self.languages))
        self.assertEqual(len(re.findall(r"^## ", docs, re.M)), len(expected))
        self.assertEqual(len(links.splitlines()), len(expected))
        for lang in expected:
            self.assertIn(f"## {lang.name} ({lang.code})\n", docs)
        for fragment in re.findall(r"translations.md#([^)]*)", links):
            self.assertIn(f'id="{fragment}"', rendered)

    def test_all_table_values_and_version_notes_match_definitions(self):
        from robot.conf.languages import En, Language

        for lang in self.languages:
            with self.subTest(language=lang.code):
                doc = next(updater.generate_docs([lang]))
                tables = RenderedTables(doc).tables
                expected = []
                for suffix in ("_header", "_setting"):
                    expected.append(
                        [
                            [getattr(En, key), getattr(lang, key) or ""]
                            for key in vars(Language)
                            if key.endswith(suffix)
                        ]
                    )
                expected.append(
                    [
                        [
                            name.capitalize(),
                            ", ".join(getattr(lang, name + "_prefixes")),
                        ]
                        for name in ("given", "when", "then", "and", "but")
                    ]
                )
                expected.append(
                    [
                        [name.capitalize(), ", ".join(getattr(lang, name + "_strings"))]
                        for name in ("true", "false")
                    ]
                )
                if hasattr(lang, "deprecations") and lang.deprecations:
                    expected.append(
                        [
                            [old, new, f"RF {version}" if version else ""]
                            for old, (new, version) in lang.deprecations.items()
                        ]
                    )
                self.assertEqual([table[1:] for table in tables], expected)
                notes = re.findall(r"New in Robot Framework [\d.]+\.", lang.__doc__)
                self.assertEqual(
                    re.findall(r"New in Robot Framework [\d.]+\.", doc), notes
                )

    def test_subsection_headings_stay_out_of_the_toc(self):
        renderer = markdown.Markdown(
            extensions=["tables", "toc"],
            extension_configs={"toc": {"toc_depth": 3, "permalink": True}},
        )
        rendered = renderer.convert("\n".join(updater.generate_docs(self.languages)))
        # The TOC extension adds this attribute dynamically to Markdown.
        tokens = vars(renderer)["toc_tokens"]
        self.assertEqual(len(tokens), len(self.languages))
        self.assertTrue(
            all(item["level"] == 2 and not item["children"] for item in tokens)
        )
        for title in ("Section headers", "Settings", "BDD prefixes", "Boolean strings"):
            self.assertIn(f"#### {title}\n", updater.TEMPLATE)
        self.assertIn("#### Deprecations\n", updater.DEPRECATIONS)
        self.assertIn('<h4 id="settings">Settings', rendered)
        self.assertIn('href="#settings"', rendered)

    def test_duplicates_missing_values_and_literal_markdown(self):
        source = self.languages[0]
        values = {
            key: getattr(source, key)
            for key in vars(source.__base__)
            if not key.startswith("__")
        }
        values.update(
            name="Fixture",
            code="xx",
            __doc__="Fixture",
            settings_header="عربي | a\\b `code` *literal* _word_ [link] <tag> &amp;",
            library_setting=None,
            given_prefixes=["Second", "First", "Second"],
            true_strings=[],
            deprecations={"old|term": ("new*term", None)},
        )
        lang = SimpleNamespace(**values)
        tables = RenderedTables(next(updater.generate_docs([lang]))).tables
        self.assertEqual(tables[0][1], ["Settings", lang.settings_header])
        self.assertEqual(tables[1][1], ["Library", ""])
        self.assertEqual(tables[2][1], ["Given", "Second, First, Second"])
        self.assertEqual(tables[3][1], ["True", ""])
        self.assertEqual(tables[4][1], ["old|term", "new*term", ""])

    def test_language_without_deprecation_api(self):
        source = self.languages[0]
        values = {
            key: getattr(source, key)
            for key in vars(source.__base__)
            if key.endswith(("_header", "_setting", "_prefixes", "_strings"))
        }
        lang = SimpleNamespace(name="Fixture", code="xx", __doc__="Fixture", **values)
        without_metadata = next(updater.generate_docs([lang]))
        self.assertEqual(len(RenderedTables(without_metadata).tables), 4)
        self.assertNotIn("#### Deprecations", without_metadata)
        lang.deprecations = {}
        self.assertEqual(next(updater.generate_docs([lang])), without_metadata)


class TestMarkedUpdates(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.paths = [
            Path(self.temp.name) / name for name in ("translations.md", "data.md")
        ]

    def document(self, newline="\n"):
        return newline.join(
            [
                "Hand-written  spaces  ",
                updater.START_MARKER,
                "old",
                updater.END_MARKER,
                "Tail\t",
                "",
            ]
        ).encode()

    def test_rendering_preserves_surrounding_content_and_source_files(self):
        for newline in ("\n", "\r\n"):
            with self.subTest(newline=newline):
                for path in self.paths:
                    path.write_bytes(self.document(newline))
                    os.utime(path, ns=(1000000000, 1000000000))
                pages = updater.render_pages(*self.paths)
                for path, after in zip(self.paths, pages.values(), strict=True):
                    before = self.document(newline).decode()
                    self.assertEqual(
                        before.split(updater.START_MARKER)[0],
                        after.split(updater.START_MARKER)[0],
                    )
                    self.assertEqual(
                        before.split(updater.END_MARKER)[1],
                        after.split(updater.END_MARKER)[1],
                    )
                    self.assertNotIn("old", after)
                    self.assertEqual(after.count(updater.NOTICE), 1)
                    self.assertEqual(path.read_bytes(), self.document(newline))
                self.assertEqual(updater.render_pages(*self.paths), pages)
                self.assertEqual(
                    [path.stat().st_mtime_ns for path in self.paths], [1000000000] * 2
                )

    def test_export_skips_unchanged_files(self):
        for path in self.paths:
            path.write_bytes(self.document())
        pages = updater.render_pages(*self.paths)
        output_dir = Path(self.temp.name) / "export"
        updater.write_pages(output_dir, pages)
        for target, content in pages.items():
            path = output_dir / target
            self.assertEqual(path.read_bytes(), content.encode("utf-8"))
            os.utime(path, ns=(1000000000, 1000000000))
        updater.write_pages(output_dir, pages)
        for target in pages:
            self.assertEqual((output_dir / target).stat().st_mtime_ns, 1000000000)
        self.assertEqual(
            [path.read_bytes() for path in self.paths], [self.document()] * 2
        )

    def test_export_refuses_the_source_docs_directory(self):
        for output_dir in (updater.DOCS, updater.DOCS / "generated"):
            with (
                self.subTest(output_dir=output_dir),
                patch.object(Path, "write_bytes") as write,
                self.assertRaisesRegex(ValueError, "source docs folder"),
            ):
                updater.write_pages(output_dir, {Path("appendix/translations.md"): ""})
            write.assert_not_called()

    def test_build_function_refuses_source_file_writes_outside_a_build(self):
        for directory in (updater.DOCS, updater.DOCS / "generated"):
            with (
                self.subTest(directory=directory),
                patch.object(
                    FilesEditor,
                    "current",
                    return_value=SimpleNamespace(directory=directory),
                ),
                patch.object(Path, "write_bytes") as write,
                self.assertRaisesRegex(RuntimeError, "active ProperDocs build"),
            ):
                updater.update_translations()
            write.assert_not_called()

    def test_validates_both_files_before_writing(self):
        start, end = updater.START_MARKER, updater.END_MARKER
        invalid = [
            "",
            start,
            end,
            f"{end}\n{start}\n",
            f"{start}\n{start}\n{end}\n",
            f"{start}\n{end}\n{end}\n",
            f"inline {start}\n{end}\n",
        ]
        for bad in invalid:
            for broken in (0, 1):
                with self.subTest(content=bad, file=broken):
                    for path in self.paths:
                        path.write_bytes(self.document())
                    self.paths[broken].write_text(bad, encoding="utf-8")
                    before = [path.read_bytes() for path in self.paths]
                    with self.assertRaisesRegex(
                        ValueError, str(self.paths[broken].name)
                    ):
                        updater.render_pages(*self.paths)
                    self.assertEqual([path.read_bytes() for path in self.paths], before)

    def test_build_runner_executes_update(self):
        # gen-files calls run_path without run_name, so __name__ is '<run_path>'.
        config = cast(MkDocsConfig, MkDocsConfig())
        config.docs_dir = str(updater.DOCS)
        config.site_dir = str(Path(self.temp.name) / "site")
        config.use_directory_urls = True
        source_paths = (updater.TRANSLATIONS, updater.LOCALIZATION)
        for path in source_paths:
            source, start, end = updater.read_region(path)
            self.assertFalse(
                source[start:end].strip(), f"{path}: keep the region empty"
            )
        snapshot = [
            (path.read_bytes(), path.stat().st_mtime_ns) for path in source_paths
        ]
        expected = updater.render_pages()
        with FilesEditor(
            Files([]), config, directory=str(Path(self.temp.name) / "virtual")
        ) as editor:
            result = runpy.run_path(str(SCRIPT))
            self.assertEqual(result["__name__"], "<run_path>")
            self.assertEqual(len(editor.files), 2)
            for target, content in expected.items():
                generated = editor.files.get_file_from_path(target.as_posix())
                assert generated is not None and generated.abs_src_path is not None
                self.assertEqual(
                    Path(generated.abs_src_path).read_bytes(), content.encode("utf-8")
                )
                self.assertEqual(
                    editor.edit_paths[target.as_posix()], target.as_posix()
                )
        self.assertEqual(
            [(path.read_bytes(), path.stat().st_mtime_ns) for path in source_paths],
            snapshot,
        )


if __name__ == "__main__":
    unittest.main()
