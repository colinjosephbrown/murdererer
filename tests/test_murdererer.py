"""Unit tests for the murdererer game generator.

The tests generate many games from fixed seeds and check that:

* the scenario data files contain everything the generator needs;
* the hidden solution (schedule, murder, minor crimes, clues) follows the
  rules of the game;
* every character sheet tells a story that agrees with that solution (no room
  is described as both disturbed and untouched, nobody's sheet mentions a
  murder in the wrong room, etc.);
* pooling the information on the players' sheets singles out the murderer.

Run from the repository root with either:

    python -m unittest discover -s tests -v
    python -m pytest tests
"""
import importlib
import itertools
import json
import os
import random
import shutil
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import murdererer  # noqa: E402
import bavarian_hunting_lodge_mission as bavarian  # noqa: E402
import blackthorn_manor as blackthorn  # noqa: E402

NUM_SEEDS = 100  # per scenario and difficulty
SCENARIOS = [bavarian, blackthorn]
DIFFICULTIES = sorted(murdererer.TIMETABLES)

GENERAL_KEYS = ["intro", "phase1", "arrival", "phase2", "dinner", "discovery",
                "npc_alibi", "mission"]
PERSON_KEYS = ["name", "description", "motive"]
ROOM_KEYS = ["name", "alone", "group", "pre_murder", "murder", "post_murder",
             "pre_minor_crime", "minor_crime", "post_minor_crime", "body_found",
             "witness_pre_murder", "witness_post_murder", "clue"]


class _NullWriter(object):
    def write(self, _):
        pass

    def flush(self):
        pass


class GeneratedGame(object):
    """A game generated from a fixed seed, plus the character sheets it wrote."""

    def __init__(self, seed, scenario=bavarian, difficulty="hard"):
        self.seed = seed
        self.scenario_name = scenario.__name__
        self.difficulty = difficulty
        self.game = murdererer.Murdererer(rooms_list=list(scenario.rooms),
                                          persons_list=list(scenario.characters),
                                          general_info=scenario.general,
                                          difficulty=difficulty)
        self.sheets = self._generate(seed)

    def _generate(self, seed):
        # generate_game() reseeds from system entropy, prints everything and
        # writes the sheets to the current directory, so pin the seed, silence
        # stdout and run in a scratch folder.
        original_seed = random.seed
        original_stdout = sys.stdout
        original_cwd = os.getcwd()
        work_dir = tempfile.mkdtemp(prefix="murdererer_test_")
        try:
            original_seed(seed)
            random.seed = lambda *args, **kwargs: None
            sys.stdout = _NullWriter()
            os.chdir(work_dir)
            self.game.generate_game(work_dir)
            sheets = []
            for person in self.game.persons:
                with open(person["name"] + ".txt") as f:
                    sheets.append(f.read())
            with open("game.json") as f:
                self.game_json = json.load(f)
            return sheets
        finally:
            random.seed = original_seed
            sys.stdout = original_stdout
            os.chdir(original_cwd)
            shutil.rmtree(work_dir, ignore_errors=True)

    @property
    def num_hours(self):
        return self.game.num_hours

    @property
    def num_persons(self):
        return self.game.num_persons

    @property
    def murderer(self):
        return self.game.murder_person_index

    @property
    def murder_time(self):
        return self.game.murder_time_index

    @property
    def murder_room(self):
        return self.room_of(self.murderer, self.murder_time)

    @property
    def minor_crimes(self):
        """{time: (perpetrator, (witness, witness))}"""
        return self.game.minor_crime_witness_person_inds_by_time

    @property
    def clues(self):
        """{subject: [(witness, room), ...]}"""
        return self.game.person_clue_room_inds

    def room_of(self, person, time):
        return self.game.person_room_inds[time][person]

    def occupants(self, room, time):
        return [p for p in range(self.num_persons) if self.room_of(p, time) == room]

    def is_alone(self, person, time):
        return len(self.occupants(self.room_of(person, time), time)) == 1

    def solo_times(self, person):
        return [t for t in range(self.num_hours) if self.is_alone(person, t)]

    def text(self, room, key):
        return self.game.rooms[room][key]

    def name(self, person):
        return self.game.persons[person]["name"]

    def hour_line(self, person, time):
        """The '* ...' line of a sheet describing one hour of the evening."""
        lines = [l for l in self.sheets[person].split("\n") if l.startswith("* ")]
        # The first bullet is dinner; the last is the discovery of the body.
        return lines[1 + time]

    def __str__(self):
        return "%s %s seed=%d (murderer=%s at %d o'clock in the %s)" % (
            self.scenario_name, self.difficulty, self.seed, self.name(self.murderer), self.game.clock_time(self.murder_time),
            self.text(self.murder_room, "name"))


def deduce_suspects(g, clues_prove_solo_visit=True):
    """Return everyone who could be the murderer given what the players know.

    This models the deduction the game is designed around. The murderer shares
    nothing from their sheet and lies freely; every innocent shares their sheet
    truthfully (who they were with, what they witnessed, the clues they noticed
    about others).

    With clues_prove_solo_visit, players read a clue such as "X smells of cigar
    smoke" as showing that X was alone in that room at some point. Without it,
    the clue could equally come from a time X was there with a group.

    A player's hour is verified when someone else vouches for them: being in a
    group, or being witnessed committing a minor crime. A player is a suspect if
    they could have been alone in the murder room, unverified, during the
    window in which the murder could have happened, with every clue about them
    still explained by a different unverified hour.
    """
    murder_room = g.murder_room
    innocents = [p for p in range(g.num_persons) if p != g.murderer]

    # Innocents who visited the murder room saw it before or after the murder.
    seen_before = [t for t in range(g.num_hours) for p in innocents
                   if g.room_of(p, t) == murder_room and t < g.murder_time]
    seen_after = [t for t in range(g.num_hours) for p in innocents
                  if g.room_of(p, t) == murder_room and t > g.murder_time]
    earliest = max(seen_before) + 1 if seen_before else 0
    latest = min(seen_after) - 1 if seen_after else g.num_hours - 1

    # verified[person] = {time: room} for hours someone else vouches for.
    verified = [dict() for _ in range(g.num_persons)]
    for t in range(g.num_hours):
        for p in range(g.num_persons):
            if not g.is_alone(p, t):
                verified[p][t] = g.room_of(p, t)
        if t in g.minor_crimes:
            perpetrator, witnesses = g.minor_crimes[t]
            if any(w != g.murderer for w in witnesses):
                verified[perpetrator][t] = g.room_of(perpetrator, t)

    clue_rooms = [sorted(set(room for witness, room in g.clues.get(p, []) if witness != g.murderer))
                  for p in range(g.num_persons)]

    def room_seen_occupied(person, room, t):
        return any(verified[o].get(t) == room for o in range(g.num_persons) if o != person)

    def could_be_murderer_at(person, t):
        if t in verified[person] or room_seen_occupied(person, murder_room, t):
            return False
        # Every clue needs its own hour, other than the murder hour, that
        # explains it: an unverified hour in which that room was otherwise
        # empty or, if clues might come from group visits, a verified hour there.
        def explains(room, s):
            if s in verified[person]:
                return not clues_prove_solo_visit and verified[person][s] == room
            return not room_seen_occupied(person, room, s)

        other_hours = [s for s in range(g.num_hours) if s != t]
        for hours in itertools.permutations(other_hours, len(clue_rooms[person])):
            if all(explains(room, s) for room, s in zip(clue_rooms[person], hours)):
                return True
        return False

    return set(p for p in range(g.num_persons)
               if any(could_be_murderer_at(p, t) for t in range(earliest, latest + 1)))


class ScenarioDataTest(unittest.TestCase):
    """Each scenario file must provide every key and template the generator uses."""

    def check_scenario(self, module_name):
        scenario = importlib.import_module(module_name)
        num_persons = len(scenario.characters)
        self.assertEqual(num_persons, 5, "the generator only supports 5 players")
        self.assertEqual(len(scenario.rooms), 5, "the schedule uses exactly 5 rooms")

        for key in GENERAL_KEYS:
            self.assertIn(key, scenario.general)
        names = ["Alpha", "Bravo", "Charlie", "Delta"]
        arrival = scenario.general["arrival"] % tuple(names)
        for name in names:
            self.assertIn(name, arrival)

        images = scenario.general.get("images", {})
        self.assertTrue(set(images) <= set(["invitation", "discovery"]), "unknown picture slots %s" % sorted(images))
        for file_name in images.values():
            self.assertTrue(file_name.strip(), "picture file names can't be blank")

        for person in scenario.characters:
            for key in PERSON_KEYS:
                self.assertIn(key, person, "%s is missing %r" % (person.get("name"), key))
            self.assertIn(person["name"], person["description"] % person["name"])
        self.assertEqual(len(set(p["name"] for p in scenario.characters)), num_persons,
                         "character names must be unique")

        for room in scenario.rooms:
            label = room.get("name")
            for key in ROOM_KEYS:
                self.assertIn(key, room, "room %r is missing %r" % (label, key))
            self.assertIn("11", room["alone"] % 11, "room %r 'alone'" % label)
            group = room["group"] % (11, "Alpha", "Bravo")
            for expected in ("11", "Alpha", "Bravo"):
                self.assertIn(expected, group, "room %r 'group'" % label)
            for key in ("witness_pre_murder", "witness_post_murder", "clue"):
                self.assertIn("Alpha", room[key] % "Alpha", "room %r %r" % (label, key))
            for key in ("pre_murder", "murder", "post_murder", "pre_minor_crime",
                        "minor_crime", "post_minor_crime", "body_found"):
                room[key] % ()  # raises TypeError if it has a placeholder
        self.assertEqual(len(set(r["name"] for r in scenario.rooms)), len(scenario.rooms),
                         "room names must be unique")

    def test_bavarian_hunting_lodge_scenario_is_complete(self):
        self.check_scenario("bavarian_hunting_lodge_mission")

    def test_blackthorn_manor_scenario_is_complete(self):
        self.check_scenario("blackthorn_manor")


class TimetableTest(unittest.TestCase):

    def visits(self, timetable, person):
        """(group rooms, solo rooms) a person visits over the evening."""
        group_rooms, solo_rooms = [], []
        for row in timetable:
            room = row[person]
            (solo_rooms if row.count(room) == 1 else group_rooms).append(room)
        return group_rooms, solo_rooms

    def test_easy_timetable_has_everyone_visit_every_room_once(self):
        timetable = murdererer.TIMETABLES["easy"]
        for person in range(len(timetable[0])):
            rooms = [row[person] for row in timetable]
            self.assertEqual(sorted(rooms), list(range(len(timetable))), "person %d" % person)

    def test_hard_timetable_has_everyone_revisit_one_solo_room_with_a_group(self):
        timetable = murdererer.TIMETABLES["hard"]
        for person in range(len(timetable[0])):
            group_rooms, solo_rooms = self.visits(timetable, person)
            self.assertEqual(len(set(group_rooms) & set(solo_rooms)), 1, "person %d" % person)

    def test_unknown_difficulty_is_rejected(self):
        self.assertRaises(ValueError, murdererer.Murdererer, [], [], {}, difficulty="medium")


class _GeneratedGamesTestCase(unittest.TestCase):
    """Shares one batch of seeded games between all the test classes below."""
    _games = None

    @classmethod
    def setUpClass(cls):
        if _GeneratedGamesTestCase._games is None:
            _GeneratedGamesTestCase._games = [GeneratedGame(seed, scenario, difficulty)
                                              for scenario in SCENARIOS
                                              for difficulty in DIFFICULTIES
                                              for seed in range(NUM_SEEDS)]
        cls.games = _GeneratedGamesTestCase._games


class SolutionRulesTest(_GeneratedGamesTestCase):
    """The hidden solution must obey the rules the deduction relies on."""

    def test_each_hour_has_one_group_of_three_and_two_people_alone(self):
        for g in self.games:
            for t in range(g.num_hours):
                sizes = sorted(len(g.occupants(r, t)) for r in set(g.game.person_room_inds[t]))
                self.assertEqual(sizes, [1, 1, 3], "%s hour %d" % (g, t))

    def test_everyone_is_alone_exactly_twice_in_different_rooms(self):
        for g in self.games:
            for p in range(g.num_persons):
                solo_rooms = [g.room_of(p, t) for t in g.solo_times(p)]
                self.assertEqual(len(solo_rooms), 2, "%s %s" % (g, g.name(p)))
                self.assertEqual(len(set(solo_rooms)), 2, "%s %s" % (g, g.name(p)))

    def test_murderer_is_alone_with_the_victim(self):
        for g in self.games:
            self.assertEqual(g.occupants(g.murder_room, g.murder_time), [g.murderer], str(g))

    def test_other_person_alone_during_murder_commits_a_witnessed_minor_crime(self):
        for g in self.games:
            t = g.murder_time
            others_alone = [p for p in range(g.num_persons) if g.is_alone(p, t) and p != g.murderer]
            self.assertIn(t, g.minor_crimes, str(g))
            self.assertEqual([g.minor_crimes[t][0]], others_alone, str(g))

    def test_minor_crimes_are_solo_distinct_and_witnessed_by_two_people_in_a_group(self):
        for g in self.games:
            perpetrators = []
            crime_rooms = []
            for t, (perpetrator, witnesses) in g.minor_crimes.items():
                self.assertNotEqual(perpetrator, g.murderer, str(g))
                self.assertTrue(g.is_alone(perpetrator, t), str(g))
                self.assertEqual(len(set(witnesses)), 2, "%s: crime at hour %d" % (g, t))
                for witness in witnesses:
                    self.assertFalse(g.is_alone(witness, t), str(g))
                perpetrators.append(perpetrator)
                crime_rooms.append(g.room_of(perpetrator, t))
            self.assertEqual(len(set(perpetrators)), len(perpetrators),
                             "%s: someone committed two minor crimes" % g)
            self.assertEqual(len(set(crime_rooms)), len(crime_rooms),
                             "%s: a room was robbed twice" % g)

    def test_every_solo_hour_except_the_murder_has_exactly_one_piece_of_evidence(self):
        for g in self.games:
            for p in range(g.num_persons):
                expected = []
                for t in g.solo_times(p):
                    murdering = (p == g.murderer and t == g.murder_time)
                    witnessed = (t in g.minor_crimes and g.minor_crimes[t][0] == p)
                    if not murdering and not witnessed:
                        expected.append(g.room_of(p, t))
                clue_rooms = set(room for _, room in g.clues.get(p, []))
                self.assertEqual(sorted(clue_rooms), sorted(expected), "%s %s" % (g, g.name(p)))

    def test_every_clue_is_noticed_by_two_other_people(self):
        for g in self.games:
            for subject, pairs in g.clues.items():
                for clue_room in set(room for _, room in pairs):
                    witnesses = [w for w, room in pairs if room == clue_room]
                    self.assertEqual(len(witnesses), 2, "%s %s" % (g, g.name(subject)))
                    self.assertEqual(len(set(witnesses)), 2, "%s %s" % (g, g.name(subject)))
                    self.assertNotIn(subject, witnesses, str(g))

    def test_the_murderer_is_never_the_only_witness(self):
        for g in self.games:
            for _, witnesses in g.minor_crimes.values():
                self.assertTrue(any(w != g.murderer for w in witnesses), str(g))
            for pairs in g.clues.values():
                for clue_room in set(room for _, room in pairs):
                    witnesses = [w for w, room in pairs if room == clue_room]
                    self.assertTrue(any(w != g.murderer for w in witnesses), str(g))

    def test_the_murderer_holds_a_typical_amount_of_evidence(self):
        # If the murderer were never (or always) a witness, counting what each
        # player has seen would give them away. Compare the murderer's average
        # with the average innocent's over all the generated games.
        murderer_total = 0
        innocent_total = 0
        for g in self.games:
            held = [0] * g.num_persons
            for _, witnesses in g.minor_crimes.values():
                for w in witnesses:
                    held[w] += 1
            for pairs in g.clues.values():
                for w, _ in pairs:
                    held[w] += 1
            murderer_total += held[g.murderer]
            innocent_total += sum(held) - held[g.murderer]
        murderer_mean = float(murderer_total) / len(self.games)
        innocent_mean = float(innocent_total) / (len(self.games) * (self.games[0].num_persons - 1))
        self.assertAlmostEqual(murderer_mean, innocent_mean, delta=0.15 * innocent_mean,
                               msg="murderer holds %.2f items on average, innocents %.2f" % (
                                   murderer_mean, innocent_mean))


class CharacterSheetTest(_GeneratedGamesTestCase):
    """The text of every sheet must match the hidden solution and each other."""

    def test_sheets_have_no_unfilled_placeholders(self):
        for g in self.games:
            for p, sheet in enumerate(g.sheets):
                self.assertNotIn("%s", sheet, "%s %s" % (g, g.name(p)))
                self.assertNotIn("%d", sheet, "%s %s" % (g, g.name(p)))

    def test_each_player_is_introduced_to_the_other_four(self):
        for g in self.games:
            for p, sheet in enumerate(g.sheets):
                arrival = [l for l in sheet.split("\n") if "introduced to" in l][0]
                for other in range(g.num_persons):
                    if other != p:
                        self.assertIn(g.name(other), arrival, str(g))

    def test_hour_lines_name_exactly_the_people_you_were_with(self):
        for g in self.games:
            for p in range(g.num_persons):
                for t in range(g.num_hours):
                    room = g.room_of(p, t)
                    clock = g.game.clock_time(t)
                    if g.is_alone(p, t):
                        expected = g.text(room, "alone") % clock
                    else:
                        others = [g.name(o) for o in g.occupants(room, t) if o != p]
                        expected = g.text(room, "group") % (clock, others[0], others[1])
                    self.assertTrue(g.hour_line(p, t).startswith("* " + expected),
                                    "%s %s at hour %d" % (g, g.name(p), t))

    def test_only_the_murderer_reads_the_murder(self):
        for g in self.games:
            murder_text = g.text(g.murder_room, "murder")
            for p, sheet in enumerate(g.sheets):
                self.assertEqual(sheet.count(murder_text), 1 if p == g.murderer else 0, str(g))
                for r in range(len(g.game.rooms)):
                    if r != g.murder_room:
                        self.assertNotIn(g.text(r, "murder"), sheet, str(g))

    def test_everyone_learns_where_the_body_was_found(self):
        for g in self.games:
            for sheet in g.sheets:
                self.assertIn(g.text(g.murder_room, "body_found"), sheet, str(g))

    def test_rooms_look_disturbed_only_after_the_murder_happened_there(self):
        for g in self.games:
            for p in range(g.num_persons):
                for t in range(g.num_hours):
                    line = g.hour_line(p, t)
                    room = g.room_of(p, t)
                    if room == g.murder_room and t == g.murder_time:
                        continue
                    msg = "%s: %s in the %s at hour %d" % (g, g.name(p), g.text(room, "name"), t)
                    if room == g.murder_room and t > g.murder_time:
                        self.assertIn(g.text(room, "post_murder"), line, msg)
                    else:
                        # (post_murder text often extends pre_murder, so only
                        # the absence of post_murder is meaningful here.)
                        self.assertIn(g.text(room, "pre_murder"), line, msg)
                        self.assertNotIn(g.text(room, "post_murder"), line, msg)

    def test_stolen_items_go_missing_only_after_the_theft(self):
        for g in self.games:
            theft_time = {}
            for t, (perpetrator, _) in g.minor_crimes.items():
                theft_time[g.room_of(perpetrator, t)] = t
            for p in range(g.num_persons):
                for t in range(g.num_hours):
                    line = g.hour_line(p, t)
                    room = g.room_of(p, t)
                    msg = "%s: %s in the %s at hour %d" % (g, g.name(p), g.text(room, "name"), t)
                    if t in g.minor_crimes and g.minor_crimes[t][0] == p:
                        self.assertIn(g.text(room, "minor_crime"), line, msg)
                    elif room in theft_time and t > theft_time[room]:
                        self.assertIn(g.text(room, "post_minor_crime"), line, msg)
                    else:
                        self.assertIn(g.text(room, "pre_minor_crime"), line, msg)

    def test_minor_crime_witnesses_see_the_crime_room_in_its_true_state(self):
        # A witness glancing into a room should only see signs of the murder if
        # it is the murder room and the murder has already happened.
        for g in self.games:
            for t, (perpetrator, witnesses) in g.minor_crimes.items():
                room = g.room_of(perpetrator, t)
                after_murder = room == g.murder_room and t > g.murder_time
                key = "witness_post_murder" if after_murder else "witness_pre_murder"
                expected = g.text(room, key) % g.name(perpetrator)
                for witness in witnesses:
                    self.assertIn(expected, g.hour_line(witness, t),
                                  "%s: %s sees %s in the %s at %d o'clock and should read %r" % (
                                      g, g.name(witness), g.name(perpetrator), g.text(room, "name"),
                                      g.game.clock_time(t), key))

    def test_clues_appear_on_the_witness_sheet(self):
        for g in self.games:
            for subject, pairs in g.clues.items():
                for witness, room in pairs:
                    self.assertIn(g.text(room, "clue") % g.name(subject), g.sheets[witness], str(g))


class GameJsonTest(_GeneratedGamesTestCase):
    """game.json holds the same content as the text sheets, in structured form."""

    def test_game_json_renders_to_the_same_text_sheets(self):
        for g in self.games:
            players = g.game_json["players"]
            self.assertEqual([p["name"] for p in players], [g.name(p) for p in range(g.num_persons)], str(g))
            for p, sheet in enumerate(players):
                self.assertEqual(murdererer.Murdererer.character_sheet_text(sheet), g.sheets[p], str(g))

    def test_game_json_records_the_solution(self):
        for g in self.games:
            solution = g.game_json["solution"]
            self.assertEqual(solution["murderer"], g.name(g.murderer), str(g))
            self.assertEqual(solution["clock"], g.game.clock_time(g.murder_time), str(g))
            self.assertEqual(solution["room"], g.text(g.murder_room, "name"), str(g))
            self.assertEqual(g.game_json["difficulty"], g.difficulty, str(g))
            scenario = importlib.import_module(g.scenario_name)
            self.assertEqual(g.game_json["images"], scenario.general.get("images", {}), str(g))

    def test_evening_runs_from_dinner_at_6_to_the_discovery_at_midnight(self):
        for g in self.games:
            for sheet in g.game_json["players"]:
                self.assertEqual(sheet["dinner_clock"], 6, str(g))
                self.assertEqual([h["clock"] for h in sheet["hours"]], [7, 8, 9, 10, 11], str(g))
                self.assertEqual(sheet["discovery_clock"], 12, str(g))

    def test_dinner_and_discovery_text_agree_with_the_schedule(self):
        for g in self.games:
            sheet = g.game_json["players"][0]
            self.assertIn("%d o'clock" % sheet["dinner_clock"], sheet["dinner"], str(g))
            self.assertIn("midnight", sheet["discovery"], str(g))

    def test_only_murders_and_minor_crimes_are_marked_secret(self):
        for g in self.games:
            for p, sheet in enumerate(g.game_json["players"]):
                for t, hour in enumerate(sheet["hours"]):
                    if p == g.murderer and t == g.murder_time:
                        expected = "murder"
                    elif t in g.minor_crimes and g.minor_crimes[t][0] == p:
                        expected = "minor_crime"
                    else:
                        expected = None
                    self.assertEqual(hour["secret"], expected, "%s %s at hour %d" % (g, g.name(p), t))

    def test_hours_record_who_you_were_with(self):
        for g in self.games:
            for p, sheet in enumerate(g.game_json["players"]):
                for t, hour in enumerate(sheet["hours"]):
                    room = g.room_of(p, t)
                    expected = sorted(g.name(o) for o in g.occupants(room, t) if o != p)
                    self.assertEqual(sorted(hour["with"]), expected, str(g))
                    self.assertEqual(hour["room"], g.text(room, "name"), str(g))


class SolvabilityTest(_GeneratedGamesTestCase):

    def assert_only_murderer_suspected(self, g, clues_prove_solo_visit):
        suspects = deduce_suspects(g, clues_prove_solo_visit)
        self.assertEqual(suspects, set([g.murderer]),
                         "%s: suspects are %s" % (g, sorted(g.name(s) for s in suspects)))

    def test_pooled_evidence_identifies_exactly_one_suspect(self):
        for g in self.games:
            self.assert_only_murderer_suspected(g, clues_prove_solo_visit=True)

    def test_easy_games_need_no_assumption_about_what_clues_mean(self):
        for g in self.games:
            if g.difficulty == "easy":
                self.assert_only_murderer_suspected(g, clues_prove_solo_visit=False)

    def test_hard_games_can_be_ambiguous_if_clues_are_misread(self):
        # The hard timetable is only harder if a clue can sometimes be blamed
        # on a group visit, leaving an innocent player under suspicion.
        hard_games = [g for g in self.games if g.difficulty == "hard"]
        ambiguous = [g for g in hard_games if len(deduce_suspects(g, clues_prove_solo_visit=False)) > 1]
        self.assertTrue(ambiguous)


if __name__ == "__main__":
    unittest.main()
