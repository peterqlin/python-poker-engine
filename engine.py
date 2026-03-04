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
        self.num_players = len(players)

    # TODO: add bet validation logic
    def input_bet(self, action_idx):
        done_betting = False
        while not done_betting:
            try:
                print("enter bet: ", end="")
                bet_amount = int(input())
                done_betting = True
            except Exception as e:
                print(f"try again: {e}")
        return bet_amount

    def betting_round(self, start_player_idx=0, min_bet=0, initial_bets=None):
        """
        simulate one round of betting
        """
        bets = [0] * self.num_players
        if initial_bets: # add initial bets, like blinds or straddles
            for i, b in enumerate(initial_bets):
                bets[i] = b

        current_bet = min_bet
        min_raise_amount = min_bet
        hand_done = False
        acted_indices = []
        inc = 0
        while not hand_done:
            action_idx = (start_player_idx + inc) % self.num_players # who is the action on
            if self.active[action_idx]: # only let active players act
                print(f"action is on player {self.players[action_idx].id}")
                bet = self.input_bet(action_idx)
                print(f"{self.players[action_idx].id} bets {bet}")
                if bet == 0: # interpret bet 0 as fold or check depending on context
                    if current_bet > 0:
                        self.active[action_idx] = False

                # hand is done when either one player is active or all active players have acted
                # if one player is active, then no future streets should play out; the hand is over
                active_indices = [i for i, _ in enumerate(self.players) if self.active[i]]
                active_bets = [bets[i] for i in active_indices]
                print(f"{active_indices=}")
                print(f"{active_bets=}")
                hand_done = len(active_indices) == 1 or set(active_indices) == set(acted_indices)
            inc += 1 # increment action index

# TODO: implement no limit, then generalize and create a game-agnostic engine that can easily be adapted to limit and PLO

class NoLimitHoldemEngine:
    """
    engine to play arbitrarily many rounds of no limit holdem
    """

    # TODO: figure out how to manage players joining and leaving tables (this should live at a different level of abstraction)
    # when players leave/join, a whole new engine needs to be created, which is bad since we don't want to shuffle seats every time this happens
    def __init__(self, num_players=2, small_blind=5, big_blind=10, hand_size=2, seed=42):
        """
        shuffle deck, create players, and set initial stage
        """
        assert num_players > 1, "Not enough players"

        random.seed(seed) # seed for reproducibility
        self.deck = Deck()
        self.num_players = num_players
        self.players = [Player(chr(ord("A") + i), [], 100) for i in range(num_players)]
        self.hand_size = hand_size # how many cards each player has
        self.stage = "setup" # setup -> deal -> preflop -> flop -> turn -> river -> back to deal

        self.active = [True] * num_players
        self.small_blind = small_blind
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

    # TODO: abstract out the concept of a street instead of hardcoding them all, esp because hands can end at earlier streets
    def preflop(self):
        assert self.stage == "preflop", "Current stage is not 'preflop'"

        # UTG sits at index 2 (after SB and BB)
        utg_idx = 2 % self.num_players # prevent out of bounds access when there are only 2 players

        # enforce small blind and big blind
        # players array has length at least 2, so indexing 0 and 1 is safe here
        # TODO: handle edge case when blind puts player all-in
        self.players[0].remove_money(self.small_blind)
        self.players[1].remove_money(self.big_blind)

        self.b.betting_round(start_player_idx=utg_idx, min_bet=self.big_blind, initial_bets=[self.small_blind, self.big_blind])
        self.stage = "flop"

    def flop(self):
        assert self.stage == "flop", "Current stage is not 'flop'"
        self.stage = "turn"

    def turn(self):
        assert self.stage == "turn", "Current stage is not 'turn'"
        self.stage = "river"

    def river(self):
        assert self.stage == "river", "Current stage is not 'river'"
        self.stage = "showdown"


