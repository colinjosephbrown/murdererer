general = {
    "intro": "You have been invited to Blackthorn Manor, the sprawling and isolated estate of Duke Percival Blackthorn, for an exclusive weekend retreat. The mansion, perched atop misty hills, looms with gothic grandeur, its sprawling halls illuminated faintly by candlelight.",
    "phase1": "The Arrival",
    "arrival": "As your carriage crests the hill on a chilly autumn evening, you see the vast silhouette of Blackthorn Manor. Inside, the Duke greets you warmly, a stately man in his late fifties with an air of reserved authority. Other guests arrive, and you are introduced to %s, %s, %s, and %s.",
    "phase2": "The Evening",
    "dinner": "At precisely 6 o'clock, the party gathers in the grand dining hall. The dinner is exquisite: venison, roast fowl, and delicacies abound. The conversation is civil, though an undertone of tension hangs in the air. By a quarter to 7, the evening's formalities wind down and the guests drift off to amuse themselves about the manor.",
    "discovery": "In the dead of night, at the stroke of midnight, a bloodcurdling scream echoes through the halls. Moments later, the butler bursts into the great hall - 'The Duke! The Duke has been murdered!'",
    "npc_alibi": "The household staff is interrogated. They all insist they were together in the servant quarters all evening, preparing for morning duties. If there is a killer, it must be one of the guests. The air grows cold with suspicion as you eye one another.",
    "mission": "The realization dawns - there's no leaving until the murderer is found. Trust no one, reveal nothing, and uncover the truth before someone else falls victim."
}

characters = [
    {
        "name": "Lady Beatrice Ashcroft",
        "description": "You are Lady %s, a renowned socialite and widow from London. You are famed for your opulent balls and impeccable taste.",
        "motive": "The Duke had acquired several prized art pieces from an auction you dearly coveted. Worse, he planned to reveal scandalous letters regarding your late husband's debts, threatening your standing in society."
    },
    {
        "name": "Sir Edmund Caldwell",
        "description": "You are Sir %s, a seasoned explorer and member of the Royal Geographic Society. You have returned to England after years abroad.",
        "motive": "The Duke once funded your expeditions but has refused your latest request, calling you 'a reckless dreamer.' Without his patronage, your explorations may be at an end."
    },
    {
        "name": "Dr. Horace Blythe",
        "description": "You are %s, a brilliant but controversial physician specializing in experimental treatments for the rich and desperate.",
        "motive": "The Duke publicly denounced your latest treatment as 'charlatanry,' costing you wealthy clients and your reputation."
    },
    {
        "name": "Miss Clara Pendleton",
        "description": "You are %s, a rising journalist for the London Gazette, known for your exposes on the upper classes.",
        "motive": "The Duke discovered you were writing a story on the Blackthorn family's sordid secrets and had threatened to ruin you before it could be published."
    },
    {
        "name": "Colonel Ambrose Hawthorne",
        "description": "You are %s, a retired military officer and former confidant of the Duke, known for your stern demeanor.",
        "motive": "The Duke accused you of stealing from the regimental funds during your time in the army and planned to present evidence, risking your legacy and honor."
    }
]

rooms = [{
    "name": "study",
    "alone": "At %d o'clock, you retreat to the Duke's study to admire the vast shelves of legal tomes and curios.",
    "group": "At %d o'clock, you join %s and %s in the study to discuss politics over brandy.",
    "pre_murder": "A grand mahogany desk dominates the room, littered with unopened letters and a heavy silver paperweight shaped like a lion.",
    "murder": "The Duke sits at his desk, absorbed in a letter. You creep up behind him, grab the heavy silver paperweight, and deliver a single decisive blow to the back of his head. You heave his body into the deep window seat beneath the curtains and lower its lid, then wipe the paperweight clean, return it to the desk and quietly exit.",
    "post_murder": "The study is silent. A faint dark stain mars the Persian rug near the desk.",
    "pre_minor_crime": "Behind the desk, a glass-fronted cabinet displays the Blackthorn signet ring on a velvet cushion, its great ruby glowing in the candlelight.",
    "minor_crime": "You have come for the Blackthorn signet ring, the seal with which the Duke signs his most private correspondence. With it, any letter could be made to bear his authority. You ease open the glass-fronted cabinet behind the desk, pocket the ring and leave a paste copy in its place on the velvet cushion before slipping out.",
    "post_minor_crime": "Behind the desk, a glass-fronted cabinet stands slightly ajar. On a velvet cushion inside sits the Blackthorn signet ring, though its ruby looks oddly dull and the gold suspiciously like brass.",
    "body_found": "The Duke's body has been found folded into the window seat of his study, the back of his skull caved in by a single heavy blow. A dark stain on the Persian rug marks where he must have fallen.",
    "witness_pre_murder": "Passing the study, you glimpse %s through the half-open door, slipping something small from the glass cabinet behind the desk into their pocket. Beyond them, the study is in perfect order, the Persian rug spotless.",
    "witness_post_murder": "Passing the study, you glimpse %s through the half-open door, slipping something small from the glass cabinet behind the desk into their pocket. Beyond them, you notice a dark stain on the Persian rug near the desk.",
    "clue": "You notice %s has a smear of ink on their cuff, as though they'd been rifling through documents hastily."
},
{
    "name": "conservatory",
    "alone": "You slip away to the conservatory at %d o'clock to enjoy the scent of roses in solitude.",
    "group": "At %d o'clock, you, %s and %s take a stroll through the conservatory's lush greenery.",
    "pre_murder": "A tall iron spade leans against the wall, incongruously placed near delicate orchids.",
    "murder": "Spotting the Duke inspecting his prized orchids, you grab the iron spade and strike him down in a fit of rage. You hastily drag his body behind a row of flowering shrubs, scatter soil over the drag marks and wipe the spade.",
    "post_murder": "A patch of freshly disturbed soil lies conspicuously near the orchids. The spade leans askew against the wall.",
    "pre_minor_crime": "At the heart of the glasshouse, beneath a bell jar, blooms the famed Blackthorn Rose, a black rose bred by the Duke's grandfather and grown nowhere else in England.",
    "minor_crime": "Collectors in Amsterdam would pay a small fortune for a cutting of the Blackthorn Rose. With no one else about, you lift the bell jar, take several careful cuttings with a pocket knife, wrap them in a damp handkerchief and tuck them into your sleeve before leaving.",
    "post_minor_crime": "At the heart of the glasshouse, beneath a bell jar that has been set down crookedly, stands the famed black Blackthorn Rose, its stems freshly and crudely cut.",
    "body_found": "The Duke's body has been found behind a row of flowering shrubs in the conservatory, the side of his head struck by a heavy iron blow. Soil has been scattered to hide the marks where he was dragged.",
    "witness_pre_murder": "Through the misted glass of the conservatory, you see %s lift a bell jar and snip at the black rose beneath it before hurrying out. Nearby, the iron spade leans against the wall and the soil by the orchids lies undisturbed.",
    "witness_post_murder": "Through the misted glass of the conservatory, you see %s lift a bell jar and snip at the black rose beneath it before hurrying out. Nearby, you notice a patch of freshly turned soil by the orchids and the spade leaning askew.",
    "clue": "A faint smear of dirt mars the hem of %s's cloak."
},
{
    "name": "drawing room",
    "alone": "You steal a moment alone at %d o'clock to admire the family portraits lining the walls.",
    "group": "At %d o'clock, you join %s and %s in the drawing room to share a glass of sherry.",
    "pre_murder": "The centerpiece is a marble bust of Duke Blackthorn himself, pridefully displayed on a pedestal.",
    "murder": "You lure the Duke to the far end of the room. As he turns his back, you seize the marble bust and swing it hard against his temple. You leave his body behind the velvet curtains.",
    "post_murder": "The curtains hang oddly, as though concealing something. The marble bust has a faint crack along its edge.",
    "pre_minor_crime": "On the mantelpiece sits a jeweled gold snuffbox, said to have been a gift to the Duke's grandfather from the Prince Regent himself.",
    "minor_crime": "Debts have a way of making a person bold. You lift the Prince Regent's jeweled snuffbox from the mantelpiece, feel its satisfying weight in your palm, and slip it into your pocket. You nudge the ornaments along the mantel to hide the gap before leaving.",
    "post_minor_crime": "On the mantelpiece, the ornaments have been shuffled about, leaving a small clean rectangle in the dust where something once sat.",
    "body_found": "The Duke's body has been found behind the velvet curtains of the drawing room, a vicious wound at his temple. Flecks of marble cling to his hair.",
    "witness_pre_murder": "Passing the drawing room, you see %s at the mantelpiece slip a glittering snuffbox into their pocket. Behind them, the marble bust of the Duke stands proudly on its pedestal and the velvet curtains hang straight.",
    "witness_post_murder": "Passing the drawing room, you see %s at the mantelpiece slip a glittering snuffbox into their pocket. Behind them, the velvet curtains at the far end hang oddly and the marble bust has a crack along its edge.",
    "clue": "You catch %s nervously glancing at the marble bust, their hands trembling slightly."
},
{
    "name": "library",
    "alone": "At %d o'clock, you browse the Duke's collection of rare books in the vast library.",
    "group": "At %d o'clock, you join %s and %s to marvel at the library's treasures.",
    "pre_murder": "A ladder stands against a tall bookshelf. A large globe sits in the center of the room.",
    "murder": "You wait until the Duke stands beneath the ladder, then push the heavy globe onto him from a height. It strikes with crushing force. You drag his body into the shadowed reading nook behind the last bookshelf, then shove the globe back into place, leaving no trace.",
    "post_murder": "The globe now seems slightly askew. A faint indentation marks the rug beneath it.",
    "pre_minor_crime": "In a locked display case lies a medieval illuminated bestiary, its gilded pages open to a painting of a griffin.",
    "minor_crime": "A collector in Paris has promised you a fortune for the Duke's illuminated bestiary. You pick the lock of its display case with a hatpin, wrap the slim volume inside your coat and leave a similarly bound book of sermons open in its place, then leave in haste.",
    "post_minor_crime": "In a display case lies what is labelled as a medieval illuminated bestiary, though the volume open inside is plainly a dreary book of sermons.",
    "body_found": "The Duke's body has been found hidden in the reading nook behind the last bookshelf of the library, his chest and skull crushed as if by some tremendous weight.",
    "witness_pre_murder": "Passing the library, you see %s bent over a display case, tucking a slim volume under their coat. The great globe stands squarely in the center of the room.",
    "witness_post_murder": "Passing the library, you see %s bent over a display case, tucking a slim volume under their coat. The great globe sits slightly askew in the center of the room.",
    "clue": "You notice %s has scuff marks on their boots, as though they'd been climbing."
},
{
    "name": "tower room",
    "alone": "You ascend the spiraling staircase to the tower room at %d o'clock to take in the moonlit view.",
    "group": "At %d o'clock, you, %s and %s climb to the tower room, braving the chill air.",
    "pre_murder": "The room is empty save for a massive brass telescope pointed skyward.",
    "murder": "You find the Duke at the telescope, lost in thought. Without warning, you shove him hard. He crashes through the window and falls to his death on the stones below. You draw a curtain across the broken pane and hurry back down the stairs.",
    "post_murder": "The telescope is tilted oddly, and the broken window is now covered hastily with a curtain.",
    "pre_minor_crime": "Beside the telescope, a velvet-lined case holds a gold marine chronometer that once belonged to the Duke's admiral grandfather.",
    "minor_crime": "The admiral's gold chronometer would settle your debts several times over. You lift it from its velvet-lined case beside the telescope, close the lid on the empty case and hurry down the spiraling stairs.",
    "post_minor_crime": "Beside the telescope sits a velvet-lined case. Lifting the lid, you find only the hollow where some instrument once rested.",
    "body_found": "The Duke's broken body has been found on the flagstones of a disused terrace at the foot of the tower, beneath a shattered window.",
    "witness_pre_murder": "At the foot of the tower stairs, you see %s hurrying down, a gold chain trailing from their pocket. The air on the staircase is still.",
    "witness_post_murder": "At the foot of the tower stairs, you see %s hurrying down, a gold chain trailing from their pocket. An icy draught sweeps down the staircase, as though a window above has been opened or broken.",
    "clue": "You notice %s's hair is windswept and their hands icy cold, as though they had recently been somewhere high and draughty."
}
]
