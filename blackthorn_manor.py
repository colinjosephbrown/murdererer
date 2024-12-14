general = {
    "intro": "You have been invited to Blackthorn Manor, the sprawling and isolated estate of Duke Percival Blackthorn, for an exclusive weekend retreat. The mansion, perched atop misty hills, looms with gothic grandeur, its sprawling halls illuminated faintly by candlelight.",
    "phase1": "The Arrival",
    "arrival": "As your carriage crests the hill on a chilly autumn evening, you see the vast silhouette of Blackthorn Manor. Inside, the Duke greets you warmly, a stately man in his late fifties with an air of reserved authority. Other guests arrive, and you are introduced to %s, %s, %s, and %s.",
    "phase2": "The Evening",
    "dinner": "At precisely 8 o'clock, the party gathers in the grand dining hall. The dinner is exquisite: venison, roast fowl, and delicacies abound. The conversation is civil, though an undertone of tension hangs in the air. By 10 o'clock, the evening's formalities begin to wind down.",
    "discovery": "In the dead of night, at the stroke of midnight, a bloodcurdling scream echoes through the halls. Moments later, the butler bursts into the drawing room—'The Duke! The Duke has been murdered!'",
    "npc_alibi": "The household staff is interrogated. They all insist they were together in the servant quarters at the time of the murder, preparing for morning duties. If there is a killer, it must be one of the guests. The air grows cold with suspicion as you eye one another.",
    "mission": "The realization dawns—there's no leaving until the murderer is found. Trust no one, reveal nothing, and uncover the truth before someone else falls victim."
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
        "description": "You are %s, a rising journalist for the London Gazette, known for your exposés on the upper classes.",
        "motive": "The Duke discovered you were writing a story on the Blackthorn family’s sordid secrets and had threatened to ruin you before it could be published."
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
    "group": "You join %s and %s in the study at %d o'clock to discuss politics over brandy.",
    "pre_murder": "A grand mahogany desk dominates the room, littered with unopened letters and a heavy silver paperweight shaped like a lion.",
    "murder": "The Duke sits at his desk, absorbed in a letter. You creep up behind him, grab the heavy silver paperweight, and deliver a single decisive blow to the back of his head. You wipe it clean and quietly exit.",
    "post_murder": "The study is silent. A faint dark stain mars the Persian rug near the desk.",
    "clue": "You notice %s has a smear of ink on their cuff, as though they'd been rifling through documents hastily."
},
{
    "name": "conservatory",
    "alone": "You slip away to the conservatory at %d o'clock to enjoy the scent of roses in solitude.",
    "group": "At %d o'clock, you and %s take a stroll through the conservatory's lush greenery.",
    "pre_murder": "A tall iron spade leans against the wall, incongruously placed near delicate orchids.",
    "murder": "Spotting the Duke inspecting his prized orchids, you grab the iron spade and strike him down in a fit of rage. You hastily drag his body behind a row of flowering shrubs and wipe the spade.",
    "post_murder": "A patch of freshly disturbed soil lies conspicuously near the orchids. The spade leans askew against the wall.",
    "clue": "A faint smear of dirt mars the hem of %s's cloak."
},
{
    "name": "drawing room",
    "alone": "You steal a moment alone at %d o'clock to admire the family portraits lining the walls.",
    "group": "At %d o'clock, you join %s and %s in the drawing room to share a glass of sherry.",
    "pre_murder": "The centerpiece is a marble bust of Duke Blackthorn himself, pridefully displayed on a pedestal.",
    "murder": "You lure the Duke to the far end of the room. As he turns his back, you seize the marble bust and swing it hard against his temple. You leave his body behind the velvet curtains.",
    "post_murder": "The curtains hang oddly, as though concealing something. The marble bust has a faint crack along its edge.",
    "clue": "You catch %s nervously glancing at the marble bust, their hands trembling slightly."
},
{
    "name": "library",
    "alone": "At %d o'clock, you browse the Duke's collection of rare books in the vast library.",
    "group": "At %d o'clock, you join %s and %s to marvel at the library's treasures.",
    "pre_murder": "A ladder stands against a tall bookshelf. A large globe sits in the center of the room.",
    "murder": "You wait until the Duke's back is turned, then push the heavy globe onto him from a height. It strikes with crushing force. You shove the globe back into place, leaving no trace.",
    "post_murder": "The globe now seems slightly askew. A faint indentation marks the rug beneath it.",
    "clue": "You notice %s has scuff marks on their boots, as though they'd been climbing."
},
{
    "name": "tower room",
    "alone": "You ascend the spiraling staircase to the tower room at %d o'clock to take in the moonlit view.",
    "group": "At %d o'clock, you and %s climb to the tower room, braving the chill air.",
    "pre_murder": "The room is empty save for a massive brass telescope pointed skyward.",
    "murder": "You find the Duke at the telescope, lost in thought. Without warning, you shove him hard. He crashes through the window and falls to his death on the stones below.",
    "post_murder": "The telescope is tilted oddly, and the broken window is now covered hastily with a curtain.",
    "clue": "A shard of glass clings to the hem of %s's coat."
}
]
