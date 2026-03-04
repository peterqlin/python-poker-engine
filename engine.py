import random
from types import Deck, Player

class NoLimitBettingEngine:
    """
    simulate no limit betting sequence
    """

    def __init__(self, players, active, big_blind):
        """
        MUTATES players and active lists
        """
        self.players = players
        self.active = active
        self.big_blind = big_blind
        self.total_bet = 0
        self.num_players = len(players)

    def betting_round(self, start_player_idx=0, min_bet=0):
        """
        simulate one round of betting
        """
        current_bet = min_bet
        min_raise_amount = min_bet
        for i in range(self.num_players):
            p = self.players[(start_player_idx + i) % self.num_players] # wraparound to prevent list out of range
            print(f"action is on player {p.id}")
            valid_bet_made = False
            while not valid_bet_made:
                try:
                    print(f"Enter bet amount for player {p.id}: ", end="")
                except Exception as e:
                    print(f"Try again: {e}")

# TODO: implement no limit, then generalize and create a game-agnostic engine that can easily be adapted to limit and PLO

class NoLimitHoldemEngine:
    """
    engine to play arbitrarily many rounds of no limit holdem
    """

    # TODO: figure out how to manage players joining and leaving tables (this should live at a different level of abstraction)
    # when players leave/join, a whole new engine needs to be created, which is bad since we don't want to shuffle seats every time this happens
    def __init__(self, num_players=2, big_blind=10, hand_size=2, seed=42):
        """
        shuffle deck, create players, and set initial stage
        """
        assert num_players > 1, "Not enough players"

        random.seed(seed) # seed for reproducibility
        self.deck = Deck()
        self.num_players = num_players
        self.players = [Player(chr(ord("A") + i), [], 100) for i in range(num_players)]
        self.hand_size = hand_size
        self.stage = "setup" # setup -> deal -> preflop -> flop -> turn -> river -> back to deal

        self.active = [True] * num_players
        self.big_blind = big_blind
        self.b = NoLimitBettingEngine(self.players, self.active, self.big_blind)

    def show(self):
        print(f"stage: {self.stage}")
        for player in self.players:
            print(player)
        print()

    def setup(self):
        """
        create random seating order
        small blind is at index 0 in the list
        """
        assert self.stage == "setup", "Current stage is not 'setup'"
        random.shuffle(self.players)
        self.stage = "deal"

    def deal_cards(self):
        """
        deal cards from leftmost to rightmost player
        """
        assert self.stage == "deal", "Current stage is not 'deal'"
        for _ in range(self.hand_size):
            for player in self.players: # we can iterate like this because self.players[0] is small blind
                dealt_cards = self.deck.remove_cards(1)
                player.add_cards(dealt_cards)
        self.stage = "preflop"

    # TODO: abstract out the concept of a street instead of hardcoding them all
    def preflop(self):
        assert self.stage == "preflop", "Current stage is not 'preflop'"
        # UTG sits at index 2 (after SB and BB)
        utg_idx = 2 % self.num_players # prevent out of bounds access when there are only 2 players
        self.b.betting_round(start_player_idx=utg_idx, min_bet=self.big_blind)
        self.stage = "flop"

    def flop(self):
        assert self.stage == "flop", "Current stage is not 'flop'"
        self.b.betting_round()
        self.stage = "turn"

    def turn(self):
        assert self.stage == "turn", "Current stage is not 'turn'"
        self.b.betting_round()
        self.stage = "river"

    def river(self):
        assert self.stage == "river", "Current stage is not 'river'"
        self.b.betting_round()
        self.stage = "showdown"


