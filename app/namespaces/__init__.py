from .auth import login, register
from .deck import deck, decks
from .card import card, cards
from .review import review_NS
from .tag import tag, tags

ns_list = (
    login,register,
    deck,decks,
    card,cards,
    review_NS,
    tag,tags
)