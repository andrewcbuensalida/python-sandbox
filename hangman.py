import random

print("Welcome=====================")
secret_words = ["medium", "hot", "cool"]
secret_word = random.choice(secret_words)
secret_word_list = list(secret_word)
# print(secret_word_list)
displayed_word_list = []
len_secret_word = len(secret_word)
num_correct_guesses = 0
for num in range(len_secret_word):
    # displayed_word_list += "_"
    displayed_word_list.append("_") # alternative

while True:
    print(" ".join(displayed_word_list) + "\n")
    guessed_letter = input("Guess a letter: ").lower()
    guessed_correctly = False

    if guessed_letter not in displayed_word_list:
        for index in range(len(secret_word_list)):
            if secret_word_list[index] == guessed_letter:
                displayed_word_list[index] = guessed_letter
                guessed_correctly = True
                num_correct_guesses += 1
        else:
            print('done')
        if not guessed_correctly:
            print("Wrong!\n ")
    else:
        print("You already guessed that letter!\n ")

    # if num_correct_guesses == len_secret_word:
    if '_' not in displayed_word_list: # alternative. 2 lines less.
        print(" ".join(displayed_word_list) + "\n")
        print("You win!\n")
        break


print("Good bye")
