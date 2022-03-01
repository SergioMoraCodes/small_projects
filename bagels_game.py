import random

num_digits = 3
max_guesses = 10

def main():
    print('''

    Adivina el número.
    Estoy pensando en un número de {} dígitos sin repetir
    Trata de adivinar, tienes {} intentos
    Cada intento te daré las siguientes pistas:

        Casi    =   un dígito es correcto pero en la posición equivocada
        Bien =  un dígito es correcto y está en posición
        Nada    =   no tienes ningún dígito correcto


    '''.format(num_digits,max_guesses))

    while True:
        secret_num = get_secret()
        print('ya pensé un número, tienes {} intentos'.format(max_guesses))
        guess_number = 1

        while guess_number <=max_guesses:
            guess = ''
            while len(guess) != num_digits or not guess.isdecimal():
                print('intento #{}: '.format(guess_number))
                guess = input('> ')

            clues = get_clues(guess,secret_num)
            print(clues)
            guess_number += 1

            if guess == secret_num:
                break
            if guess_number > max_guesses:
                print('Te quedaste sin intentos')
                print(f'The answer was {secret_num}')
        print('Quieres jugar de nuevo? (Y/N)')
        if not input('> ').lower().startswith('y'):
            break
    print('Gracias por jugar')



def get_secret():
    numbers = list('0123456789')
    random.shuffle(numbers)

    secret = ''
    for i in range(num_digits):
        secret += str(numbers[i])
    return secret

def get_clues(guess, secret_num):
    if guess == secret_num:
        return 'Adivinaste! Bravo!'

    clues = []

    for i in range(num_digits):
        if guess[i]==secret_num[i]:
            clues.append('Bien')
        elif guess[i] in secret_num:
            clues.append('Casi')
    if len(clues) == 0:
        return 'Nada'
    else:
        clues.sort()
        return ' '.join(clues)

if __name__=='__main__':
    main()