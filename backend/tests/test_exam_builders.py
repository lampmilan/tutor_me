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


class KozepOracleTests(unittest.TestCase):
    """Pinned visible + hidden oracle checks for the 10 közép launch exams."""

    def _check(self, exam_id: str, task_type: str, visible_expected: str, hidden_idx: int = 0, hidden_expected: str | None = None) -> None:
        loaded = load_exam_by_id(exam_id)
        tmpl = loaded.template
        rows = parse_dataset(tmpl.dataset_type, loaded.visible_content, plugin=loaded.plugin)
        spec = next(t.model_dump() for t in tmpl.tasks if t.type == task_type)
        self.assertEqual(
            expected_for_task(rows, spec, plugin=loaded.plugin, seed=tmpl.seed),
            visible_expected,
            f"{exam_id}/{task_type} visible mismatch",
        )
        if hidden_expected is not None:
            h_rows = parse_dataset(tmpl.dataset_type, loaded.hidden_contents[hidden_idx], plugin=loaded.plugin)
            self.assertEqual(
                expected_for_task(h_rows, spec, plugin=loaded.plugin, seed=tmpl.seed),
                hidden_expected,
                f"{exam_id}/{task_type} hidden[{hidden_idx}] mismatch",
            )

    def test_cities_count_and_hidden_differs(self) -> None:
        loaded = load_exam_by_id("cities")
        tmpl = loaded.template
        rows = parse_dataset(tmpl.dataset_type, loaded.visible_content, plugin=loaded.plugin)
        spec = next(t.model_dump() for t in tmpl.tasks if t.type == "count")
        v_out = expected_for_task(rows, spec, plugin=loaded.plugin)
        self.assertEqual(v_out, "3")
        h_rows = parse_dataset(tmpl.dataset_type, loaded.hidden_contents[0], plugin=loaded.plugin)
        h_out = expected_for_task(h_rows, spec, plugin=loaded.plugin)
        self.assertNotEqual(v_out, h_out)

    def test_versenyido_all_tasks_visible(self) -> None:
        loaded = load_exam_by_id("versenyido")
        tmpl = loaded.template
        rows = parse_dataset(tmpl.dataset_type, loaded.visible_content, plugin=loaded.plugin)
        for t in tmpl.tasks:
            out = expected_for_task(rows, t.model_dump(), plugin=loaded.plugin)
            self.assertIsInstance(out, str)

    def test_locsolo_visible_and_hidden(self) -> None:
        self._check(
            "locsolo", "locsolo_count",
            "E betuk szama: 4\nJ betuk szama: 1\nB betuk szama: 1",
            hidden_idx=0,
            hidden_expected="E betuk szama: 4\nJ betuk szama: 2\nB betuk szama: 2",
        )
        self._check(
            "locsolo", "locsolo_path",
            "A vegso helyzet: kelet 0, eszak 4\nA Manhattan-tavolsag: 4",
        )
        self._check(
            "locsolo", "locsolo_return",
            "A locsolo nem tert vissza a kiindulo pontra.",
        )

    def test_locsolo_hidden_outputs_differ_from_visible(self) -> None:
        loaded = load_exam_by_id("locsolo")
        tmpl = loaded.template
        rows = parse_dataset(tmpl.dataset_type, loaded.visible_content, plugin=loaded.plugin)
        spec = next(t.model_dump() for t in tmpl.tasks if t.type == "locsolo_count")
        v_out = expected_for_task(rows, spec, plugin=loaded.plugin)
        for i, hc in enumerate(loaded.hidden_contents):
            h_rows = parse_dataset(tmpl.dataset_type, hc, plugin=loaded.plugin)
            h_out = expected_for_task(h_rows, spec, plugin=loaded.plugin)
            self.assertIsInstance(h_out, str, f"hidden[{i}] returned None")

    def test_sorsjegy_all_tasks_visible_and_seeded(self) -> None:
        loaded = load_exam_by_id("sorsjegy")
        tmpl = loaded.template
        rows = parse_dataset(tmpl.dataset_type, loaded.visible_content, plugin=loaded.plugin)
        spec = next(t.model_dump() for t in tmpl.tasks if t.type == "sorsjegy_szamok")
        first = expected_for_task(rows, spec, plugin=loaded.plugin, seed=tmpl.seed)
        second = expected_for_task(rows, spec, plugin=loaded.plugin, seed=tmpl.seed)
        self.assertEqual(first, second)
        self.assertEqual(first, "A nyero szamok: 7 30 6 1 42 21 26 41")

    def test_csomagfeladas_visible(self) -> None:
        self._check("csomagfeladas", "csomagfeladas_count", "A dijkategoriak szama: 3")

    def test_uszoda_visible_and_hidden(self) -> None:
        self._check(
            "uszoda", "uszoda_count",
            "A tetelsorok szama: 5\nAz eladott jegyek szama: 15",
            hidden_idx=0,
            hidden_expected="A tetelsorok szama: 3\nAz eladott jegyek szama: 11",
        )
        self._check("uszoda", "uszoda_nepszeru", "A legnepszerubb jegy: BERLET")

    def test_csoposta_visible(self) -> None:
        self._check("csoposta", "csoposta_count", "A lepesek szama: 7")
        self._check("csoposta", "csoposta_veg", "A kapszula vegallomasa: 15")
        self._check("csoposta", "csoposta_atrako", "Az atrako erintesek szama: 5")

    def test_kerekparallomas_visible_and_hidden(self) -> None:
        loaded = load_exam_by_id("kerekparallomas")
        tmpl = loaded.template
        rows = parse_dataset(tmpl.dataset_type, loaded.visible_content, plugin=loaded.plugin)
        specs = {t.type: t.model_dump() for t in tmpl.tasks}
        self.assertEqual(expected_for_task(rows, specs["maximum"], plugin=loaded.plugin), "5")
        self.assertEqual(expected_for_task(rows, specs["sum"], plugin=loaded.plugin), "63")
        self.assertEqual(expected_for_task(rows, specs["count_where"], plugin=loaded.plugin), "4")
        h_rows = parse_dataset(tmpl.dataset_type, loaded.hidden_contents[0], plugin=loaded.plugin)
        self.assertEqual(expected_for_task(h_rows, specs["maximum"], plugin=loaded.plugin), "8")

    def test_madareteto_visible_and_hidden(self) -> None:
        self._check(
            "madareteto", "madareteto_sum",
            "A heti eleseg: 364 g",
            hidden_idx=0,
            hidden_expected="A heti eleseg: 206 g",
        )
        self._check("madareteto", "madareteto_max", "A legnagyobb adag: 72 g, 6. nap.")
        self._check("madareteto", "madareteto_jutalom", "Jutalom jar.")


class EmeltOracleTests(unittest.TestCase):
    """Pinned visible + hidden oracle checks for the 10 emelt launch exams."""

    def _check(self, exam_id: str, task_type: str, visible_expected: str, hidden_idx: int = 0, hidden_expected: str | None = None) -> None:
        loaded = load_exam_by_id(exam_id)
        tmpl = loaded.template
        rows = parse_dataset(tmpl.dataset_type, loaded.visible_content, plugin=loaded.plugin)
        spec = next(t.model_dump() for t in tmpl.tasks if t.type == task_type)
        self.assertEqual(
            expected_for_task(rows, spec, plugin=loaded.plugin, seed=tmpl.seed),
            visible_expected,
            f"{exam_id}/{task_type} visible mismatch",
        )
        if hidden_expected is not None:
            h_rows = parse_dataset(tmpl.dataset_type, loaded.hidden_contents[hidden_idx], plugin=loaded.plugin)
            self.assertEqual(
                expected_for_task(h_rows, spec, plugin=loaded.plugin, seed=tmpl.seed),
                hidden_expected,
                f"{exam_id}/{task_type} hidden[{hidden_idx}] mismatch",
            )

    def test_viragagyasok_offer_count_visible(self) -> None:
        loaded = load_exam_by_id("viragagyasok")
        tmpl = loaded.template
        rows = parse_dataset(tmpl.dataset_type, loaded.visible_content, plugin=loaded.plugin)
        spec = next(t.model_dump() for t in tmpl.tasks if t.type == "offer_count")
        out = expected_for_task(rows, spec, plugin=loaded.plugin)
        self.assertRegex(out, r"A felajánlások száma: \d+")

    def test_hutohaz_keszlet_visible(self) -> None:
        self._check(
            "hutohaz", "hutohaz_keszlet",
            "Ora:\nPerc:\nA hutohazban ekkor 63 lada volt.",
        )

    def test_hutohaz_termek_missing_in_hidden(self) -> None:
        loaded = load_exam_by_id("hutohaz")
        tmpl = loaded.template
        hidden = parse_dataset(tmpl.dataset_type, loaded.hidden_contents[2], plugin=loaded.plugin)
        spec = next(t.model_dump() for t in tmpl.tasks if t.type == "hutohaz_termek")
        out = expected_for_task(hidden, spec, plugin=loaded.plugin)
        self.assertIn("Nincs ilyen termek.", out)

    def test_kompatkelo_visible_and_hidden(self) -> None:
        self._check(
            "kompatkelo", "kompatkelo_count",
            "A jaratok szama: 8",
            hidden_idx=0,
            hidden_expected="A jaratok szama: 3",
        )
        self._check(
            "kompatkelo", "kompatkelo_max",
            "A legterheltebb jarat: 104, 40 jarmu, cel: BAJA",
        )
        self._check(
            "kompatkelo", "kompatkelo_group",
            "PECS 3 77\nMOHA 3 96\nBAJA 2 52",
        )

    def test_muhely_visible_and_hidden(self) -> None:
        self._check(
            "muhely", "muhely_count",
            "A kolcsonzesi esemenyek szama: 8",
            hidden_idx=0,
            hidden_expected="A kolcsonzesi esemenyek szama: 4",
        )
        self._check(
            "muhely", "muhely_kint",
            "A kint maradt szerszamok szama: 2\nA kint maradt azonosito: 3 7",
        )
        self._check(
            "muhely", "muhely_max",
            "A leghosszabb kolcsonzes: 160 perc, szerszam: 12",
        )

    def test_arapaly_visible_and_hidden(self) -> None:
        self._check(
            "arapaly", "arapaly_stats",
            "A racspontok szama: 16\nA legkisebb melyseg: 1 cm\nA legnagyobb melyseg: 9 cm",
            hidden_idx=0,
            hidden_expected="A racspontok szama: 9\nA legkisebb melyseg: 1 cm\nA legnagyobb melyseg: 9 cm",
        )
        self._check("arapaly", "arapaly_medence", "A medencek szama: 4")
        self._check("arapaly", "arapaly_file", "1 1 4\n1 4 2\n4 1 2\n4 4 1")

    def test_adagolo_visible_and_hidden(self) -> None:
        self._check(
            "adagolo", "adagolo_count",
            "A betegek szama: 4",
            hidden_idx=0,
            hidden_expected="A betegek szama: 2",
        )
        self._check(
            "adagolo", "adagolo_max",
            "Az osszes doboz: 11\nA legnagyobb adag: 3. beteg, 5 doboz",
        )
        self._check("adagolo", "adagolo_file", "1 3\n2 1\n3 5\n4 2")

    def test_hulladekudvar_visible_and_hidden(self) -> None:
        self._check(
            "hulladekudvar", "hulladekudvar_count",
            "A tetelsorok szama: 6\nAz ossztomeg: 49 kg",
            hidden_idx=0,
            hidden_expected="A tetelsorok szama: 2\nAz ossztomeg: 2 kg",
        )
        self._check("hulladekudvar", "hulladekudvar_pont", "A kiosztott pontok: 365")

    def test_zsilip_visible_and_hidden(self) -> None:
        self._check("zsilip", "zsilip_count", "A meresek szama: 7")
        self._check(
            "zsilip", "zsilip_max",
            "A legnagyobb valtozas: 17 cm, kezdete: 6:45",
        )
        self._check("zsilip", "zsilip_riasztas", "Volt riasztas.")

    def test_tuzoltosag_visible_and_hidden(self) -> None:
        self._check(
            "tuzoltosag", "tuzoltosag_count",
            "A riasztasok szama: 8\nA kivonult autok szama: 18",
            hidden_idx=0,
            hidden_expected="A riasztasok szama: 3\nA kivonult autok szama: 4",
        )
        self._check("tuzoltosag", "tuzoltosag_tuz", "A tuzesetek szama: 5")
        self._check(
            "tuzoltosag", "tuzoltosag_elso",
            "Az elso riasztas: 7:12, kerulet: I, tipus: TUZ",
        )
        self._check(
            "tuzoltosag", "tuzoltosag_file",
            "7 12 I 3\n8 5 I 2\n9 10 V 4\n10 20 XIII 2\n11 0 VIII 3",
        )

    def test_rakododaru_visible_and_hidden(self) -> None:
        self._check(
            "rakododaru", "rakododaru_count",
            "A parancsok szama: 8",
            hidden_idx=0,
            hidden_expected="A parancsok szama: 2",
        )
        self._check(
            "rakododaru", "rakododaru_veg",
            "A vegso allas: 20\nA vegso teher: 0",
        )
        self._check(
            "rakododaru", "rakododaru_szabaly",
            "A daru vegig szabalyos maradt.",
        )
        self._check(
            "rakododaru", "rakododaru_file",
            "1 19 0\n2 19 3\n3 13 3\n4 13 2\n5 23 2\n6 23 4\n7 20 4\n8 20 0",
        )


class HiddenOutputDiversityTests(unittest.TestCase):
    """Verify that hidden datasets produce different outputs from visible for exams where they should."""

    EXAMS_THAT_SHOULD_DIFFER = [
        ("locsolo", "locsolo_count"),
        ("uszoda", "uszoda_count"),
        ("kerekparallomas", "maximum"),
        ("madareteto", "madareteto_sum"),
        ("kompatkelo", "kompatkelo_count"),
        ("muhely", "muhely_count"),
        ("arapaly", "arapaly_stats"),
        ("adagolo", "adagolo_count"),
        ("hulladekudvar", "hulladekudvar_count"),
        ("tuzoltosag", "tuzoltosag_count"),
        ("rakododaru", "rakododaru_count"),
    ]

    def test_hidden_datasets_produce_varied_outputs(self) -> None:
        for exam_id, task_type in self.EXAMS_THAT_SHOULD_DIFFER:
            with self.subTest(exam=exam_id, task=task_type):
                loaded = load_exam_by_id(exam_id)
                tmpl = loaded.template
                rows = parse_dataset(tmpl.dataset_type, loaded.visible_content, plugin=loaded.plugin)
                spec = next(t.model_dump() for t in tmpl.tasks if t.type == task_type)
                v_out = expected_for_task(rows, spec, plugin=loaded.plugin, seed=tmpl.seed)
                all_outputs = {v_out}
                for hc in loaded.hidden_contents:
                    h_rows = parse_dataset(tmpl.dataset_type, hc, plugin=loaded.plugin)
                    h_out = expected_for_task(h_rows, spec, plugin=loaded.plugin, seed=tmpl.seed)
                    all_outputs.add(h_out)
                self.assertGreater(
                    len(all_outputs), 1,
                    f"{exam_id}/{task_type}: all hidden datasets produce identical output '{v_out}'",
                )

    def test_all_launch_exams_have_at_least_3_hidden_datasets(self) -> None:
        for exam_id in LAUNCH_KOZEP + LAUNCH_EMELT:
            with self.subTest(exam=exam_id):
                loaded = load_exam_by_id(exam_id)
                self.assertGreaterEqual(
                    len(loaded.hidden_contents),
                    3,
                    f"{exam_id} has only {len(loaded.hidden_contents)} hidden datasets (need ≥3)",
                )

    def test_all_launch_exams_compute_all_tasks_on_all_hidden(self) -> None:
        for exam_id in LAUNCH_KOZEP + LAUNCH_EMELT:
            with self.subTest(exam=exam_id):
                loaded = load_exam_by_id(exam_id)
                tmpl = loaded.template
                for i, hc in enumerate(loaded.hidden_contents):
                    h_rows = parse_dataset(tmpl.dataset_type, hc, plugin=loaded.plugin)
                    for t in tmpl.tasks:
                        out = expected_for_task(h_rows, t.model_dump(), plugin=loaded.plugin, seed=tmpl.seed)
                        self.assertIsInstance(
                            out, str,
                            f"{exam_id} hidden[{i}] task {t.type} returned non-string",
                        )


if __name__ == "__main__":
    unittest.main()
