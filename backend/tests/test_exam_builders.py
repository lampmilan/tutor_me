"""Smoke tests for catalog oracles and raw-string preamble."""

from __future__ import annotations

import unittest
from pathlib import Path

from app.exams.builders import expected_for_task, parse_dataset, raw_file_preamble
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
            preamble = (tmpl.preamble or "").strip() or raw_file_preamble(
                tmpl.data_file, tmpl.shared_variable or "data"
            )
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
        self.assertTrue((root / "fogasok" / "builders.py").is_file())
        self.assertTrue((root / "hutohaz" / "builders.py").is_file())
        self.assertFalse((root / "cities" / "builders.py").is_file())


LAUNCH_KOZEP = [
    "cities",
    "versenyido",
    "fogasok",
    "locsolo",
    "sorsjegy",
    "csomagfeladas",
    "uszoda",
    "csoposta",
    "kerekparallomas",
    "madareteto",
]
LAUNCH_EMELT = [
    "viragagyasok",
    "hutohaz",
    "kompatkelo",
    "muhely",
    "arapaly",
    "adagolo",
    "hulladekudvar",
    "zsilip",
    "tuzoltosag",
    "rakododaru",
]


class LaunchCatalogTests(unittest.TestCase):
    def test_launch_set_present(self) -> None:
        ids = {e.template.id for e in discover_exams()}
        for exam_id in LAUNCH_KOZEP + LAUNCH_EMELT:
            self.assertIn(exam_id, ids)

    def test_preamble_is_raw_file_string(self) -> None:
        for loaded in discover_exams():
            if loaded.template.id not in LAUNCH_KOZEP + LAUNCH_EMELT:
                continue
            preamble = loaded.template.preamble or ""
            self.assertIn("f.read()", preamble)
            self.assertNotIn(".append(", preamble)
            header = preamble.split("def ", 1)[0]
            self.assertNotIn("= []", header)

    def test_fogasok_visible_matches_sample(self) -> None:
        loaded = load_exam_by_id("fogasok")
        rows = parse_dataset("fogasok", loaded.visible_content, plugin=loaded.plugin)
        specs = {t.type: t.model_dump() for t in loaded.template.tasks}
        self.assertEqual(
            expected_for_task(rows, specs["fogasok_count"], plugin=loaded.plugin),
            "A fogasok szama: 10",
        )
        self.assertEqual(
            expected_for_task(rows, specs["fogasok_max"], plugin=loaded.plugin),
            "A legnagyobb hal: 15 dkg, 3. a sorban.",
        )
        self.assertEqual(
            expected_for_task(rows, specs["fogasok_threshold"], plugin=loaded.plugin),
            "Kategoria also hatara (dkg):\nLegalabb 10 dkg-os halak szama: 6",
        )
        hidden = parse_dataset("fogasok", loaded.hidden_contents[0], plugin=loaded.plugin)
        self.assertNotEqual(
            expected_for_task(hidden, specs["fogasok_max"], plugin=loaded.plugin),
            "A legnagyobb hal: 15 dkg, 3. a sorban.",
        )

    def test_hutohaz_visible_and_missing_product(self) -> None:
        loaded = load_exam_by_id("hutohaz")
        rows = parse_dataset("hutohaz", loaded.visible_content, plugin=loaded.plugin)
        specs = {t.type: t.model_dump() for t in loaded.template.tasks}
        self.assertEqual(
            expected_for_task(rows, specs["hutohaz_keszlet"], plugin=loaded.plugin),
            "Ora:\nPerc:\nA hutohazban ekkor 63 lada volt.",
        )
        hidden = parse_dataset("hutohaz", loaded.hidden_contents[2], plugin=loaded.plugin)
        out = expected_for_task(hidden, specs["hutohaz_termek"], plugin=loaded.plugin)
        self.assertIn("Nincs ilyen termek.", out)

    def test_sorsjegy_seeded_draw(self) -> None:
        loaded = load_exam_by_id("sorsjegy")
        rows = parse_dataset("sorsjegy", loaded.visible_content, plugin=loaded.plugin)
        spec = next(t.model_dump() for t in loaded.template.tasks if t.type == "sorsjegy_szamok")
        self.assertEqual(
            expected_for_task(rows, spec, plugin=loaded.plugin),
            "A nyero szamok: 7 30 6 1 42 21 26 41",
        )

    def test_new_solution_files_are_prefixed(self) -> None:
        skip = {
            "cities",
            "versenyido",
            "kerekparallomas",
            "viragagyasok",
            "trains",
            "temperatures",
            "students",
            "mrz-kod",
        }
        for loaded in discover_exams():
            if loaded.template.id in skip:
                continue
            for task in loaded.template.tasks:
                if task.solution_file:
                    self.assertTrue(
                        task.solution_file.startswith(loaded.template.id + "_"),
                        task.solution_file,
                    )


if __name__ == "__main__":
    unittest.main()
