Current plan:

Separate pack building functions from drafting function.
Draft function will call a pack generator function, which will return a list of cards.

Pack generators will be complex - allowing multiple types of cards, and distributions depending on the generator
Support multiple types of generators: cube, draft packs, etc
Allow users to create their own generators (will require code) - but creating custom cardpool should be do-able in ui

Maybe use FastAPI for serving data, and Vue for the frontend?

## Data Model for Drafting Side

### Draft
- id: int
- name: str
- generator: str
- players: List[Player]
- rounds: int

### User
- id: int
- name: str
- email: str
- password: str
- drafts: List[Draft]
- decks: List[Deck]
- packs: List[Pack]

### Deck
- id: int
- cards: List[Card]

### Card
- id: int
- name: str
- nrdb_id: int

### Pack
- id: int
- cards: List[Card]


Relationships:
Draft many-to-many User
Draft one-to-many Pack
Pack one-to-many Card
User one-to-many Deck
Deck many-to-many Card -> should this instead a str of card ids? If it is requires more work to get the cards, but it is simpler to implement.

Functions needed:
- Create Draft
    - Create draft object
    - Choose generator
    - Choose number of rounds
    - Share draft with other users
- Join Draft
    - Register user (NRDB OAuth?)
    - Add player to draft
- Start Draft
    - Deal packs to players
    - Create initial packs
    - Set player order
- Drafting
    - Present player with draft options
    - Update draft state
    - Pass packs to next player
    - When all packs are empty, start next round
- End Draft
    - Create decks from cards
    - Save decks to user
    - Save draft to user
    - Export to NRDB?