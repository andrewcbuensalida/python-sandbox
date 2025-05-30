import random
from functools import reduce
from typing import List


class Card:
    def __init__(self, rank, suit) -> None:
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f"{self.rank['rank']} of {self.suit}"


class Deck:
    ranks = [
        {"rank": "A", "value": 11},
        {"rank": "2", "value": 2},
        {"rank": "3", "value": 3},
        {"rank": "4", "value": 4},
        {"rank": "5", "value": 5},
        {"rank": "6", "value": 6},
        {"rank": "7", "value": 7},
        {"rank": "8", "value": 8},
        {"rank": "9", "value": 9},
        {"rank": "10", "value": 10},
        {"rank": "J", "value": 10},
        {"rank": "Q", "value": 10},
        {"rank": "K", "value": 10},
    ]
    suits = ["spades", "hearts", "diamonds", "clubs"]
    cards: List[Card] = []

    def generate_ordered(self):
        # empty deck
        self.cards.clear()
        for suit in self.suits:
            for rank in self.ranks:
                card = Card(rank, suit)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self) -> Card:
        return self.cards.pop()


class Hand:
    def __init__(self, is_dealer=False) -> None:
        self.is_dealer = is_dealer
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        temp_value = reduce(
            lambda accum, curr: accum + curr.rank["value"], self.cards, 0
        )
        # Aces 1 if value is over 21
        number_of_aces = len(
            [card for card in self.cards if card.rank["rank"] == "A"]
        )  # could also do len(list(filter(lambda))) instead of this
        while temp_value > 21 and number_of_aces > 0:
            temp_value -= 10
            number_of_aces -= 1
        self.value = temp_value

    def display(self, initial_deal=False, is_dealer=False):
        print(f"\n{'Dealer' if is_dealer else 'Player'}'s cards:")
        # loop through cards
        for index, card in enumerate(self.cards):
            # if it's the first deal to the dealer, hide the card
            if initial_deal and index == 0:
                print("Hidden")
                continue
            print(card)

        if not initial_deal or not is_dealer:
            print(f"Value: {self.value}")

    def check_blackjack(self):
        return True if self.value == 21 else False


class Game:
    def play(self):
        number_of_games_choice = int(input("How many games do you want to play?: "))
        number_of_games_remaining = number_of_games_choice
        deck = Deck()
        deck.generate_ordered()
        deck.shuffle()
        number_of_wins = 0

        while number_of_games_remaining > 0:
            print(
                f"\n{number_of_games_choice - number_of_games_remaining + 1} out of {number_of_games_choice} games................."
            )
            print(
                f"Win percentage is {100*(number_of_wins/(1 if  number_of_games_choice - number_of_games_remaining == 0 else number_of_games_choice - number_of_games_remaining))}%"
            )
            # if number of cards left in deck is less than 17, regenerate and shuffle
            if len(deck.cards) < 17:
                deck.generate_ordered()
                deck.shuffle()

            dealer_hand = Hand(True)
            player_hand = Hand()
            # deal 2 cards to player and 2 cards to dealer. 1 of the cards of the dealer is hidden.
            player_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())
            player_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())

            # calculate value
            player_hand.calculate_value()
            dealer_hand.calculate_value()

            # display cards and value
            player_hand.display()
            dealer_hand.display(initial_deal=True, is_dealer=True)

            # check if player got blackjack
            if player_hand.check_blackjack():
                print("You got a blackjack!")
                number_of_games_remaining -= 1
                number_of_wins += 1
                continue
            # loop hit or stand. If hit, deal a card to the player. If stand, dealer's turn.
            while player_hand.value <= 21:
                hit_or_stand = input("(h)it or (s)tand?: ")
                if hit_or_stand == "h":
                    player_hand.add_card(deck.deal_card())
                    player_hand.calculate_value()
                    player_hand.display()
                    if player_hand.value > 21:
                        break
                # if player chooses to stand, break
                if hit_or_stand == "s":
                    break

            # if player busts
            if player_hand.value > 21:
                print("You busted!")
                number_of_games_remaining -= 1
                continue

            # dealer's turn to hit if less than 17, or stand more than or equal
            while dealer_hand.value < 17:
                dealer_hand.add_card(deck.deal_card())
                dealer_hand.calculate_value()

            dealer_hand.display(is_dealer=True)
            # check results

            # if dealer busts
            if dealer_hand.value > 21:
                print("Dealer busted. You win!")
                number_of_wins += 1
            # if tie
            elif dealer_hand.value == player_hand.value:
                print("It's a tie!")
            # if dealer wins
            elif dealer_hand.value > player_hand.value:
                print("Dealer wins!")
            # if player wins
            elif dealer_hand.value < player_hand.value:
                print("You win!")
                number_of_wins += 1

            number_of_games_remaining -= 1


g = Game()
g.play()
