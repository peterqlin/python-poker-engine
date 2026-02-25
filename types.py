import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self, shuffle=True):
        self.deck = []
        suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        for rank in range(2, 15): # 2 through 14 (ace)
            for suit in suits:
                self.deck.append(Card(rank, suit))
        if shuffle:
            random.shuffle(self.deck) # apply fisher-yates to shuffle in-place

    def __repr__(self):
        return "\n".join([card.__repr__() for card in self.deck])

    def remove_cards(self, count):
        """
        remove some number of cards from the deck and return a list of the removed cards
        """
        removed = self.deck[-count:]
        for _ in range(count): self.deck.pop()
        return removed

class Player:
    def __init__(self, id: int, hand: list[Card], money: int):
        self.id = id
        self.hand = hand
        self.money = money

    def __repr__(self):
        return f"Player {self.id} (hand: {self.hand}, stack: {self.money})"

    def add_cards(self, cards: list[Card]):
        """
        add one or more cards to a player's hand
        """
        self.hand.extend(cards)

    def reset_cards(self):
        """
        remove all cards from a player's hand
        """
        self.hand = []

    def bet(self, amount):
        """
        place a bet
        """
        assert amount <= self.money, "Bet exceeds player's funds"
        self.money -= amount

