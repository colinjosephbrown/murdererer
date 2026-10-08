# Murdererer

Murdererer generates a tabletop murder-mystery game for **exactly five players**.
Each run produces a new scenario and writes one secret character sheet per player.
Every sheet holds a different slice of the evening. Nobody can solve the murder
alone, but if the players share what they know carefully, the murderer can be
identified with certainty.

## Running it

```sh
python murdererer.py --out_path game1
python render_cards.py game1/game.json --images bavarian_hunting_lodge
```

The first command writes into the `game1` folder (or the current folder if
`--out_path` is left out):

- one `<Character Name>.txt` sheet per player;
- `game.json`, which holds every player's sheet as structured data plus the
  solution, and is what the card renderer reads.

It also prints every sheet, a timetable of the evening and the solution to the
console, so the person running it should not read the console output if they
are also playing.

Choose a difficulty with `--difficulty easy` or `--difficulty hard` (the
default). See [Difficulty](#difficulty) below.

The scenario comes from `bavarian_hunting_lodge_mission.py`. To play
`blackthorn_manor.py` or another scenario instead, change the import at the top
of `murdererer.py`.

### Printable cards

The second command turns `game.json` into one HTML file of cards per player,
written to `game1/cards/`. Open a player's file in a browser and print it:

- **Paper:** A4 or US Letter, at 100% scale ("actual size"), with "background
  graphics" turned on.
- **Double-sided:** print double-sided, flipping on the long edge, so each card
  gets the shared card back. If your printer can't do double-sided, add
  `--no_backs` to leave out the back pages.
- **Cutting:** cut along the dashed lines. Cards are 92 × 127 mm, four to a page.

Each player gets these cards, in order:

1. **How to Play.**
2. **Character:** portrait, description and motive.
3. **An Invitation** and **Dinner.**
4. **One card for each hour** from 7 to 11. Cards describing a murder or minor
   crime have a red frame and are marked *Secret*. If the player witnessed a
   minor crime during an hour, a **sighting** evidence card follows that hour's
   card.
5. **The Discovery** and **The Investigation**, marked "Read last".
6. **Clue** evidence cards: one per clue the player noticed about another guest.

Players can show evidence cards to back up a claim without revealing their whole
evening.

**Pictures:** `--images` points at a folder of pictures (`.jpg`, `.png`,
`.webp` or `.gif`). It used to be called `--portraits`, which still works.

- **Character portraits** are matched by the character's name, ignoring case
  and punctuation, so `Dr_Sofia_Devrise.jpg` or "A portrait of Hinrich von
  Wagner….webp" both work. Characters without one get a placeholder.
- **Scene pictures** are named in the scenario's `general` settings, for
  example `"images": {"invitation": "Bavarian_residence.jpg", "discovery":
  "Count_Ludwig_IV.jpg"}`. The `invitation` picture is cropped to a banner
  across the top of the Invitation card. The `discovery` picture is shown as a
  framed portrait on The Discovery card, which suits the victim. Both are
  optional.

Pictures are embedded in the HTML, so each file stands alone. Keep them to
about 1000 pixels: that's sharper than a home printer can show at card size,
and keeps each deck to about 1 MB. Full-size source images can live in an
`originals/` subfolder, which git ignores.

**Long text:** a card whose text is too long shrinks it to fit. If it still
doesn't fit at the smallest size, the card gets a red outline on screen (not
in print) so you can shorten the scenario text.

**Times:** cards tied to a time of night show that hour as a large, faint
numeral in the background:

- the Dinner card shows 6;
- each hour card shows its hour, 7 to 11;
- each sighting card shows the hour of the sighting;
- the Discovery, Investigation and clue cards show 12.

To change the rules text, edit `RULES` at the top of `render_cards.py`.

## How a game plays out

Each player gets a sheet with three parts:

1. **The Arrival**: who you are, the other four guests, and your secret
   **motive** for killing the host. Every guest has a motive.
2. **The Evening**: dinner at 6 o'clock, then one entry for each hour from
   7 to 11 o'clock saying which room you went to and who, if anyone, was with
   you. It also describes what you noticed in the room and anything you saw
   happening elsewhere.
3. **The Discovery**: at midnight the host's body is found and everyone learns which room
   the murder happened in. The servants are ruled out. Your sheet may also list
   **clues** you noticed about other guests (for example "you notice X smells
   strongly of cigar smoke").

The players then talk. They may tell the truth or lie, but each also has
secrets to protect. The goal is to work out who the murderer is.

## How a scenario is generated

### The schedule

Every hour, the five guests split into **one group of three** and **two people
alone** in separate rooms. Over the five hours, every guest is alone exactly
**twice**, each time in a different room. Each difficulty uses its own fixed
timetable. Each game shuffles which rooms and characters fill it, and which
hour it starts at.

### The murder

An hour is chosen at random, and one of the two people alone at that hour
becomes the murderer. The room they are in becomes the murder room. Their sheet
describes the murder itself. Anyone who visits the murder room before the
murder sees it untouched (`pre_murder` text). Anyone who visits afterwards
notices something off (`post_murder` text), such as a missing dart or a moved
ladder.

### Minor crimes (alibis)

The other person alone at the murder hour is given a **minor crime**, such as
stealing a painting or a rare bottle of wine. Two of the three people in that
hour's group **witness** them leaving the room with the loot. This gives the
minor criminal an alibi, as long as the witnesses speak up or the thief is
willing to admit to the theft.

Further minor crimes are added at other hours where possible. Each minor crime
is committed by a different person, in a different room, and never by the
murderer. Anyone visiting a robbed room afterwards sees the item missing
(`post_minor_crime` text).

### Clues

Every remaining hour that someone spends alone, except the murder itself,
produces a **clue**. Another player notices a physical trace of that room on
the person: chalk from the billiards room, mud from the observatory path, and
so on. The clue goes on the sheets of two other players.

### Why the game is solvable

Group hours are always vouched for by the two other people in the room. That
leaves each guest's two solo hours, and the generator makes sure **every solo
hour is backed by exactly one piece of evidence**: a witnessed minor crime or a
clue on someone else's sheet. The single exception is the murderer's murder
hour, which has no evidence at all.

Every piece of evidence has **two witnesses**, so the murderer is never the
only person who knows it and can't hide someone's alibi by keeping quiet. The
murderer still witnesses things as often as anyone else, so how much a player
has seen doesn't give them away.

So when the innocent guests share their schedules, their companions, what they
witnessed and the clues they hold, every innocent guest can account for both solo hours,
but the murderer can only account for one. Before-and-after descriptions of the
murder room narrow down when the murder happened.

### Difficulty

The two difficulties differ only in the timetable, which changes how much a
clue proves.

- **Easy:** everyone visits every room exactly once. A clue such as "mud on
  their shoes" can only come from a solo visit to the observatory, so it
  directly backs up one of that person's solo hours.
- **Hard:** each guest's two solo rooms include one they also visit with a
  group. A clue about that room might come from the group visit, so players
  have to work out which visit it refers to. Players who take a clue at face
  value can end up suspecting an innocent guest. In testing, that happened in
  about two out of three hard games.

## Writing a new scenario

A scenario is a Python module defining three things:

| Name         | Contents |
|--------------|----------|
| `general`    | Shared story text: `intro`, `phase1`, `arrival` (four `%s` for the other guests' names), `phase2`, `dinner`, `discovery`, `npc_alibi`, `mission`. |
| `characters` | Five dicts with `name`, `description` (one `%s` for the name) and `motive`. |
| `rooms`      | Five dicts, each with the keys below. |

Room keys and their placeholders:

| Key | Placeholders | Used when |
|-----|--------------|-----------|
| `name` | none | Room name |
| `alone` | `%d` hour | You are alone in the room |
| `group` | `%d` hour, `%s`, `%s` other two names | You are in the group of three |
| `pre_murder` / `post_murder` | none | Room state before / after the murder (only differs in the murder room) |
| `murder` | none | Murderer's description of the killing |
| `body_found` | none | How the body is discovered |
| `pre_minor_crime` / `post_minor_crime` | none | Room state before / after its minor crime |
| `minor_crime` | none | The thief's description of the theft |
| `witness_pre_murder` / `witness_post_murder` | `%s` thief's name | What the witness sees |
| `clue` | `%s` guest's name | A trace of this room noticed on another guest |

`tests/test_murdererer.py` checks every scenario module for these keys and placeholders.

## Tests

```sh
python -m unittest discover -s tests -v      # or: python -m pytest tests
```

The tests generate 100 games from fixed seeds for each scenario and difficulty, and check that:

- every scenario file provides every key and template the generator needs;
- the hidden solution follows the rules above (schedule shape, a lone
  murderer, distinct minor crimes, one piece of evidence per solo hour, two
  witnesses for every piece of evidence);
- every character sheet agrees with the solution and with the other sheets
  (correct companions, room states that change only after the event, clues
  delivered to the right player, no leftover `%s`/`%d`);
- pooling the innocent players' information leaves exactly one possible
  suspect, even if the murderer shares nothing. Easy games stay solvable
  even if players think clues might come from group visits, while some hard
  games don't;
- `game.json` holds the same content as the text sheets, with secrets and
  companions recorded correctly;
- every piece of a player's sheet appears on one of their cards, each front
  page is followed by a matching page of backs, and pictures are matched and
  embedded (`tests/test_render_cards.py`).

## Limitations

- The generator only supports five players, five rooms and five hours.
