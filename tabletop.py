from random import shuffle


class Tabletop:
    def __init__(self):
        self._cards = {}
        self._owners = {}

    def place_card(self, card, player_id):
        self._cards[card] = {"owner": player_id, "tokens": set()}
        self._owners[player_id] = card

    def place_token(self, card, player_id):
        self._cards[card]["tokens"].add(player_id)

    def show(self):
        cards = list(self._cards.keys())
        shuffle(cards)
        return cards

    def count_tokens(self, player_id):
        return len(self._cards[self._owners[player_id]]["tokens"])

    def get_tokens(self, player_id):
        return self._cards[self._owners[player_id]]["tokens"]

    def discard_all(self):
        cards = set(self._cards.keys())
        self._cards = {}
        self._owners = {}
        return cards
