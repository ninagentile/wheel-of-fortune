import os

from phrases import phrases


def guessed_phrase_behaviour(phrase):
    phrase.current_guess = tentative_phrase
    print('Complimenti, hai indovinato!!!')
    print('Premi un pulsante per passare alla prossima frase')
    input()


for phrase in phrases:
    os.system('cls')
    phrase.print()
    while phrase.check_completed() is False:
        os.system('cls')
        phrase.print()
        print(
            'Cosa vuoi fare? A do la soluzione, un pulsante qualsiasi '
            'per dare una lettera'
        )
        move = input()

        if move.lower() != 'a':
            print('Inserisci la lettera')
            letter = input()
            phrase.add_letter_to_current_guess(letter=letter)
            if phrase.check_completed():
                guessed_phrase_behaviour(phrase)
        else:
            print('Digita la frase')
            tentative_phrase = input()
            if phrase.is_equal_to(tentative_phrase):
                guessed_phrase_behaviour(phrase)
            else:
                phrase.print_error()
