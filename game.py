from time import sleep

from deck import Deck
from player import Player
from tabletop import Tabletop

from collections import Counter, deque
from random import randrange

PLAYERS = 5
HAND_LIMIT = 7
SCORE_LIMIT = 100
ROUND_LIMIT = 10
NUMBER_OF_CARDS = 100
STORYTELLER_NONE = 0  # or ALL
#STORYTELLER_ALL = 0  # redundant
STORYTELLER_FEW = 3
GUESSER_WRONG = 0
GUESSER_CORRECT_FEW = 3
GUESSER_CORRECT_NONE = 2  # or ALL
#GUESSER_CORRECT_ALL = 2  # redundant
DECOY_SUCCESS = 1  # for each


class Game():
    def __init__(self, n_players, score_limit=SCORE_LIMIT, round_limit=ROUND_LIMIT):
        self.n_players = n_players
        self.players = [Player(i) for i in range(n_players)]
        # players[0] is always the storyteller, others are guessers
        # players rotate at the end of the turn
        self.deck = Deck(n_cards=NUMBER_OF_CARDS)
        self.tabletop = Tabletop()
        self.scores = Counter({p.id: 0 for p in self.players})
        self.score_limit = score_limit
        self.round_limit = round_limit
        self.clue = None
        self.i_turn = 0

    def start(self):
        # put all cards back in the deck and shuffle
        self.tabletop.discard_all()
        for player in self.players:
            self.deck.discard(player.discard_all())
        self.deck.reshuffle_free_deck()
        # deal out cards
        for player in self.players:
            for i in range(HAND_LIMIT):
                player.receive(self.deck.draw())
        # randomly select storyteller
        # self.players.rotate(randrange(self.n_players))
        # reset turn counter
        self.i_turn = 0
        # run main loop
        self.loop()

    def loop(self):
        while self.i_turn // self.n_players < self.round_limit \
                and max(self.scores.values()) < self.score_limit:
            # storyteller plays a (card, clue) tuple
            self.storyteller_phase()
            # other players each play a card
            self.guesser_phase()
            # evaluate board and award scores
            self.scoring_phase()
            # each player draws a card
            # rotate player roles
            self.cleanup_phase()
            self.i_turn += 1
            print(self.scores)
        self.end()

    def end(self):
        print(f"Game finished in {self.i_turn} turns ({self.i_turn // self.n_players} rounds)")
        print(self.scores)

    def storyteller_phase(self):
        card, self.clue = self.players[0].play_story()
        self.tabletop.place_card(card, self.players[0].id)

    def guesser_phase(self):
        for player in self.players[1:]:
            self.tabletop.place_card(player.play_decoy(self.clue), player.id)
        on_table = self.tabletop.show()
        for player in self.players[1:]:
            guess = player.play_guess(on_table)
            self.tabletop.place_token(guess, player.id)

    def scoring_phase(self):
        # evaluate storyteller's card
        # --case ALL or NONE
        if self.tabletop.count_tokens(self.players[0].id) in (0, self.n_players-1):
            self.scores[self.players[0].id] += STORYTELLER_NONE
            for token in self.players[1:]:
                self.scores[token.id] += GUESSER_CORRECT_NONE
        # --case DEFAULT
        else:
            self.scores[self.players[0].id] += STORYTELLER_FEW
            for token_id in self.tabletop.get_tokens(self.players[0].id):
                self.scores[token_id] += GUESSER_CORRECT_FEW
        # evaluate other cards
        for decoy in self.players[1:]:
            for token_id in self.tabletop.get_tokens(decoy.id):
                self.scores[token_id] += GUESSER_WRONG
                self.scores[decoy.id] += DECOY_SUCCESS

    def cleanup_phase(self):
        self.deck.discard(self.tabletop.discard_all())
        for player in self.players:
            player.receive(self.deck.draw())
        self.players.append(self.players.pop(0))


def main():
    g = Game(n_players=PLAYERS)
    g.start()


if __name__ == '__main__':
    main()
