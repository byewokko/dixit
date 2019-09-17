from random import choice

class Player:
    def __init__(self, id):
        self.id = id
        self._hand = set()
        self._decoy_card = None

    def play_story(self):
        # play random
        return self._hand.pop(), "some clue"

    def play_decoy(self, clue):
        # play random
        self._decoy_card = self._hand.pop()
        return self._decoy_card

    def play_guess(self, cards):
        actions = set(cards)
        actions.discard(self._decoy_card)
        # play random
        return actions.pop()

    def discard_all(self):
        cards = list(self._hand)
        self._hand = set()
        return cards

    def receive(self, card):
        assert isinstance(card, int)
        self._hand.add(card)


