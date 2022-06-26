import os
import random
import argparse
from bavarian_hunting_lodge_mission import rooms, characters, general


class Murdererer:
    def __init__(self, rooms_list, persons_list, general_info):
        self.general = general_info
        self.rooms = rooms_list
        self.persons = persons_list

        self.person_room_inds = None
        self.num_hours = 5

    @property
    def num_persons(self):
        return len(self.persons)

    def clock_time(self, index):
        return index + 8

    def generate_game(self, out_path):
        random.seed()

        # Randomize rooms, persons and when persons go to rooms
        random.shuffle(self.rooms)
        random.shuffle(self.persons)

        self.person_room_inds = [[0, 0, 0, 3, 1],
                                 [2, 1, 1, 1, 4],
                                 [0, 3, 2, 2, 2],
                                 [3, 1, 4, 3, 3],
                                 [4, 4, 2, 0, 4]]

        clock_roll = random.randint(0, self.num_hours - 1)
        self.person_room_inds = self.person_room_inds[clock_roll:] + self.person_room_inds[:clock_roll]

        # Setup murders
        self.murder_time_index = random.randint(0, self.num_hours - 1)

        solo_person_inds_by_time = {}
        group_person_inds_by_time = {}
        self.minor_crime_witness_person_inds_by_time = {}

        minor_crime_room_ind_list = []
        minor_crime_person_ind_list = []
        witness_person_ind_list = []
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
                witness_person_index = group_person_inds_by_time[time_index][1]
                self.minor_crime_witness_person_inds_by_time[time_index] = (minor_crime_person_index,
                                                                            witness_person_index)
                minor_crime_room_ind_list.append(self.person_room_inds[time_index][minor_crime_person_index])
                minor_crime_person_ind_list.append(minor_crime_person_index)
                witness_person_ind_list.append(witness_person_index)

        # Select witnesses to see minor crime and (and thus alabis for those times)
        for time_index in range(0, self.num_hours):

            # Find a witness who hasn't seen anything
            gpi = 0
            while group_person_inds_by_time[time_index][gpi] in witness_person_ind_list:
                gpi += 1

                # Should have a witness at every time_index, even if person has been a witness before
                if gpi >= len(group_person_inds_by_time[time_index]):
                    gpi = 0
                    break
            witness_person_ind_list.append(group_person_inds_by_time[time_index][gpi])

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
            minor_crime_room_ind_list.append(self.person_room_inds[time_index][solo_person_ind])
            minor_crime_person_ind_list.append(solo_person_ind)

            # Each entry is encoded as (purpetrator, witness)
            self.minor_crime_witness_person_inds_by_time[time_index] = (solo_person_inds_by_time[time_index][spi],
                                                                        group_person_inds_by_time[time_index][gpi])

        minor_crime_witness_person_inds = list(range(0, self.num_persons))
        random.shuffle(minor_crime_witness_person_inds)

        # For each person, add a clue for each solo room that they didn't commit murder or minor crime in
        minor_crime_witness_index = 0
        for person_ind in range(0, self.num_persons):
            for time_index in range(0, self.num_hours):
                if person_ind in solo_person_inds_by_time[time_index] and \
                   not(person_ind == self.murder_person_index and time_index == self.murder_time_index) and \
                   (time_index not in self.minor_crime_witness_person_inds_by_time or
                    person_ind != self.minor_crime_witness_person_inds_by_time[time_index][0]):

                    if person_ind not in self.person_clue_room_inds:
                        self.person_clue_room_inds[person_ind] = []

                    # Make sure the witness of the clue is the person who the clue is about
                    if person_ind == minor_crime_witness_person_inds[minor_crime_witness_index]:
                        minor_crime_witness_index = (1 + minor_crime_witness_index) % self.num_persons

                    # Make a witness person id, room id pair
                    witness_room_ind_pair = (minor_crime_witness_person_inds[minor_crime_witness_index],
                                             self.person_room_inds[time_index][person_ind])
                    minor_crime_witness_index = (1 + minor_crime_witness_index) % self.num_persons
                    self.person_clue_room_inds[person_ind].append(witness_room_ind_pair)

        # TODO: write each character's sheet
        for person_ind in range(0, self.num_persons):
            self._write_character_sheet(person_ind, print_text=True)

        self._print_person_rooms()

        print("Murder at %d o'clock in the %s by %s" % (self.clock_time(self.murder_time_index),
                                                        self.rooms[murder_room_index]['name'],
                                                        self.persons[self.murder_person_index]['name']))

    def _write_character_sheet(self, person_ind, print_text=False):
        new_line_chr = "\n"
        murder_room_ind = self.person_room_inds[self.murder_time_index][self.murder_person_index]

        sheet_str = self.persons[person_ind]['name'] + new_line_chr
        sheet_str += self.persons[person_ind]['description'] % (self.persons[person_ind]['name']) + "\n"

        sheet_str += self.general['phase1'] + "\n"
        sheet_str += self.general['intro'] + "\n"

        other_names = [self.persons[i]['name'] for i in range(0, self.num_persons) if i != person_ind]
        sheet_str += self.general['arrival'] % (other_names[0], other_names[1], other_names[2], other_names[3]) + "\n"
        sheet_str += self.persons[person_ind]['motive'] + new_line_chr + "\n"

        sheet_str += self.general['phase2'] + "\n"
        sheet_str += "* " + self.general['dinner'] + new_line_chr

        for time_index in range(0, self.num_hours):
            clock_time = self.clock_time(time_index)
            room_ind = self.person_room_inds[time_index][person_ind]

            solo_room_inds, group_room_inds = self._get_solo_and_group_inds_for_time(self.person_room_inds[time_index])

            sheet_str += "* "

            # Room description
            if room_ind in solo_room_inds:
                sheet_str += self.rooms[room_ind]['alone'] % (clock_time)
            elif room_ind in group_room_inds:
                other_person_inds = [pi for pi, ri in enumerate(self.person_room_inds[time_index])
                                     if pi != person_ind and ri == room_ind]
                assert len(other_person_inds) == 2

                room_text = self.rooms[room_ind]['group'] % (clock_time,
                                                             self.persons[other_person_inds[0]]['name'],
                                                             self.persons[other_person_inds[1]]['name'])
                sheet_str += room_text
            else:
                assert False

            if room_ind != murder_room_ind:
                # If this isn't the murder room, its always pre-murder
                sheet_str += " " + self.rooms[room_ind]['pre_murder']
            else:
                if time_index < self.murder_time_index:
                    sheet_str += " " + self.rooms[room_ind]['pre_murder']
                elif person_ind == self.murder_person_index and self.murder_time_index == time_index:
                    sheet_str += " " + self.rooms[room_ind]['murder']
                else:
                    sheet_str += " " + self.rooms[room_ind]['post_murder']

            minor_crimes_time_ind_by_room_ind = self._get_minor_crimes_time_ind_by_room_ind()
            if time_index in self.minor_crime_witness_person_inds_by_time and \
                    self.minor_crime_witness_person_inds_by_time[time_index][0] == person_ind:
                sheet_str += " " + self.rooms[room_ind]['minor_crime']
            elif room_ind in minor_crimes_time_ind_by_room_ind and time_index > minor_crimes_time_ind_by_room_ind[room_ind]:
                sheet_str += " " + self.rooms[room_ind]['post_minor_crime']
            else:
                sheet_str += " " + self.rooms[room_ind]['pre_minor_crime']

            if time_index in self.minor_crime_witness_person_inds_by_time and \
                    self.minor_crime_witness_person_inds_by_time[time_index][1] == person_ind:
                other_person_ind = self.minor_crime_witness_person_inds_by_time[time_index][0]
                other_room_ind = self.person_room_inds[time_index][other_person_ind]

                if time_index < self.murder_time_index:
                    sheet_str += " " + self.rooms[other_room_ind]['witness_pre_murder'] % (self.persons[other_person_ind]['name'])
                else:
                    sheet_str += " " + self.rooms[other_room_ind]['witness_post_murder'] % (self.persons[other_person_ind]['name'])

            sheet_str += new_line_chr

        # Describe murder
        murder_room_index = self.person_room_inds[self.murder_time_index][self.murder_person_index]
        sheet_str += "* " + self.general['discovery']
        sheet_str += " " + self.rooms[murder_room_index]['body_found']
        sheet_str += new_line_chr + "\n"
        sheet_str += self.general['npc_alibi']

        # Print clues
        for other_person_ind in range(0, self.num_persons):
            witness_room_pairs = self.person_clue_room_inds[other_person_ind]
            for wi, ri in witness_room_pairs:
                if wi == person_ind:
                    sheet_str += " " + self.rooms[ri]['clue'] % (self.persons[other_person_ind]['name']) + "\n"

        sheet_str += self.general['mission']
        sheet_str += new_line_chr
        if print_text:
            print(sheet_str)

        with(open(self.persons[person_ind]['name'] + ".txt", 'w')) as f:
            f.write(sheet_str)
        return sheet_str

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

                    if self.minor_crime_witness_person_inds_by_time[time_ind][1] == person_ind:
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

    return parser


if __name__ == "__main__":
    args = create_parser().parse_args()
    murdererer = Murdererer(rooms_list=rooms, persons_list=characters, general_info=general)
    murdererer.generate_game(args.out_path)