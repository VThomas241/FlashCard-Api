# API Specification


## Authorization
- /login - to login a user
- /register - to register new user

## Decks
- /decks/
    - /
        - get - get all decks.
        - post - add a new deck.

    - /\<int:id\>
        - get -  get the deck with it's id, name and tags.
        - update - update deck name.
        - delete - delete deck.

## Cards
- /decks/\<int:id\>/cards
    - /
        - get - retrieve all cards from the deck.
        - post - add a new card to the deck.
    - \<int:id\>/
        - get - get the card.
        - update - update the card.
        - delete - delete the card.
## Reviews
- /decks/\<int:id\>/review
    - /
        - post - update deck statistics with latest review
## Tags