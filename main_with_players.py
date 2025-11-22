import os

from base_models import (
    Player,
    Match,
    Wheel,
    MatchResult,
    FinalMatch,
    WonderWheel,
)
from phrases import phrases, final_phrases


def change_player(current_player_idx: int, players: list):
    return (current_player_idx + 1) % len(players)


def choose_winner(players: list[Player]) -> Player:
    max_score = 0
    winner = None
    for player in players:
        if player.score > max_score:
            max_score = player.score
            winner = player
    return winner


def main():
    players: list[Player] = [
        Player(name='Jack'),
        Player(name='Angi'),
        Player(name='Nina'),
    ]

    # todo: remove
    players[0].score = 100
    phrases = []

    curr_player_idx = 0
    wheel = Wheel()
    for phrase in phrases:
        os.system('cls')
        for player in players:
            player.print_scores()
        input('Pronti per un nuovo round??')
        while True:
            curr_player = players[curr_player_idx]

            match = Match(player=curr_player, wheel=wheel, phrase=phrase)
            match_result = match.play_match()

            if match_result == MatchResult.WIN:
                input('Complimenti, hai indovinato!!!')
                # Increase the score of the winning player
                curr_player.win_match()

                # Reset temporary scores
                for player in players:
                    player.reset_temp_score()

                break

            else:
                curr_player_idx = change_player(
                    current_player_idx=curr_player_idx, players=players
                )

    winner = choose_winner(players=players)
    wonder_wheel = WonderWheel()
    match = FinalMatch(
        player=winner, wheel=wonder_wheel, phrases=final_phrases
    )
    match_result = match.play_match()


if __name__ == '__main__':
    main()
