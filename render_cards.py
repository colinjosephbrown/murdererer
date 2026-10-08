"""Render each player's character sheet as a printable deck of cards.

Takes the game.json written by murdererer.py and writes one HTML file per
player. Open a file in a browser and print it double-sided (flip on the long
edge) to get the shared card back on the reverse of every card, then cut along
the dashed lines.

    python render_cards.py game.json --images bavarian_hunting_lodge
"""
import argparse
import base64
import io
import json
import os
import re

CARD_WIDTH_MM = 92
CARD_HEIGHT_MM = 127
COLUMNS = 2
ROWS = 2
CARDS_PER_PAGE = COLUMNS * ROWS

IMAGE_TYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
               ".webp": "image/webp", ".gif": "image/gif"}

RULES = [
    "Read your cards in order: who you are, your arrival, the evening hour by hour, then the discovery.",
    "Keep your cards to yourself. Share what you choose, by telling others or by showing them a card.",
    "Evidence cards record what you noticed about other guests. Showing one is the strongest proof you can offer.",
    "Cards marked <em>Secret</em> are yours to protect. Every guest has something to hide, but only one is a murderer.",
    "Tell the truth or tell lies. Before the night is over, agree on who the murderer is.",
]


def escape(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def clock_label(clock):
    return "%d o'clock" % clock


def _name_words(text):
    """Lower-case words with punctuation, spaces and underscores ignored: 'Dr. Sofia_Devrise' -> ' dr sofia devrise '."""
    return " %s " % " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def find_portrait(portraits_dir, name):
    """Find an image whose file name contains the character's name, ignoring case and punctuation."""
    if not portraits_dir or not os.path.isdir(portraits_dir):
        return None
    wanted = _name_words(name)
    for file_name in sorted(os.listdir(portraits_dir)):
        stem, ext = os.path.splitext(file_name)
        if ext.lower() in IMAGE_TYPES and wanted in _name_words(stem):
            return os.path.join(portraits_dir, file_name)
    return None


def image_data_uri(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return "data:%s;base64,%s" % (IMAGE_TYPES[os.path.splitext(path)[1].lower()], data)


def card(kicker, title, body_html, subtitle=None, extra_class="", banner=None, top_html="", background_html=""):
    """One card front. body_html, top_html and background_html must already be escaped."""
    parts = ['<div class="card %s"><div class="frame">' % extra_class,
             background_html,
             '<div class="kicker">%s</div>' % escape(kicker),
             '<div class="title">%s</div>' % escape(title)]
    if subtitle:
        parts.append('<div class="subtitle">%s</div>' % escape(subtitle))
    parts.append('<div class="divider"></div>')
    parts.append(top_html)
    parts.append('<div class="body">%s</div>' % body_html)
    if banner:
        parts.append('<div class="banner">%s</div>' % escape(banner))
    parts.append('</div></div>')
    return "".join(parts)


def paragraphs(*texts):
    return "".join("<p>%s</p>" % escape(t) for t in texts if t)


def numeral(clock):
    """A large, faint hour shown behind a card's text (nothing if the hour isn't known)."""
    if clock is None:
        return ""
    return '<div class="numeral%s" aria-hidden="true">%d</div>' % (" two-digit" if clock >= 10 else "", clock)


def player_cards(sheet, portrait_path, scene_images=None):
    """scene_images maps a card ('invitation', 'discovery') to a picture file to head it."""
    cards = []
    scene_images = scene_images or {}
    discovery_clock = sheet.get("discovery_clock")

    cards.append(card("Murdererer", "How to Play",
                      '<ol class="rules">%s</ol>' % "".join("<li>%s</li>" % r for r in RULES),
                      extra_class="rules-card"))

    if portrait_path:
        portrait = '<img class="portrait" src="%s" alt="">' % image_data_uri(portrait_path)
    else:
        portrait = '<div class="portrait placeholder"><span>Portrait to come</span></div>'
    cards.append(card("You are", sheet["name"],
                      paragraphs(sheet["description"]) +
                      '<p class="motive"><span class="label">Your motive.</span> %s</p>' % escape(sheet["motive"]),
                      extra_class="character-card", top_html=portrait, banner="Secret: keep this card hidden"))

    invitation_image = ""
    if scene_images.get("invitation"):
        invitation_image = '<img class="scene-image" src="%s" alt="">' % image_data_uri(scene_images["invitation"])
    cards.append(card(sheet["phase1"], "An Invitation", paragraphs(sheet["intro"], sheet["arrival"]),
                      top_html=invitation_image))
    cards.append(card(sheet["phase2"], "Dinner", paragraphs(sheet["dinner"]),
                      background_html=numeral(sheet.get("dinner_clock"))))

    for hour in sheet["hours"]:
        company = "With %s and %s" % tuple(hour["with"]) if hour["with"] else "Alone"
        secret = hour["secret"] is not None
        cards.append(card("%s, %s" % (sheet["phase2"], clock_label(hour["clock"])),
                          hour["room"].title(),
                          paragraphs(" ".join([hour["scene"], hour["murder_state"], hour["minor_crime_state"]])),
                          subtitle=company, extra_class="hour-card secret-card" if secret else "hour-card",
                          banner="Secret: keep this card hidden" if secret else None,
                          background_html=numeral(hour["clock"])))

        # Anything seen during the hour follows its hour card
        seen = hour["witnessed"]
        if seen:
            cards.append(card("Evidence: a sighting", seen["person"], paragraphs(seen["text"]),
                              subtitle="Near the %s at %s" % (seen["room"], clock_label(hour["clock"])),
                              extra_class="evidence-card", background_html=numeral(hour["clock"])))

    discovery_image = ""
    if scene_images.get("discovery"):
        discovery_image = '<img class="portrait" src="%s" alt="">' % image_data_uri(scene_images["discovery"])
    cards.append(card("Read last", "The Discovery", paragraphs(sheet["discovery"], sheet["body_found"]),
                      top_html=discovery_image, background_html=numeral(discovery_clock)))
    cards.append(card("Read last", "The Investigation", paragraphs(sheet["npc_alibi"], sheet["mission"]),
                      background_html=numeral(discovery_clock)))

    # Clues are noticed after the discovery, so they come last
    for clue in sheet["clues"]:
        cards.append(card("Evidence: a clue", clue["person"], paragraphs(clue["text"]),
                          subtitle="Noticed after the discovery", extra_class="evidence-card",
                          background_html=numeral(discovery_clock)))
    return cards


CARD_BACK = """<div class="card back"><svg viewBox="0 0 84 119" preserveAspectRatio="none" aria-hidden="true">
<defs><pattern id="lattice" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<path d="M0 0H6M0 0V6" stroke="currentColor" stroke-width="0.25" fill="none"/></pattern></defs>
<rect x="1" y="1" width="82" height="117" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="2.6" y="2.6" width="78.8" height="113.8" fill="none" stroke="currentColor" stroke-width="0.3"/>
<rect x="4.4" y="4.4" width="75.2" height="110.2" fill="url(#lattice)"/>
<circle cx="42" cy="59.5" r="17" fill="#fff" stroke="currentColor" stroke-width="0.8"/>
<circle cx="42" cy="59.5" r="14.6" fill="none" stroke="currentColor" stroke-width="0.3"/>
<circle cx="42" cy="54.8" r="3.4" fill="currentColor"/>
<path d="M39.8 57.2 L44.2 57.2 L45.6 66.8 L38.4 66.8 Z" fill="currentColor"/>
</svg><div class="back-name">Murdererer</div></div>"""

STYLE = """
@page { size: auto; margin: 10mm; }
:root { --ink: #2a211b; --muted: #6b5d52; --accent: #7a1f24; --rule: #b9a99a; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; color: var(--ink); }
body { font-family: "EB Garamond", Georgia, "Times New Roman", serif;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.sheet { width: %(sheet_w)smm; height: %(sheet_h)smm; margin: 0 auto; display: grid;
         grid-template-columns: repeat(%(cols)s, %(card_w)smm); grid-template-rows: repeat(%(rows)s, %(card_h)smm);
         break-after: page; page-break-after: always; }
.sheet:last-child { break-after: auto; page-break-after: auto; }
.card { width: %(card_w)smm; height: %(card_h)smm; padding: 4mm; position: relative; overflow: hidden;
        outline: 0.2mm dashed #c8c8c8; outline-offset: -0.1mm; }
.frame { height: 100%%; border: 0.7mm double var(--ink); padding: 3.5mm 4.5mm 3mm; display: flex; flex-direction: column;
         position: relative; overflow: hidden; }
.frame > * { position: relative; z-index: 1; }
/* Large, faint hour behind the text of an hour card, filling the lower part of the card. */
/* bottom offsets put the baseline about 3mm above the frame (the baseline sits ~0.094em above the box). */
.frame > .numeral { position: absolute; z-index: 0; right: 3mm; bottom: -6mm; margin: 0;
                    font-family: "EB Garamond", Georgia, serif; font-variant-numeric: lining-nums;
                    font-size: 96mm; line-height: 1; color: var(--accent); opacity: 0.08;
                    pointer-events: none; user-select: none; }
.frame > .numeral.two-digit { font-size: 78mm; bottom: -4.3mm; right: 2mm; }
.kicker { font-family: "IM Fell English SC", Georgia, serif; font-size: 8pt; letter-spacing: 0.08em;
          color: var(--accent); text-align: center; }
.title { font-family: "IM Fell English SC", Georgia, serif; font-size: 16pt; line-height: 1.1; text-align: center;
         margin-top: 0.8mm; }
.subtitle { font-style: italic; font-size: 9pt; color: var(--muted); text-align: center; margin-top: 0.8mm; }
.divider { height: 2.4mm; margin: 1.6mm 8mm 1.6mm; border-bottom: 0.25mm solid var(--rule); position: relative; }
.divider::after { content: ""; position: absolute; left: 50%%; bottom: -1.05mm; width: 1.8mm; height: 1.8mm;
                  background: #fff; border: 0.25mm solid var(--rule); transform: translateX(-50%%) rotate(45deg); }
.body { flex: 1; min-height: 0; overflow: hidden; font-size: 10pt; line-height: 1.3; text-align: justify;
        hyphens: auto; -webkit-hyphens: auto; }
.body p { margin: 0 0 0.45em; }
.body p:last-child { margin-bottom: 0; }
.label { font-variant: small-caps; color: var(--accent); }
.rules { margin: 0; padding-left: 1.2em; }
.rules li { margin-bottom: 0.45em; }
.banner { margin-top: 2mm; padding-top: 1.4mm; border-top: 0.25mm solid var(--accent); color: var(--accent);
          font-family: "IM Fell English SC", Georgia, serif; font-size: 8pt; letter-spacing: 0.06em; text-align: center; }
.secret-card .frame { border-color: var(--accent); }
.evidence-card .title { font-size: 14pt; }
.portrait { display: block; width: 30mm; height: 36mm; margin: 0 auto 2mm; object-fit: cover; object-position: top;
            border: 0.4mm solid var(--ink); flex: none; }
.scene-image { display: block; width: 100%%; height: 34mm; margin: 0 0 2mm; object-fit: cover; object-position: center;
               border: 0.4mm solid var(--ink); flex: none; }
.portrait.placeholder { display: flex; align-items: center; justify-content: center; border-style: dashed;
                        color: var(--muted); font-style: italic; font-size: 8pt; text-align: center; padding: 2mm; }
.back { padding: 4mm; color: var(--accent); }
.back svg { display: block; width: 100%%; height: 100%%; }
.back-name { position: absolute; left: 0; right: 0; bottom: 14mm; text-align: center; color: var(--accent);
             font-family: "IM Fell English SC", Georgia, serif; font-size: 11pt; letter-spacing: 0.2em; }
@media screen {
  html, body { background: #77706a; }
  .sheet { background: #fff; margin: 8mm auto; box-shadow: 0 1mm 4mm rgba(0, 0, 0, 0.35); }
  .card.overflow .frame { outline: 1mm solid #e0301e; }
}
""" % {"sheet_w": CARD_WIDTH_MM * COLUMNS, "sheet_h": CARD_HEIGHT_MM * ROWS, "cols": COLUMNS, "rows": ROWS,
       "card_w": CARD_WIDTH_MM, "card_h": CARD_HEIGHT_MM}

FIT_SCRIPT = """
// Shrink text on any card whose body overflows; flag it in red on screen if it still doesn't fit.
function fitCards() {
  var minPx = 9.3;  // about 7pt
  document.querySelectorAll('.card .body').forEach(function (body) {
    var size = parseFloat(getComputedStyle(body).fontSize);
    while (body.scrollHeight > body.clientHeight + 1 && size > minPx) {
      size -= 0.25;
      body.style.fontSize = size + 'px';
    }
    if (body.scrollHeight > body.clientHeight + 1) {
      body.closest('.card').classList.add('overflow');
    }
  });
  document.body.setAttribute('data-fitted', 'true');
}
// Fit once the page loads, and again once web fonts arrive (they can change how much fits).
window.addEventListener('load', fitCards);
if (document.fonts) { document.fonts.ready.then(fitCards); }
"""


def render_deck(sheet, portrait_path=None, backs=True, scene_images=None):
    cards = player_cards(sheet, portrait_path, scene_images)
    pages = []
    for start in range(0, len(cards), CARDS_PER_PAGE):
        fronts = cards[start:start + CARDS_PER_PAGE]
        pages.append('<section class="sheet">%s</section>' % "".join(fronts))
        if backs:
            # Printed double-sided and flipped on the long edge, each row comes back mirrored.
            slots = []
            for row in range(ROWS):
                for col in range(COLUMNS):
                    front_index = row * COLUMNS + (COLUMNS - 1 - col)
                    slots.append(CARD_BACK if front_index < len(fronts) else '<div class="card empty"></div>')
            pages.append('<section class="sheet backs">%s</section>' % "".join(slots))

    return u"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(name)s: Cards</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital@0;1&family=IM+Fell+English+SC&display=swap" rel="stylesheet">
<style>%(style)s</style>
</head>
<body>
%(pages)s
<script>%(script)s</script>
</body>
</html>
""" % {"name": escape(sheet["name"]), "style": STYLE, "pages": "\n".join(pages), "script": FIT_SCRIPT}


def find_scene_images(images_dir, images):
    """Resolve the scenario's picture file names against the images folder, skipping any that are missing."""
    found = {}
    if not images_dir:
        return found
    for card_name, file_name in sorted((images or {}).items()):
        path = os.path.join(images_dir, file_name)
        if os.path.isfile(path):
            found[card_name] = path
        else:
            print("Warning: picture '%s' for the %s card is not in %s" % (file_name, card_name, images_dir))
    return found


def render_game(game_json_path, out_dir=None, images_dir=None, backs=True):
    """Write one HTML deck per player and return the paths written."""
    with io.open(game_json_path, encoding="utf-8") as f:
        game = json.load(f)
    out_dir = out_dir or os.path.join(os.path.dirname(os.path.abspath(game_json_path)), "cards")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    scene_images = find_scene_images(images_dir, game.get("images"))
    paths = []
    for sheet in game["players"]:
        html = render_deck(sheet, find_portrait(images_dir, sheet["name"]), backs, scene_images)
        path = os.path.join(out_dir, sheet["name"] + ".html")
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(html)
        paths.append(path)
    return paths


def create_parser():
    parser = argparse.ArgumentParser(
        "render_cards",
        description="Turn a game.json from murdererer.py into printable HTML cards, one file per player.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("game_json", help="game.json written by murdererer.py")
    parser.add_argument("--out_dir", "-o", default=None, help="output folder (default: a 'cards' folder next to game.json)")
    parser.add_argument("--images", "--portraits", "-p", dest="images", default=None,
                        help="folder of pictures: character portraits (matched by the character's name) and any "
                             "pictures the scenario names for its cards")
    parser.add_argument("--no_backs", action="store_true", help="leave out the card-back pages")
    return parser


if __name__ == "__main__":
    args = create_parser().parse_args()
    for written in render_game(args.game_json, args.out_dir, args.images, backs=not args.no_backs):
        print(written)
