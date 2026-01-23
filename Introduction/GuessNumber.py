import random

def generate_number():
    return random.randint(1, 100)


def get_guess():
    while True:
        try:
            return int(input('Guess: '))
        except ValueError:
            print('Please enter a valid number.')


def check_win(number, guess):
    return guess == number


def guess_number():
    number = generate_number()
    attempts = 5

    while attempts > 0:
        guess = get_guess()

        if check_win(number, guess):
            return 'You won!'

        attempts -= 1

        if guess > number:
            print(f'Too high. {attempts} attempts remaining\n')
        else:
            print(f'Too low. {attempts} attempts remaining\n')

    return f'You lost. Nummber was {number}'


result = guess_number()
print(result)