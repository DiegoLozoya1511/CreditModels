import random

words = [
    "cat", "dog", "sun", "book", "tree",
    "apple", "house", "plant", "river", "music",
    "python", "diamond", "journey", "library",
    "computer", "elephant", "mountain"
]

HANGMAN_PICS = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
    """
]

def get_word(words):
    ind = random.randint(0, len(words))
    return words[ind].upper()


def get_guess():
    while True:
        guess = input("\nGuess a letter or the full word: ").upper()

        if not guess.isalpha():
            print("Please enter letters only.")
            continue

        return guess

    

def check_letter(word, display, guess, attempts):
    if guess in word:
        for i in range(len(word)):
            if word[i] == guess:
                display[i] = guess
    else:
        attempts -=1
        print(f'   {guess} is not in word. {attempts} attempts remaining')
    return display, attempts


def guessed_letters(used_letters, guess):
    if guess in used_letters:
        print('You have already used this letter')
        return False
    else:
        used_letters.append(guess)
        return True


def check_win(display):
    return '_' not in display
        

def guess_word():
    word = get_word(words)
    display = ["_"] * len(word)

    max_attempts = len(HANGMAN_PICS) - 1
    attempts = max_attempts
    used_letters = []

    while attempts > 0:
        wrong_guesses = max_attempts - attempts
        print(HANGMAN_PICS[wrong_guesses])

        print("\nWord to guess:")
        print(" ".join(display))

        if used_letters:
            print("\nUsed letters:", " ".join(used_letters))

        guess = get_guess()

        # ---- FULL WORD GUESS ----
        if len(guess) > 1:
            if guess == word:
                print(HANGMAN_PICS[max_attempts - attempts])
                print("\nThe word was:", " ".join(word))
                return "\n🎉 You win!"
            else:
                attempts -= 1
                print(f"   {guess} is not the word. {attempts} attempts remaining.")
                continue

        # ---- SINGLE LETTER GUESS ----
        if not guessed_letters(used_letters, guess):
            continue

        display, attempts = check_letter(word, display, guess, attempts)

        if check_win(display):
            print(HANGMAN_PICS[max_attempts - attempts])
            print("\nThe word was:", " ".join(word))
            return "\n🎉 You win!"

    return f"{HANGMAN_PICS[max_attempts - attempts]}\n💀 You lose. The word was {word}"



result = guess_word()
print(result)