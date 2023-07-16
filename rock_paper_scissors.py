import random

def get_choices():
    player_choice = input("Rock, paper, or scissors? ")
    options = ["rock","paper","scissors"]
    # random_index = (random.random() * 3).__floor__()
    # computer_choice = options[random_index]
    # OR
    computer_choice = random.choice(options)
    choices = {"player": player_choice, "computer": computer_choice}

    return choices

def check_win(choices):
    # print("The computer chose " + choices["computer"])
    #  OR
    print(f"The computer chose {choices['computer']}")
    if choices["player"] == "rock" and choices["computer"] == "rock":
        return "Draw"
    if choices["player"] == "rock" and choices["computer"] == "paper":
        return "You lose"
    if choices["player"] == "rock" and choices["computer"] == "scissors":
        return "You win"
    


def play():
    choices = get_choices()
    # print(choices)
    print(check_win(choices))


play()
