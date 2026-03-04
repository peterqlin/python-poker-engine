from engine import NoLimitHoldemEngine

def main():
    holdem = NoLimitHoldemEngine(num_players=2)
    holdem.show()
    holdem.setup()
    holdem.show()
    holdem.deal_cards()
    holdem.show()
    holdem.preflop()
    holdem.show()
    holdem.flop()
    holdem.show()
    holdem.turn()
    holdem.show()
    holdem.river()
    holdem.show()
    

if __name__ == "__main__":
    main()
