import os
import json
import random
import argparse
from bavarian_hunting_lodge_mission import rooms, characters, general

# Room index for each person (columns) at each hour (rows). Every hour has one group of three and two people
# alone, and everyone is alone twice in different rooms.
TIMETABLES = {
    # Everyone visits every room exactly once, so a clue about a room can only come from a solo visit.
    "easy": [[0, 0, 0, 1, 2],
             [1, 1, 3, 0, 1],
             [2, 4, 2, 2, 0],
             [4, 3, 1, 3, 3],
             [3, 2, 4, 4, 4]],
    # Everyone has one solo room they also visit with a group, so a clue about that room is ambiguous.
    "hard": [[0, 0, 0, 3, 1],
             [2, 1, 1, 1, 4],
             [0, 3, 2, 2, 2],
             [3, 1, 4, 3, 3],
             [4, 4, 2, 0, 4]],
}


class Murdererer:
    def __init__(self, rooms_list, persons_list, general_info, difficulty="hard"):
        if difficulty not in TIMETABLES:
            raise ValueError("difficulty must be one of %s" % sorted(TIMETABLES))
        self.general = general_info
        self.rooms = rooms_list
        self.persons = persons_list
        self.difficulty = difficulty

        self.person_room_inds = None
        self.num_hours = 5

    @property
    def num_persons(self):
        return len(self.persons)

    def clock_time(self, index):
        return index + 7

    def generate_game(self, out_path):
        random.seed()

        # Randomize rooms, persons and when persons go to rooms
        random.shuffle(self.rooms)
        random.shuffle(self.persons)

        self.person_room_inds = [list(row) for row in TIMETABLES[self.difficulty]]

        clock_roll = random.randint(0, self.num_hours - 1)
        self.person_room_inds = self.person_room_inds[clock_roll:] + self.person_room_inds[:clock_roll]

        # Setup murders
        self.murder_time_index = random.randint(0, self.num_hours - 1)

        solo_person_inds_by_time = {}
        group_person_inds_by_time = {}
        self.minor_crime_witness_person_inds_by_time = {}

        minor_crime_room_ind_list = []
        minor_crime_person_ind_list = []
        times_witnessed_by_person_ind = dict((pi, 0) for pi in range(0, self.num_persons))
        self.person_clue_room_inds = {}

        for time_index in range(0, self.num_hours):
            solo_room_inds, group_room_inds = self._get_solo_and_group_inds_for_time(self.person_room_inds[time_index])

            solo_person_inds_by_time[time_index] = []
            group_person_inds_by_time[time_index] = []
            for person_index in range(0, self.num_persons):
                room_ind = self.person_room_inds[time_index][person_index]
                if room_ind in solo_room_inds:
                    solo_person_inds_by_time[time_index].append(person_index)
                elif room_ind in group_room_inds:
                    group_person_inds_by_time[time_index].append(person_index)
                else:
                    assert False

            random.shuffle(solo_person_inds_by_time[time_index])
            random.shuffle(group_person_inds_by_time[time_index])

            # Select murderer and murder room
            if time_index == self.murder_time_index:
                self.murder_person_index = solo_person_inds_by_time[time_index][0]
                murder_room_index = self.person_room_inds[time_index][self.murder_person_index]

                # Other solo person at this time gets an alabi
                minor_crime_person_index = solo_person_inds_by_time[time_index][1]
                minor_crime_room_ind_list.append(self.person_room_inds[time_index][minor_crime_person_index])
                minor_crime_person_ind_list.append(minor_crime_person_index)

        # Select minor crimes and witnesses to see them (and thus alabis for those times)
        for time_index in range(0, self.num_hours):
            if time_index == self.murder_time_index:
                minor_crime_person_ind = minor_crime_person_ind_list[0]
            else:
                # Find person for minor crime who has been to a room not already used for a minor crime
                spi = 0
                while spi < len(solo_person_inds_by_time[time_index]):
                    solo_person_ind = solo_person_inds_by_time[time_index][spi]
                    if solo_person_ind == self.murder_person_index or \
                       self.person_room_inds[time_index][solo_person_ind] in minor_crime_room_ind_list or \
                       solo_person_ind in minor_crime_person_ind_list:
                        spi += 1
                    else:
                        break
                if spi >= len(solo_person_inds_by_time[time_index]):
                    continue
                minor_crime_person_ind = solo_person_ind
                minor_crime_room_ind_list.append(self.person_room_inds[time_index][minor_crime_person_ind])
                minor_crime_person_ind_list.append(minor_crime_person_ind)

            # Two of the three people in the group witness the crime, favouring those who have seen the least.
            # At most one of them can be the murderer, so the alibi can't be hidden by the murderer staying quiet.
            witness_person_inds = sorted(group_person_inds_by_time[time_index],
                                         key=lambda pi: times_witnessed_by_person_ind[pi])[:2]
            for witness_person_ind in witness_person_inds:
                times_witnessed_by_person_ind[witness_person_ind] += 1

            # Each entry is encoded as (purpetrator, (witness, witness))
            self.minor_crime_witness_person_inds_by_time[time_index] = (minor_crime_person_ind,
                                                                        tuple(witness_person_inds))

        clue_witness_person_inds = list(range(0, self.num_persons))
        random.shuffle(clue_witness_person_inds)

        # For each person, add a clue for each solo room that they didn't commit murder or minor crime in
        clue_witness_index = 0
        for person_ind in range(0, self.num_persons):
            for time_index in range(0, self.num_hours):
                if person_ind in solo_person_inds_by_time[time_index] and \
                   not(person_ind == self.murder_person_index and time_index == self.murder_time_index) and \
                   (time_index not in self.minor_crime_witness_person_inds_by_time or
                    person_ind != self.minor_crime_witness_person_inds_by_time[time_index][0]):

                    if person_ind not in self.person_clue_room_inds:
                        self.person_clue_room_inds[person_ind] = []

                    # Each clue is noticed by two other people, so the murderer is never the only one to see it
                    clue_witness_inds = []
                    while len(clue_witness_inds) < 2:
                        witness_ind = clue_witness_person_inds[clue_witness_index]
                        clue_witness_index = (1 + clue_witness_index) % self.num_persons
                        if witness_ind != person_ind and witness_ind not in clue_witness_inds:
                            clue_witness_inds.append(witness_ind)

                    # Make a witness person id, room id pair for each witness
                    for witness_ind in clue_witness_inds:
                        self.person_clue_room_inds[person_ind].append(
                            (witness_ind, self.person_room_inds[time_index][person_ind]))

        if out_path and not os.path.isdir(out_path):
            os.makedirs(out_path)
        for person_ind in range(0, self.num_persons):
            self._write_character_sheet(person_ind, out_path, print_text=True)
        self.write_game_json(out_path)

        self._print_person_rooms()

        print("Murder at %d o'clock in the %s by %s" % (self.clock_time(self.murder_time_index),
                                                        self.rooms[murder_room_index]['name'],
                                                        self.persons[self.murder_person_index]['name']))

    def build_character_sheet(self, person_ind):
        """Everything one player is told, as plain data (strings, numbers, lists and dicts)."""
        murder_room_ind = self.person_room_inds[self.murder_time_index][self.murder_person_index]
        minor_crimes_time_ind_by_room_ind = self._get_minor_crimes_time_ind_by_room_ind()
        person = self.persons[person_ind]

        other_names = [self.persons[i]['name'] for i in range(0, self.num_persons) if i != person_ind]
        sheet = {
            'name': person['name'],
            'description': person['description'] % (person['name']),
            'motive': person['motive'],
            'phase1': self.general['phase1'],
            'intro': self.general['intro'],
            'arrival': self.general['arrival'] % (other_names[0], other_names[1], other_names[2], other_names[3]),
            'phase2': self.general['phase2'],
            'dinner': self.general['dinner'],
            'dinner_clock': self.clock_time(-1),
            'hours': [],
            'discovery': self.general['discovery'],
            'discovery_clock': self.clock_time(self.num_hours),
            'body_found': self.rooms[murder_room_ind]['body_found'],
            'npc_alibi': self.general['npc_alibi'],
            'clues': [],
            'mission': self.general['mission'],
        }

        for time_index in range(0, self.num_hours):
            clock_time = self.clock_time(time_index)
            room_ind = self.person_room_inds[time_index][person_ind]
            room = self.rooms[room_ind]

            solo_room_inds, group_room_inds = self._get_solo_and_group_inds_for_time(self.person_room_inds[time_index])

            # Room description
            if room_ind in solo_room_inds:
                with_names = []
                scene = room['alone'] % (clock_time)
            elif room_ind in group_room_inds:
                other_person_inds = [pi for pi, ri in enumerate(self.person_room_inds[time_index])
                                     if pi != person_ind and ri == room_ind]
                assert len(other_person_inds) == 2
                with_names = [self.persons[pi]['name'] for pi in other_person_inds]
                scene = room['group'] % (clock_time, with_names[0], with_names[1])
            else:
                assert False

            secret = None
            if room_ind != murder_room_ind:
                # If this isn't the murder room, its always pre-murder
                murder_state = room['pre_murder']
            elif time_index < self.murder_time_index:
                murder_state = room['pre_murder']
            elif person_ind == self.murder_person_index and self.murder_time_index == time_index:
                murder_state = room['murder']
                secret = 'murder'
            else:
                murder_state = room['post_murder']

            if time_index in self.minor_crime_witness_person_inds_by_time and \
                    self.minor_crime_witness_person_inds_by_time[time_index][0] == person_ind:
                minor_crime_state = room['minor_crime']
                secret = 'minor_crime'
            elif room_ind in minor_crimes_time_ind_by_room_ind and time_index > minor_crimes_time_ind_by_room_ind[room_ind]:
                minor_crime_state = room['post_minor_crime']
            else:
                minor_crime_state = room['pre_minor_crime']

            witnessed = None
            if time_index in self.minor_crime_witness_person_inds_by_time and \
                    person_ind in self.minor_crime_witness_person_inds_by_time[time_index][1]:
                other_person_ind = self.minor_crime_witness_person_inds_by_time[time_index][0]
                other_room_ind = self.person_room_inds[time_index][other_person_ind]
                other_name = self.persons[other_person_ind]['name']

                # Only the murder room, once the murder has happened, shows signs of it
                if other_room_ind != murder_room_ind or time_index < self.murder_time_index:
                    witness_text = self.rooms[other_room_ind]['witness_pre_murder'] % (other_name)
                else:
                    witness_text = self.rooms[other_room_ind]['witness_post_murder'] % (other_name)
                witnessed = {'person': other_name, 'room': self.rooms[other_room_ind]['name'], 'text': witness_text}

            sheet['hours'].append({
                'clock': clock_time,
                'room': room['name'],
                'with': with_names,
                'scene': scene,
                'murder_state': murder_state,
                'minor_crime_state': minor_crime_state,
                'secret': secret,
                'witnessed': witnessed,
            })

        for other_person_ind in range(0, self.num_persons):
            for wi, ri in self.person_clue_room_inds[other_person_ind]:
                if wi == person_ind:
                    other_name = self.persons[other_person_ind]['name']
                    sheet['clues'].append({'person': other_name, 'room': self.rooms[ri]['name'],
                                           'text': self.rooms[ri]['clue'] % (other_name)})
        return sheet

    @staticmethod
    def character_sheet_text(sheet):
        """Render a character sheet built by build_character_sheet as plain text."""
        lines = [sheet['name'], sheet['description'], sheet['phase1'], sheet['intro'], sheet['arrival'],
                 sheet['motive'], "", sheet['phase2'], "* " + sheet['dinner']]
        for hour in sheet['hours']:
            line = "* " + " ".join([hour['scene'], hour['murder_state'], hour['minor_crime_state']])
            if hour['witnessed']:
                line += " " + hour['witnessed']['text']
            lines.append(line)
        lines.append("* " + sheet['discovery'] + " " + sheet['body_found'])
        lines.append("")
        text = "\n".join(lines) + "\n" + sheet['npc_alibi']
        for clue in sheet['clues']:
            text += " " + clue['text'] + "\n"
        return text + sheet['mission'] + "\n"

    def _write_character_sheet(self, person_ind, out_path="", print_text=False):
        sheet_str = self.character_sheet_text(self.build_character_sheet(person_ind))
        if print_text:
            print(sheet_str)

        with(open(os.path.join(out_path, self.persons[person_ind]['name'] + ".txt"), 'w')) as f:
            f.write(sheet_str)
        return sheet_str

    def write_game_json(self, out_path=""):
        """Save every player's sheet and the solution, for render_cards.py."""
        murder_room_ind = self.person_room_inds[self.murder_time_index][self.murder_person_index]
        game = {
            'difficulty': self.difficulty,
            'images': self.general.get('images', {}),
            'solution': {
                'murderer': self.persons[self.murder_person_index]['name'],
                'clock': self.clock_time(self.murder_time_index),
                'room': self.rooms[murder_room_ind]['name'],
            },
            'players': [self.build_character_sheet(pi) for pi in range(0, self.num_persons)],
        }
        with open(os.path.join(out_path, "game.json"), 'w') as f:
            json.dump(game, f, indent=2)
        return game

    def _get_minor_crimes_time_ind_by_room_ind(self):
        minor_crimes_time_ind_by_room_ind = {}
        for time_ind, pair in self.minor_crime_witness_person_inds_by_time.items():
            room_ind = self.person_room_inds[time_ind][pair[0]]
            minor_crimes_time_ind_by_room_ind[room_ind] = time_ind
        return minor_crimes_time_ind_by_room_ind

    def _random_selection(self, _list):
        index = random.randint(0, len(_list))
        return _list[index]

    def _get_solo_and_group_inds_for_time(self, room_inds):
        solo_inds = []
        group_inds = []
        counter = {}
        for room_ind in room_inds:
            counter[room_ind] = 1 if room_ind not in counter else counter[room_ind] + 1

        for index, cnt in counter.items():
            if cnt > 1:
                group_inds.append(index)
            else:
                solo_inds.append(index)

        return solo_inds, group_inds

    def _print_person_rooms(self):
        char_str = "   "
        for char in self.persons:
            char_str += char['name'] + ',\t\t\t\t'
        print(char_str)

        num_minor_crimes = 0

        for time_ind, row in enumerate(self.person_room_inds):
            hour_str = str(self.clock_time(time_ind)) + ': '
            for person_ind, room_ind in enumerate(row):
                if person_ind == self.murder_person_index and time_ind == self.murder_time_index:
                    hour_str += '!'

                if time_ind in self.minor_crime_witness_person_inds_by_time:
                    if self.minor_crime_witness_person_inds_by_time[time_ind][0] == person_ind:
                        hour_str += 'a_'
                        num_minor_crimes += 1

                    if person_ind in self.minor_crime_witness_person_inds_by_time[time_ind][1]:
                        hour_str += 'w_'

                if person_ind in self.person_clue_room_inds:
                    has_clue = len([ri for wi, ri in self.person_clue_room_inds[person_ind] if room_ind == ri]) > 0
                    if has_clue:
                        hour_str += 'c_'

                hour_str += self.rooms[room_ind]['name'] + ',\t\t\t\t\t'
            print(hour_str)

        print(str(num_minor_crimes) + " persons have committed minor crimes")

        for person_ind in range(0, self.num_persons):
            witness_room_pairs = self.person_clue_room_inds[person_ind]
            for wi, ri in witness_room_pairs:
                clue_str = "Clues that " + self.persons[person_ind]['name'] + " was in the "
                clue_str += self.rooms[ri]['name'] + " is seen by " + self.persons[wi]['name'] + "."
                print(clue_str)


def create_parser():
    parser = argparse.ArgumentParser(
        "keypoint_annotation_tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--out_path", "-o", default="", type=str, help="output directory path")
    parser.add_argument("--difficulty", "-d", default="hard", choices=sorted(TIMETABLES),
                        help="easy: clues always point to a solo visit; hard: some clues are ambiguous")

    return parser


if __name__ == "__main__":
    args = create_parser().parse_args()
    murdererer = Murdererer(rooms_list=rooms, persons_list=characters, general_info=general,
                            difficulty=args.difficulty)
    murdererer.generate_game(args.out_path)