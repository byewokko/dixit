from random import shuffle


class Deck:
    def __init__(self, n_cards=None):
        self._draw_pile = [i for i in range(n_cards)]
        self._discard_pile = []

    def draw(self):
        if not self._draw_pile:
            self.reshuffle_free_deck()
        return self._draw_pile.pop()

    def discard(self, card_or_list):
        if isinstance(card_or_list, (list, set, tuple)):
            for card in card_or_list:
                assert isinstance(card, int)
                self._discard_pile.append(card)
        else:
            assert isinstance(card_or_list, int)
            self._discard_pile.append(card_or_list)

    def reshuffle_free_deck(self):
        while self._discard_pile:
            self._draw_pile.append(self._discard_pile.pop())
        self.shuffle_draw_pile()

    def shuffle_draw_pile(self):
        shuffle(self._draw_pile)
