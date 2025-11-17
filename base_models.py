import os


class Phrase:

    def __init__(self, title: str, phrase_to_guess: str):
        self.title: str = title
        self.phrase_to_guess: str = phrase_to_guess
        self.current_guess = self._initialize_current_guess()

    def _initialize_current_guess(self) -> list[str]:
        current_guess = []
        for char in self.phrase_to_guess:
            if char.isalpha():
                current_guess.append('_')
            else:
                current_guess.append(char)

        return current_guess

    def print(self):
        print(f'Argomento: {self.title}')
        print(''.join([e for e in self.current_guess]))

    def add_letter_to_current_guess(self, letter: str):
        letter_found = False
        for idx, el in enumerate(self.phrase_to_guess):
            if el.lower() == letter.lower():
                self.current_guess[idx] = el
                letter_found = True
        if letter_found:
            os.system('cls')
            self.print()
        else:
            self.print_error()

    def is_equal_to(self, tentative_phrase: str) -> bool:
        return tentative_phrase.lower() == self.phrase_to_guess.lower()

    def check_completed(self) -> bool:
        for el in self.current_guess:
            if el == '_':
                return False
        return True

    @staticmethod
    def print_error():
        print('❌❌❌❌❌❌❌')
        input()
