general = {
    "intro": "You have been invited to the royal Bavarian mountain residence for an exclusive dinner party by Count Ludwig IV of Bavaria, great nephew of the famous king. The residence is as spectacular as it is high in the Alps.",
    "phase1": "The Arrival",
    "arrival": "Upon arrival by carriage on the clear October evening, you enter and are greeted by the Count and his servants. The Count is a short man, slight in build and charismatic. He appears to be in his late twenties. Other guests are also arriving and you are introduced to %s, %s, %s and %s.",
    "phase2": "The Evening",
    "dinner": "At 7 o'clock everyone reconvenes in the dining hall, looking fit for royal audience. The dinner is served in many delicate courses. Conversation is lively and interesting. By quarter to 8, the meal is concluding and there is discussion of how to retire.",
    "discovery": "At 1 in the morning, as guests are starting to make their way towards bed, there is a loud commotion. One of the servants has discovered there's been a murder!",
    "npc_alibi": "The servants are all summoned and questioned. Each servant corroborates the same story; until a nightly round when the body of Count Ludwig IV was found, all of the servants had been down stairs in the servant common room together. No one was unaccounted for for more than a few minutes. If there is a murderer here, it is not one of them. You look around the room at the other guests, now all suspects.",
    "mission": "Reality starts to set in - with a murderer on the loose, no one is safe. It is too far to get help from the authorities tonight. You need to discover who is the culprit before the night is up. Tell the truth, tell lies but try not to reveal your own secrets!"
}

characters = [
    {
        "name": "Matilde Acosta",
        "description": "You are Baroness %s, of Lisbon. You have been made honorary diplomatic envoy to Portugal and frequently tour mainland Europe, keeping ties with heads of state, royals and other ranks of high society.",
        "motive": "Due to the wide interbreeding of the European royals through the ages, you happen be to Count Ludwig's niece. Owing to certain unmarried relatives and some tragic deaths in the family, you also happen to presently be the Count's eldest surviving heir to his considerable wealth - that is, unless he marries and has children of his own."
    },
    {
        "name": "Reginald Coleman",
        "description": "You are %s, Scottish industrialist and railroad tycoon. You like to rub shoulders with the elite, whatever their title, as wealthy investors can never number too many.",
        "motive": "Count Ludwig, however, happens to be one wealthy elite you wish would disappear as his flat refusal to allow new rail lines to cross his vast land holdings in southern Germany have cost you millions."
    },
    {
        "name": "Eva Palvin",
        "description": "You are not famous Hungarian actress %s, but instead you are her younger step sister, Lili, who happens to share an uncanny resemblance. Looking for vacation away from the public eye, your sister said you could go in her stead and helped you dress the part.",
        "motive": "Eight years prior, your love and fiance Jozsef was fighting for Austria-Hungary in the first world war. A German artillary squadron was giving cover as the Jozsef's company advanced. Identifying low probability of victory, the Germans under command of Count Ludwig IV decided to retreat, leaving the Austro-Hungarians undefended. They were all killed that day and you have always blamed the Count for the death of your love."
    },
    {
        "name": "Hinrich von Wagner",
        "description": "You are %s a german general and career military man. You served with the Count in the war.",
        "motive": "While the Count persists he is your friend, he holds great sway in the upper echelons of the millitary and rumor on good authority has come your way that he will reccomend your rival, Klaus von Bismark for the post of high commander over you. As Klaus has never respected your leadership and his posting could be ruinous for your career."
    },
    {
        "name": "Dr. Sofia Devrise",
        "description": "You are %s, a pre-imminent French physicist working in quantum theory.",
        "motive": "The Count was once a patron of the scientific programme that funded your research but has recently pulled out, in support of a group at the University of Erlang-Nurnberg where your rival, Dr. Godel Schmitt is posted. If this funding goes through, they will have the upper hand in the race to understand quantum mechanics and your career could be ruined."
    }
]

rooms = [
    {
        "name": "billiards room",
        "alone": "You enter the billiards room at %d o'clock alone to practice your pool shots and breaks.",
        "group": "You go to the billiards room at %d o'clock for a sporting 3-way tournament with %s and %s.",
        "pre_murder": "After a couple rounds of billiards, you decide to switch-up the game and move to darts. There are three colour matched darts for each player ready at the board.",
        "murder": "Entering the room, you find your mark, the Count and invite him to a friendly game of darts. He throws first and as he goes to collect, you dip one of your three green darts into a small vial of poison. As he retuns and faces the board once again, you stab the count in the neck with the poison dart. The effect is immediate and he begins to go limp. You catch his fall and drag him akwardly to the window. In moments the poison has acted and he is dead. You open one the large windows looking down onto thick hedges and throw his corpse over. As you exit, you realize you are still holding the dart, but there is no time to return.",
        "post_murder": "After a couple rounds of billiards, you decide to switch-up the game and move to darts. There are three colour matched darts for each player save green for which one dart appears to be missing.",
        "pre_minor_crime": "On one wall sits a painting that immediately catches your eye. It depicts a beautiful garden with idyllic fruiting trees, flowers and fauna. The colour and brush work is clearly the work of a master, though you aren't sure which one.",
        "minor_crime": "Looking at the far wall you immediately mark your prize. A masterpiece by Frans Ulm, your favourite impressionist. From a photograph, you have contracted a forgery created and now you set to work replacing the real with the forgery. It takes time and effort, and it pains you to roll up the real work, but once done, you are releaved and extatic. You quickly exit to hide your prize in your room.",
        "post_minor_crime": "On one wall sits a painting that immediately catches your eye for its dullness. It depicts a garden with idyllic fruiting trees, flowers and fauna however, he colour is drab and brush strokes amateurish.",
        "body_found": "The mangled body of the Count has been found beside the house, under the window of the billiards room, which have been left open. At first, it is thought that the cause of death is the fall, but after closer examination, a small piercing wound is found on the side of the Count's neck. The wound seems too small for him to have bled out, suggesting poison.",
        "witness_pre_murder": "Passing near the billiards room, you witness %s exiting with what appears to be a rolled painting. You don't appear to have been seen. Looking in, there is no one inside and the windows are all shut.",
        "witness_post_murder": "Passing near the billiards room, you witness %s exiting with what appears to be a rolled painting. You don't appear to have been seen. Looking in, there is no one inside, but a large window has been left open.",
        "clue": "You notice %s is nervously fingering an object that, after a few moments, you realize is a pool cue chalk holder."
    },
    {
        "name": "smoking lounge",
        "alone": "At %d o'clock, you take leave from the party and make your way to the smoking lounge.",
        "group": "At %d o'clock, make way to the smoking lounge to partake in the smoking of cigars with %s and %s.",
        "pre_murder": "The lounge is equipped with beautiful leather chairs by a large fire place, a wine rack and a humidor so large you could almost fit inside.",
        "murder": "The Count sits by the fire with a glass of wine in hand. On the wall you see a rapier and with no one else in the room, decide to finish what you came to do. The blade is sharp and narrow. Quietly and decisively you run the sword through the back of the arm chair and through his heart, killing him swiftly. The small blade leads to little blood but the wine takes some cleaning up. A large humidor makes a conveient place to hide the body, with a little elbow grease.",
        "post_murder": "The lounge is equipped with beautiful leather chairs by a large fire place, a wine rack and a humidor so large you could almost fit inside. You notice however that one of the leather chairs has a small puncture hole that extends through its back and there are some wine stains on the rug. Perhaps the Count should reprimand his head servant for not taking more notice of the needed mantenance.",
        "pre_minor_crime": "A glass panel door secures the wine on the rack but even through this, you note some auspicious labels and vintages.",
        "minor_crime": "As a wine connoisseur, word has reached your ear of several bottles of especially sought-after vintages in the Count's collection. You puruse the rack and begin taking bottles of the most extreme rarity. In order not to raise immediate suspicion, you replace each bottle with lesser wines, complete with fake labels that you have smuggled in your carpet bag. With the bottles secured, you exit to hide them in your room until your departure.",
        "post_minor_crime": "A glass panel door secures the wine on the rack but has been left open. Taking a look at the bottles you note some auspicious labels and vintages.",
        "body_found": "The contorted body of the Count has been found crammed undignified into a large humidor in the smoking lounge. He has a small puncture wound in his back, which appears to continue through to his heart.",
        "witness_pre_murder": "Leaving, you witness %s exiting the smoking lounge with a carpet bag. It clinks slightly as they pass and a cork peaks out of the opening. After they leave, you peak inside the room and see nothing of note save a beautiful, flawless leather arm chair by the fire, inviting you to sit.",
        "witness_post_murder": "Leaving, you witness %s exiting the smoking lounge with a carpet bag. It clinks slightly as they pass and a cork peaks out of the opening. After they leave, you peak inside the room and see nothing of note save a leather arm chair by the fire with a hole punched through its backing.",
        "clue": "You notice that %s smells strongly of cigar smoke."
    },
    {
        "name": "library",
        "alone": "You venture to the library at %d o'clock alone to peruse some of its impressive collection. Its tall east windows must provide an impressive morning view.",
        "group": "You head to the library at %d o'clock with %s and %s to gawk at its impressive collection. Its tall east windows must provide an impressive morning view.",
        "pre_murder": "On the opposite wall, pushed all the way to the north-west corner of the room is a rolling ladder to reach books on high shelves.",
        "murder": "You enter the library and notice the Count perusing the shelves, apparently lost in thought. You quietly move a rolling ladder on the opposite wall from the north corner of the room to the south and then climb its rungs. You've come prepared. With the count still facing away, you throw a noose across one of the high rafters and lower it just behind your mark. With rope in hand, you make your way back down and approach him from behind. With an agile flick, you throw the loop over the Count's neck, and pull the line with all your strength. With great effort, you hoist the Count's moddest corpse high and out of line-of-sight, tying off the end to the top rung of the ladder.",
        "post_murder": "On the opposite wall, near the entrance at the south-west corner of the room is a rolling ladder to reach books on high shelves.",
        "pre_minor_crime": "You also spot a glass case exhibiting a rare first edition copy of Mary Shelley's 'Frankenstein'.",
        "minor_crime": "You have come to steal a rare first edition of Frankenstein that you have heard rumor is among the collection. You scroll up and down the walls of books but its nowhere to be found. Finally, across the room you see a glass case with the first edition sitting alone on display. Clearly this is a prized possession, but not one the owner expects a guest to steal as the case is unlocked. You open the case, marvel at your prize and replace the original with a reprint. You exit quickly, not to linger around the scene.",
        "post_minor_crime": "You also spot a glass case that is presently empty.",
        "body_found": "The body of the Count has been discovered hanging in the library, high and out of sight of those not looking up. The noose has been hung over the rafter beams and secured to the top rung of a rolling ladder. As there is no obvious way to get over the rafter, it does not appear to be suicide",
        "witness_pre_murder": "On your way down the hall, you notice %s, climbing a ladder just inside the library. A few moments later they decend, turn and open a glass case.",
        "witness_post_murder": "On your way down the hall, you notice %s, climbing a ladder in the far corner of the library from its entrance. A few moments later they decend, turn and open a glass case.",
        "clue": "You notice %s has a leather bound book in hand of the style of many in the library."
    },
    {
        "name": "conservatory",
        "alone": "At %d o'clock you avoid the party by entering the conservatory, an elaborate greenhouse filled with exotic fruiting and flowering plants, all oddly out of place in the high alps.",
        "group": "At %d o'clock %s and %s join you in a tour of the conservatory, an elaborate greenhouse filled with exotic fruiting and flowering plants, all oddly out of place in the high alps.",
        "pre_murder": "Juxtaposed against the immaculate arrangements of the horticulture is a rather plain shed, closed and presumably full of gardening tools.",
        "murder": "You have followed the Count here and survey the room to ensure there is no one else. The Count is appraising his favourite orchid as you silently open the tool shed and grab a large shovel. To ensure no alarm is raise, you charge quietly from behind and strike the side of his head with full force. There is the dull ring of the metal shovel as he drops to the floor. Blood slowly pools. You repurpose your weapon to dig a shallow grave and roll your victim in. In haste, you wipe up the evidence, bury the body and bloody rags and throw the shovel back in tool shed.",
        "post_murder": "A tool shed near the entrance has been left open with trowels and buckets arranged with the care of a professional, save one shovel seemingly thrown in.",
        "pre_minor_crime": "The orchid garden is especially splendid, arranged with inspiration from a rainbow and exhibiting a single rare flower of every colour.",
        "minor_crime": "Progressing to the orchid garden, you spot the exquisite rare blue orchid that you have sought for years. With no one else in the room, you dig your hands in the soil and pull the delicate flower up, roots and all. You place it in a small purse and turn to hide it in your quarters.",
        "post_minor_crime": "The beatiful orchid garden contains one specimen of every colour, arranged in a rainbow with the exception of a freshly dug hole where a blue orchid should grow.",
        "body_found": "The corpse of the Count has be discovered shallowly buried in a large planter in the conservatory. He seems to have suffered trauma to the side of the head. The discovery was made as the gardener was doing a last watering of the plants before bed. He also mentions that someone had been using his tools, a crime it seems he is almost as upset about.",
        "witness_pre_murder": "Walking by the conservatory, you spy %s digging a blue orchid from the ground. The tool shed appears shut, so they must be using their hands - and thus likely do not have permission.",
        "witness_post_murder": "Walking by the conservatory, you notice the tool shed open and spy %s digging a blue orchid from the ground.",
        "clue": "A tiny flower petal has clung to %s's shoulder, seemingly without their notice. Given the season, it could only be from a flowering tree grown indoors."
    },
    {
        "name": "observatory",
        "alone": "At %d o'clock, you head along a muddy path and up to the observatory on the hill to view the full October moon in peace and quiet.",
        "group": "At %d o'clock, you, %s and %s head along a muddy path and up to the observatory on the hill to view the full October moon in splendid detail.",
        "pre_murder": "Inside, you see that the telescope nearly fills the room, resting on a large rotating mount, providing low head clearance as it swivels.",
        "murder": "After entering you recognize the Count on the other side of the room, admiring the structure of the dome. He doesn't notice you enter. Quietly you grab the handle of the telescope mount and swing it forcefully around in his direction. The metal frame slams into the back of his skull and he drops instantly. You drag his body out to a small alcove behind the observatory, wipe up the trail of blood and your finger prints on the telescope.",
        "post_murder": "Inside, you see that the telescope nearly fills the room, resting on a large rotating mount, providing low head clearance as it swivels. Strangely, the telescope has been left pointing low to the north, one of the few directions from which the sky can't be seen from this vantage point.",
        "pre_minor_crime": "It is clear that the observatory is actively used by astronomers as the small desk in the room is covered in scientific log books and written notes.",
        "minor_crime": "The resident scientist, Dr. Farnstomm is not here tonight, but instead back at the University. With jealous fore-knowledge of the discovery of a new planet that he is ready to break to the world, you steal all the scientific log books and written notes off his desk.",
        "post_minor_crime": "While you've been told that the observatory is actively used by astronomers, the one desk in the room is clear of any scientific log books or written notes.",
        "body_found": "The body of the Count has been found in a small alcove behind the observatory. The cause of death appears to be blunt force trauma to the back of the head. No weapon has been found at the scene.",
        "witness_pre_murder": "On your way out you eye %s coming down the path from the observatory, carrying a large stack of notebooks and papers. They appear to be in a hurry and uninterested in coversation. The observatory seems to be pointed towards the full moon.",
        "witness_post_murder": "On your way out you eye %s coming down the path from the observatory, carrying a large stack of notebooks and papers. They appear to be in a hurry and uninterested in coversation. The observatory seems to be pointed north away from the moon.",
        "clue": "You notice a small amount of gray mud on the shoes of %s, likely recent given that everyone arrived for dinner looking their best."

    }
]
