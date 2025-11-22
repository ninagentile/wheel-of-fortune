import os
import random
import sys
from abc import abstractmethod, ABC
from datetime import datetime
from time import sleep
from enum import Enum
from random import choice

from timing import start_match_with_time, start_third_match_with_time

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

    def reveal_start_and_end(self):
        for idx, el in enumerate(self.current_guess):
            if idx == 0:
                self.current_guess[idx] = self.phrase_to_guess[idx]
            else:
                if self.current_guess[idx].isalpha() is False and (
                    self.current_guess[idx] != '_'
                ):
                    self.current_guess[idx - 1] = self.phrase_to_guess[idx - 1]
                    if idx + 1 <= len(self.current_guess) - 1:
                        self.current_guess[idx + 1] = self.phrase_to_guess[
                            idx + 1
                        ]

                if idx == len(self.current_guess) - 1:
                    self.current_guess[idx] = self.phrase_to_guess[idx]


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
            f'\n {self.name} \nScore: {self.temp_score} \nTotal: {self.score}\n'
        )


class Slice:
    def __init__(self, value: str | int):
        self.value = value


class AbstractWheel(ABC):
    def __init__(self):
        self.slices: list[Slice] = self._initialize_slices()

    def turn_wheel(self) -> str | int:
        chosen_slice = random.choice(self.slices)
        return chosen_slice.value

    @staticmethod
    @abstractmethod
    def _initialize_slices() -> list[Slice]:
        pass


class Wheel(AbstractWheel):
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


class WonderWheel(AbstractWheel):
    """
    Final wheel
    """

    def __init__(self):
        super().__init__()
        # Shuffle slices
        random.shuffle(self.slices)

    def turn_wheel(self) -> list[str | int]:
        chosen_slice_idx = random.randint(0, len(self.slices) - 1)
        first_slice_idx = chosen_slice_idx - 1
        if first_slice_idx < 0:
            first_slice_idx = len(self.slices) - 1
        third_slice_idx = chosen_slice_idx + 1
        if third_slice_idx == len(self.slices):
            third_slice_idx = 0

        first_slice = self.slices[first_slice_idx].value
        middle_slice = self.slices[chosen_slice_idx].value
        third_slice = self.slices[third_slice_idx].value
        return [first_slice, middle_slice, third_slice]

    @staticmethod
    def _initialize_slices() -> list[Slice]:
        slices = []
        for i in range(4):
            for prize in [100, 1000, 5000, 10000]:
                slices.append(Slice(value=prize))
        for i in range(3):
            slices.append(Slice(value=15000))
        for i in range(2):
            slices.append(Slice(value=20000))
        slices.append(Slice(value=100000))
        slices.append(Slice(value=200000))
        slices.append(Slice(value='Buono abbraccio'))

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
            print('Cosa vuoi fare?')
            print('1) Girare la ruota')
            print('2) Comprare una vocale')
            print('3) Dare la soluzione')
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


class FinalMatch:
    def __init__(
        self, player: Player, wheel: WonderWheel, phrases: list[Phrase]
    ):
        self.player = player
        self.wheel = wheel
        self.phrases = phrases

    def play_match(self):
        # Turn the wheel and get 3 slices
        prizes = self.wheel.turn_wheel()

        # Play each of the three phrases
        remaining_seconds, first_match_won = self._play_first_match()

        input('Premi un tasto per passare al secondo match')
        os.system('cls')
        remaining_seconds, second_match_won = self._play_second_match(
            remaining_seconds
        )
        input('Premi un tasto per passare al terzo match')
        os.system('cls')
        third_match_won = self._play_third_match(remaining_seconds)

        # Choose among the available prizes
        self._choose_prize(
            won_matches=[first_match_won, second_match_won, third_match_won],
            prizes=prizes,
        )

    def _choose_prize(self, won_matches: list[bool], prizes: list[str | int]):
        pass

    def _play_first_match(self) -> tuple[int, bool]:
        phrase = self.phrases[0]
        # Add initial letters
        phrase.add_letter_to_current_guess_and_compute_score(
            letter='N', value=1
        )
        phrase.add_letter_to_current_guess_and_compute_score(
            letter='R', value=1
        )
        phrase.add_letter_to_current_guess_and_compute_score(
            letter='T', value=1
        )
        phrase.add_letter_to_current_guess_and_compute_score(
            letter='E', value=1
        )
        phrase.print()

        # Ask player to give three consonants and a vowel
        letters = input('Inserire 3 consonanti e 1 vocale: ')
        for letter in letters:
            phrase.add_letter_to_current_guess_and_compute_score(
                letter=letter, value=1
            )
        phrase.print()

        remaining_seconds, answer = start_match_with_time(remaining_seconds=60)
        match_won = self._give_match_result(answer=answer, phrase=phrase)
        return remaining_seconds, match_won

    def _play_second_match(self, remaining_seconds: int) -> tuple[int, bool]:
        phrase = self.phrases[1]
        phrase.reveal_start_and_end()
        phrase.print()

        remaining_seconds, answer = start_match_with_time(
            remaining_seconds=remaining_seconds
        )

        match_won = self._give_match_result(answer=answer, phrase=phrase)
        return remaining_seconds, match_won

    def _play_third_match(self, remaining_seconds: int) -> bool:
        phrase = self.phrases[-1]
        phrase.print()

        _, answer = start_third_match_with_time(
            remaining_seconds=remaining_seconds, phrase=phrase
        )

        match_won = self._give_match_result(answer=answer, phrase=phrase)

        return match_won

    @staticmethod
    def _give_match_result(answer: str, phrase: Phrase) -> bool:
        match_won = phrase.is_equal_to(answer)
        if match_won:
            print('Complimenti Hai indovinato!!!')
        else:
            print(
                f'❌❌❌ Hai perso. La frase corretta era: "{phrase.phrase_to_guess}"'
            )
        return match_won
