import random

def generate_number():
    return random.randint(1, 100)

def guess_number():
    number = generate_number()

    attempts = 5
    while attempts > 0:
        guess = int(input('Guess: '))
        if guess == number:
            return 'You won'
        elif guess > number:
            print('Too high\n')
            attempts -= 1
        else:
            print('Too low\n')
            attempts -= 1

    print('You lost')