import os
import threading
import time


stop_flag = False
total_seconds = 60


def countdown(seconds):
    global stop_flag
    global total_seconds
    total_seconds = seconds
    while not stop_flag:
        if total_seconds < 0:
            print('\nTempo scaduto!')
            stop_flag = True
            break
        print(f'\rTempo rimanente: {total_seconds}s    ', end='')
        time.sleep(1)
        total_seconds -= 1


def get_input():
    global stop_flag
    input()
    stop_flag = True


def get_input_third_match(phrase):
    global total_seconds
    global stop_flag
    inserted_vowels = False
    curr_phrase = ''.join([e for e in phrase.current_guess])
    print(f'\r{curr_phrase}')

    while total_seconds > 0:
        letter = input()

        # type a number to give the answer
        if letter.isnumeric():
            stop_flag = True
            return

        is_vowel = letter in ['a', 'e', 'i', 'o', 'u']

        # Otherwise insert the letter
        if is_vowel:
            if inserted_vowels:
                score = 0
            else:
                score = phrase.add_letter_to_current_guess_and_compute_score(
                    letter, value=1
                )
                inserted_vowels = True
        else:
            score = phrase.add_letter_to_current_guess_and_compute_score(
                letter, value=1
            )

        # If letter is wrong: decrement seconds
        if score == 0:
            total_seconds -= 3
            print('\r❌❌❌❌❌❌❌')

        # Otherwise print
        os.system('cls')
        curr_phrase = ''.join([e for e in phrase.current_guess])
        print(f'\r{curr_phrase}')


def start_match_with_time(remaining_seconds: int) -> tuple[int, str]:
    global stop_flag
    global total_seconds
    total_seconds = remaining_seconds
    stop_flag = False
    print('Premi un tasto per fermare il tempo e dare la risposta')
    timer_thread = threading.Thread(target=countdown, args=(total_seconds,))
    input_thread = threading.Thread(target=get_input)

    timer_thread.start()
    input_thread.start()

    input_thread.join()
    stop_flag = True
    timer_thread.join()

    print(f'\nTimer fermato: {total_seconds}')
    answer = input('Scrivi la tua risposta: ')
    return total_seconds, answer


def start_third_match_with_time(
    remaining_seconds: int, phrase
) -> tuple[int, str]:
    global stop_flag
    global total_seconds
    total_seconds = remaining_seconds
    stop_flag = False
    print('Digita un numero per fermare il tempo e dare la risposta')
    timer_thread = threading.Thread(target=countdown, args=(total_seconds,))
    input_thread = threading.Thread(
        target=get_input_third_match, args=(phrase,)
    )

    timer_thread.start()
    input_thread.start()

    input_thread.join()
    stop_flag = True
    timer_thread.join()

    answer = ''
    if total_seconds > 0:
        print(f'\nTimer fermato')
        answer = input('Scrivi la tua risposta: ')
    else:
        print(f'\nTempo scaduto')
    return total_seconds, answer
