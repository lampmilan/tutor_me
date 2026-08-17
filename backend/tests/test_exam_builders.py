"""Smoke tests for catalog oracles and raw-string preamble."""

from __future__ import annotations

import unittest
from pathlib import Path

from app.exams.builders import build_exam_preamble, expected_for_task, parse_dataset, raw_file_preamble
from app.exams.loader import discover_exams, load_exam_by_id


class CatalogStructureTests(unittest.TestCase):
    def test_raw_preamble_reads_file_into_string(self) -> None:
        src = raw_file_preamble("felajanlas.txt", "felajanlasok")
        self.assertEqual(
            src,
            'with open("felajanlas.txt", encoding="utf-8") as f:\n'
            "    felajanlasok = f.read()\n",
        )

    def test_every_catalog_exam_materializes_expected_outputs(self) -> None:
        exams = discover_exams()
        self.assertGreaterEqual(len(exams), 7)
        for loaded in exams:
            tmpl = loaded.template
            preamble = build_exam_preamble(tmpl)
            self.assertIn("f.read()", preamble)
            self.assertNotIn(".append(", preamble)
            visible = parse_dataset(
                tmpl.dataset_type, loaded.visible_content, plugin=loaded.plugin
            )
            for spec in (t.model_dump() for t in tmpl.tasks):
                out = expected_for_task(visible, spec, plugin=loaded.plugin)
                self.assertIsInstance(out, str)

    def test_viragagyasok_uses_exam_plugin(self) -> None:
        loaded = load_exam_by_id("viragagyasok")
        self.assertIsNotNone(loaded.plugin)
        self.assertIsNotNone(loaded.plugin.parse)
        self.assertIn("offer_count", loaded.plugin.task_builders)
        rows = parse_dataset("viragagyasok", loaded.visible_content, plugin=loaded.plugin)
        spec = next(t.model_dump() for t in loaded.template.tasks if t.type == "offer_count")
        out = expected_for_task(rows, spec, plugin=loaded.plugin)
        self.assertTrue(out.startswith("A felajánlások száma: "))

    def test_mrz_gender_and_name_follow_the_dataset(self) -> None:
        loaded = load_exam_by_id("mrz-kod")
        self.assertIsNotNone(loaded.plugin)
        visible = parse_dataset("lines", loaded.visible_content, plugin=loaded.plugin)
        hidden = parse_dataset("lines", loaded.hidden_contents[0], plugin=loaded.plugin)
        gender_spec = {"type": "gender"}
        self.assertEqual(
            expected_for_task(visible, gender_spec, plugin=loaded.plugin),
            "Az okmány tulajdonosa nő.",
        )
        self.assertEqual(
            expected_for_task(hidden, gender_spec, plugin=loaded.plugin),
            "Az okmány tulajdonosa férfi.",
        )
        name_spec = {"type": "mrz_name"}
        self.assertEqual(
            expected_for_task(visible, name_spec, plugin=loaded.plugin),
            "Családi név: NAGY KOVACS\nUtónév: GYOENGYVIRAG MARIA\nA név nem csonkolt.",
        )
        hidden_name = expected_for_task(hidden, name_spec, plugin=loaded.plugin)
        self.assertIn("Családi név: NAGY", hidden_name)
        self.assertIn("Utónév: ISTVAN", hidden_name)

    def test_plugin_path_exists_for_unique_exams_only(self) -> None:
        root = Path(__file__).resolve().parents[1] / "app" / "exams"
        self.assertTrue((root / "viragagyasok" / "builders.py").is_file())
        self.assertTrue((root / "mrz-kod" / "builders.py").is_file())
        self.assertFalse((root / "cities" / "builders.py").is_file())


if __name__ == "__main__":
    unittest.main()
