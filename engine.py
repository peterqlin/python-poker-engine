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

    def betting_round(self, start_player_idx=0):
        """
        simulate one round of betting starting with player at start_player_idx
        skips over inactive players
        """
        print("begin betting round")
        done = False
        p_idx = start_player_idx
        bets = [0] * self.num_players
        max_bet = 0
        if start_player_idx != 0: # preflop means BB and SB have bets
            bets[0], bets[1] = self.big_blind // 2, self.big_blind # assume integer blinds and bets
        while not done:
            if self.active[p_idx]:
                self.players[p_idx].bet(self.big_blind) # TODO: bet validation based on game state
                bets[p_idx] += self.big_blind # yea none of this works without good bet validation
                max_bet = max(max_bet, bets[p_idx])
            p_idx = (p_idx + 1) % self.num_players
            print(f"bets tuple: {tuple(bets[i] for i in range(self.num_players) if self.active[i])}")
            done = tuple(bets[i] for i in range(self.num_players) if self.active[i]) == (max_bet for i in range(self.num_players) if self.active[i])


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
        self.players = [Player(i, [], 100) for i in range(num_players)]
        self.hand_size = hand_size
        self.stage = "setup" # setup -> deal -> preflop -> flop -> turn -> river -> back to deal

        self.active = [True] * num_players
        self.big_blind = big_blind
        self.b = NoLimitBettingEngine(self.players, self.active, self.big_blind)

    def show(self):
        print(f"stage: {self.stage}")
        for player in self.players:
            print(player)

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

    def preflop(self):
        assert self.stage == "preflop", "Current stage is not 'preflop'"
        # UTG sits at index 2 (after SB and BB)
        utg_idx = 2 % self.num_players # prevent out of bounds access when there are only 2 players
        # TODO: abstract betting loop into a reusable BettingEngine
        self.b.betting_round(start_player_idx=utg_idx)

        self.stage = "flop"

    def flop(self):
        pass

    def turn(self):
        pass

    def river(self):
        pass

