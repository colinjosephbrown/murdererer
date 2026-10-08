"""Unit tests for render_cards.py, the printable card renderer.

Run from the repository root with:

    python -m unittest discover -s tests -v
"""
import io
import os
import re
import shutil
import sys
import tempfile
import unittest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TESTS_DIR)
for path in (REPO_ROOT, TESTS_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

import render_cards  # noqa: E402
from test_murdererer import GeneratedGame, SCENARIOS, DIFFICULTIES  # noqa: E402

NUM_SEEDS = 10  # per scenario and difficulty


def count(pattern, html):
    return len(re.findall(pattern, html))


class RenderDeckTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.games = [GeneratedGame(seed, scenario, difficulty)
                     for scenario in SCENARIOS for difficulty in DIFFICULTIES for seed in range(NUM_SEEDS)]

    def sheets(self):
        for g in self.games:
            for sheet in g.game_json["players"]:
                yield g, sheet

    def expected_card_count(self, sheet):
        # Rules, character, arrival, dinner, five hours, discovery, investigation, then evidence.
        witnessed = len([h for h in sheet["hours"] if h["witnessed"]])
        return 4 + len(sheet["hours"]) + 2 + witnessed + len(sheet["clues"])

    def test_every_piece_of_text_is_on_a_card(self):
        for g, sheet in self.sheets():
            html = render_cards.render_deck(sheet)
            texts = [sheet[k] for k in ("name", "description", "motive", "intro", "arrival", "dinner",
                                        "discovery", "body_found", "npc_alibi", "mission")]
            for hour in sheet["hours"]:
                texts.append(" ".join([hour["scene"], hour["murder_state"], hour["minor_crime_state"]]))
                if hour["witnessed"]:
                    texts.append(hour["witnessed"]["text"])
            texts.extend(clue["text"] for clue in sheet["clues"])
            for text in texts:
                self.assertIn(render_cards.escape(text), html, "%s %s" % (g, sheet["name"]))

    def test_one_card_per_section_hour_and_piece_of_evidence(self):
        for g, sheet in self.sheets():
            html = render_cards.render_deck(sheet, backs=False)
            self.assertEqual(count(r'<div class="card [^"]*"><div class="frame">', html),
                             self.expected_card_count(sheet), "%s %s" % (g, sheet["name"]))

    def test_secret_cards_match_the_sheet(self):
        for g, sheet in self.sheets():
            html = render_cards.render_deck(sheet, backs=False)
            secrets = len([h for h in sheet["hours"] if h["secret"]])
            self.assertEqual(count(r'class="card [^"]*\bsecret-card\b', html), secrets, "%s %s" % (g, sheet["name"]))

    def test_timed_cards_show_their_hour_as_a_background_numeral(self):
        # Dinner, each hour followed by any sighting during it, the discovery and
        # investigation, then each clue (noticed after the discovery), in card order.
        for g, sheet in self.sheets():
            html = render_cards.render_deck(sheet, backs=False)
            numerals = re.findall(r'<div class="card [^"]*"><div class="frame">'
                                  r'<div class="numeral[^"]*" aria-hidden="true">(\d+)</div>', html)
            discovery = sheet["discovery_clock"]
            expected = [sheet["dinner_clock"]]
            for h in sheet["hours"]:
                expected += [h["clock"], h["clock"]] if h["witnessed"] else [h["clock"]]
            expected += [discovery, discovery] + [discovery] * len(sheet["clues"])
            self.assertEqual([int(n) for n in numerals], expected, "%s %s" % (g, sheet["name"]))
            self.assertEqual(count('class="numeral', html), len(expected), str(g))

    def test_each_sighting_card_follows_its_hour_card(self):
        for g, sheet in self.sheets():
            html = render_cards.render_deck(sheet, backs=False)
            fronts = re.findall(r'<div class="card ([^"]*)"><div class="frame">(.*?)<div class="title">(.*?)</div>',
                                html)
            for hour in sheet["hours"]:
                hour_index = [i for i, (cls, kicker, _) in enumerate(fronts)
                              if "hour-card" in cls and ">%d<" % hour["clock"] in kicker][0]
                following = fronts[hour_index + 1]
                if hour["witnessed"]:
                    self.assertIn("evidence-card", following[0], "%s %s" % (g, sheet["name"]))
                    self.assertEqual(following[2], render_cards.escape(hour["witnessed"]["person"]), str(g))
                else:
                    self.assertNotIn("evidence-card", following[0], "%s %s" % (g, sheet["name"]))

    def test_two_digit_numerals_are_sized_to_fit(self):
        html = render_cards.numeral(12) + render_cards.numeral(7)
        self.assertIn('class="numeral two-digit" aria-hidden="true">12<', html)
        self.assertIn('class="numeral" aria-hidden="true">7<', html)
        self.assertEqual(render_cards.numeral(None), "")

    def test_every_page_of_fronts_is_followed_by_a_page_of_backs(self):
        for g, sheet in self.sheets():
            html = render_cards.render_deck(sheet)
            pages = re.findall(r'<section class="sheet( backs)?">(.*?)</section>', html, re.S)
            fronts = [p for kind, p in pages if not kind]
            backs = [p for kind, p in pages if kind]
            self.assertEqual(len(fronts), len(backs), str(g))
            for i, (kind, page) in enumerate(pages):
                self.assertEqual(bool(kind), i % 2 == 1, str(g))
            for front, back in zip(fronts, backs):
                self.assertEqual(count('<div class="card back">', back), count('<div class="frame">', front))
                self.assertLessEqual(count('<div class="frame">', front), render_cards.CARDS_PER_PAGE)

    def test_backs_mirror_a_partly_filled_page(self):
        # Flipped on the long edge, a card in the left column has its back in the right column.
        _, sheet = next(self.sheets())
        html = render_cards.render_deck(sheet)
        last_backs = re.findall(r'<section class="sheet backs">(.*?)</section>', html, re.S)[-1]
        slots = re.findall(r'<div class="card (back|empty)">', last_backs)
        fronts_on_last_page = (self.expected_card_count(sheet) - 1) % render_cards.CARDS_PER_PAGE + 1
        expected = []
        for row in range(render_cards.ROWS):
            for col in range(render_cards.COLUMNS):
                front_index = row * render_cards.COLUMNS + (render_cards.COLUMNS - 1 - col)
                expected.append("back" if front_index < fronts_on_last_page else "empty")
        self.assertEqual(slots, expected)

    def test_no_backs_option_leaves_out_back_pages(self):
        _, sheet = next(self.sheets())
        self.assertNotIn('class="card back"', render_cards.render_deck(sheet, backs=False))

    def test_missing_portrait_shows_a_placeholder(self):
        _, sheet = next(self.sheets())
        html = render_cards.render_deck(sheet, portrait_path=None)
        self.assertIn('class="portrait placeholder"', html)

    def test_text_is_html_escaped(self):
        _, sheet = next(self.sheets())
        sheet = dict(sheet, motive='<b>"Revenge" & more</b>')
        html = render_cards.render_deck(sheet)
        self.assertIn("&lt;b&gt;&quot;Revenge&quot; &amp; more&lt;/b&gt;", html)
        self.assertNotIn("<b>", html)


class PortraitTest(unittest.TestCase):

    def setUp(self):
        self.folder = tempfile.mkdtemp(prefix="murdererer_portraits_")

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def add_file(self, name, data=b"\x89PNG fake image"):
        with open(os.path.join(self.folder, name), "wb") as f:
            f.write(data)

    def test_matches_names_with_underscores_or_inside_longer_file_names(self):
        self.add_file("Matilde_Acosta.jpg")
        self.add_file("A portrait of Hinrich von Wagner, a German general.webp")
        self.assertTrue(render_cards.find_portrait(self.folder, "Matilde Acosta").endswith("Matilde_Acosta.jpg"))
        self.assertTrue(render_cards.find_portrait(self.folder, "Hinrich von Wagner").endswith(".webp"))

    def test_matching_ignores_punctuation_but_not_partial_words(self):
        self.add_file("Dr_Sofia_Devrise.jpg")
        self.add_file("Evan_Palvinson.jpg")
        self.assertTrue(render_cards.find_portrait(self.folder, "Dr. Sofia Devrise").endswith("Dr_Sofia_Devrise.jpg"))
        self.assertIsNone(render_cards.find_portrait(self.folder, "Eva Palvin"))

    def test_missing_portraits_and_non_images_are_ignored(self):
        self.add_file("Eva Palvin notes.txt")
        self.assertIsNone(render_cards.find_portrait(self.folder, "Eva Palvin"))
        self.assertIsNone(render_cards.find_portrait(None, "Eva Palvin"))
        self.assertIsNone(render_cards.find_portrait(os.path.join(self.folder, "missing"), "Eva Palvin"))

    def test_portrait_is_embedded_in_the_deck(self):
        self.add_file("Eva_Palvin.png")
        game = GeneratedGame(0)
        sheet = [s for s in game.game_json["players"] if s["name"] == "Eva Palvin"][0]
        html = render_cards.render_deck(sheet, render_cards.find_portrait(self.folder, "Eva Palvin"))
        self.assertIn('src="data:image/png;base64,', html)
        self.assertNotIn("portrait placeholder", html)


class SceneImageTest(unittest.TestCase):

    def setUp(self):
        self.folder = tempfile.mkdtemp(prefix="murdererer_scenes_")
        for name in ("Residence.jpg", "Host.png"):
            with open(os.path.join(self.folder, name), "wb") as f:
                f.write(b"fake image")
        self.sheet = GeneratedGame(0).game_json["players"][0]

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def card_fronts(self, html):
        return re.findall(r'<div class="card [^"]*"><div class="frame">.*?</div></div>', html, re.S)

    def test_pictures_head_the_invitation_and_discovery_cards(self):
        images = render_cards.find_scene_images(self.folder, {"invitation": "Residence.jpg", "discovery": "Host.png"})
        html = render_cards.render_deck(self.sheet, backs=False, scene_images=images)
        invitation = [c for c in self.card_fronts(html) if "An Invitation" in c][0]
        discovery = [c for c in self.card_fronts(html) if "The Discovery" in c][0]
        self.assertIn('class="scene-image" src="data:image/jpeg;base64,', invitation)
        self.assertIn('class="portrait" src="data:image/png;base64,', discovery)
        self.assertEqual(count("data:image/", html), 2)

    def test_missing_pictures_are_skipped(self):
        stdout = sys.stdout
        sys.stdout = io.StringIO() if sys.version_info[0] >= 3 else io.BytesIO()
        try:
            images = render_cards.find_scene_images(self.folder, {"invitation": "Nowhere.jpg"})
            self.assertEqual(images, {})
            self.assertEqual(render_cards.find_scene_images(None, {"discovery": "Host.png"}), {})
        finally:
            sys.stdout = stdout
        html = render_cards.render_deck(self.sheet, backs=False, scene_images=images)
        self.assertNotIn('class="scene-image"', html)
        self.assertEqual(count("data:image/", html), 0)


class RenderGameTest(unittest.TestCase):

    def test_writes_one_deck_per_player_next_to_game_json(self):
        work_dir = tempfile.mkdtemp(prefix="murdererer_render_")
        try:
            game = GeneratedGame(0)
            game_json_path = os.path.join(work_dir, "game.json")
            import json
            with io.open(game_json_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(game.game_json, ensure_ascii=False))
            paths = render_cards.render_game(game_json_path)
            names = sorted(os.path.basename(p) for p in paths)
            self.assertEqual(names, sorted(s["name"] + ".html" for s in game.game_json["players"]))
            for path in paths:
                self.assertEqual(os.path.dirname(path), os.path.join(work_dir, "cards"))
                with io.open(path, encoding="utf-8") as f:
                    self.assertTrue(f.read().startswith("<!doctype html>"))
        finally:
            shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
