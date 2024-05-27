# API Specification

## Authorization
- ~~/login/ - to login a user~~
- ~~/register/ - to register new user~~

## Decks
- /decks/
    - /
        - ~~get - get all decks.~~  
        - ~~post - add a new deck.~~

    - /\<int:deck_id\>/
        - ~~get -  get the deck with it's id, name and tags.~~
        - ~~update - update deck name.~~
        - ~~delete - delete deck.~~

## Cards
- /decks/\<int:deck_id\>/cards
    - /
        - ~~get - retrieve all cards from the deck.~~
        - ~~post - add a new card to the deck.~~
    - /\<int:card_id\>/
        - ~~get - get the card.~~
        - ~~update - update the card.~~
        - ~~delete - delete the card.~~
## Reviews
- /decks/\<int:deck_id\>/review
    - /
        - post - update deck statistics with latest review
## Tags
- /tags/
    - /
        - ~~get - get all tags created by user~~
        - ~~post - create a new tag~~
    - /\<int:tag_id\>/
        - ~~get - get all decks with the tag~~
        - ~~update - update tag name~~
        - ~~delete - delete tag~~
    - /decks/\<int:deck_id\>/
        - ~~get - get all tags associated with the deck~~
        - ~~update - update the tags associated with the deck~~