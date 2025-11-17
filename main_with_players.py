import os

from base_models import Player, Match, Wheel, MatchResult
from phrases import phrases


def change_player(current_player_idx: int, players: list):
    return (current_player_idx + 1) % len(players)


def main():
    players: list[Player] = [
        Player(name='Jack'), Player(name='Angi'), Player(name='Nina')
    ]

    curr_player_idx = 0
    wheel = Wheel()
    for phrase in phrases:
        os.system('cls')
        for player in players:
            player.print_scores()
        input('Pronti per un nuovo round??')
        while True:
            curr_player = players[curr_player_idx]

            match = Match(
                player=curr_player, wheel=wheel, phrase=phrase
            )
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


if __name__ == '__main__':
    main()

