import os
import random
from enum import Enum
from random import choice

vowel_cost = 300


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

    def add_letter_to_current_guess_and_compute_score(
        self, letter: str, value: int
    ) -> int:
        n_letters_found = 0
        for idx, el in enumerate(self.phrase_to_guess):
            if el.lower() == letter.lower():
                # Insert letter
                self.current_guess[idx] = el
                # Update score
                n_letters_found += 1

        return n_letters_found * value

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


class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.temp_score = 0

    def increase_score(self, n_points: int):
        self.score += n_points

    def increase_temp_score(self, n_points: int):
        self.temp_score += n_points

    def decrease_score(self, n_points: int):
        self.increase_score(-n_points)

    def decrease_temp_score(self, n_points: int):
        self.increase_temp_score(-n_points)

    def win_match(self):
        self.increase_score(self.temp_score)

    def bankrupt(self):
        self.score = 0
        self.temp_score = 0

    def reset_temp_score(self):
        self.temp_score = 0

    def print_scores(self):
        print(
            f'\n {self.name} \n'
            f'Score: {self.temp_score} \n'
            f'Total: {self.score}\n'
        )


class Slice:
    def __init__(self, value: str | int):
        self.value = value


class Wheel:
    def __init__(self):
        self.slices = self._initialize_slices()

    def turn_wheel(self) -> str | int:
        chosen_slice = random.choice(self.slices)
        return chosen_slice.value

    @staticmethod
    def _initialize_slices() -> list[Slice]:
        slices = []
        for i in range(20):
            slices.append(
                Slice(value=choice([100, 200, 300, 400, 500, 600, 700]))
            )
        slices.append(Slice(value='Bancarotta'))
        slices.append(Slice(value='Bancarotta'))
        slices.append(Slice(value='Passa'))
        slices.append(Slice(value='Passa'))

        return slices


class MatchResult(Enum):
    WIN = 'win'
    LOSE = 'lose'
    KEEP_PLAYING = 'keep_playing'


class Match:
    def __init__(self, wheel: Wheel, player: Player, phrase: Phrase):
        self.wheel = wheel
        self.player = player
        self.phrase = phrase

    def play_match(self):
        match_result = MatchResult.KEEP_PLAYING
        while match_result == MatchResult.KEEP_PLAYING:
            os.system('cls')
            self.phrase.print()
            self.player.print_scores()
            print("Cosa vuoi fare?")
            print("1) Girare la ruota")
            print("2) Comprare una vocale")
            print("3) Dare la soluzione")
            choice = input()
            match choice:
                case '1':
                    match_result = self._spin_wheel_and_play()
                case '2':
                    match_result = self._insert_vowel()
                case '3':
                    match_result = self._give_solution()

        return match_result

    def _spin_wheel_and_play(self) -> MatchResult:
        slice_value = self.wheel.turn_wheel()
        input(f'Risultato: {slice_value}')
        if isinstance(slice_value, int):
            return self._play(slice_value, is_vowel=False)
        elif slice_value.lower() == 'bancarotta':
            self.player.bankrupt()
            return MatchResult.LOSE
        elif slice_value.lower() == 'passa':
            return MatchResult.LOSE

    def _insert_vowel(self) -> MatchResult:
        if self._check_vowel_can_be_inserted():
            match_result = self._play(slice_value=0, is_vowel=True)
            self.player.decrease_temp_score(vowel_cost)
            return match_result
        else:
            return MatchResult.LOSE

    def _check_vowel_can_be_inserted(self) -> bool:
        return self.player.temp_score >= vowel_cost

    def _play(self, slice_value: int, is_vowel: bool) -> MatchResult:
        if is_vowel:
            print('Inserire la vocale')
            slice_value = 1
        else:
            print('Inserire la consonante')
        letter = input()
        score = self.phrase.add_letter_to_current_guess_and_compute_score(
            letter=letter, value=slice_value
        )
        if score > 0:
            if is_vowel is False:
                self.player.increase_temp_score(score)
            return MatchResult.KEEP_PLAYING
        return MatchResult.LOSE

    def _give_solution(self) -> MatchResult:
        print('Digita la soluzione')
        solution = input()
        if self.phrase.is_equal_to(solution):
            self.player.increase_temp_score(1000)
            return MatchResult.WIN
        return MatchResult.LOSE
