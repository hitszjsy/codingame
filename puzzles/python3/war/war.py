import re
from collections import deque
from functools import total_ordering
from typing import Deque, Dict, Tuple


@total_ordering
class Card:
    MAPPING: Dict[str, int] = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14
    }

    def __init__(self, value: str, suit: str):
        self.value: str = value
        self.suit: str = suit

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.MAPPING[self.value] < self.MAPPING[other.value]

    def __repr__(self):
        return str(self.value) + self.suit


class Player:
    def __init__(self, player_number: int):
        self.player_number: int = player_number
        self.deck: Deque[Card] = deque()

    def has_empty_deck(self) -> bool:
        return len(self.deck) == 0


def read_player_input(player_number: int) -> Player:
    card_pattern: str = r"([\dJQKA]+)([DHCS])"
    player: Player = Player(player_number)
    nb_cards: int = int(input())
    for _ in range(nb_cards):
        line: str = input()
        value, suit = re.findall(card_pattern, line)[0]
        card: Card = Card(value, suit)
        player.deck.append(card)
    return player


def read_game_input() -> Tuple[Player, Player]:
    player1: Player = read_player_input(1)
    player2: Player = read_player_input(2)
    return player1, player2


def get_game_result(player1: Player, player2: Player, nb_rounds: int) -> str:
    if player1.has_empty_deck():
        return f"{player2.player_number} {nb_rounds}"
    elif player2.has_empty_deck():
        return f"{player1.player_number} {nb_rounds}"
    else:
        return "PAT"


def play_game(player1: Player, player2: Player) -> str:
    nb_rounds: int = 0
    deck_index: int = 0

    while True:
        if len(player1.deck) <= deck_index or len(player2.deck) <= deck_index:
            break
        player1_card: Card = player1.deck[deck_index]
        player2_card: Card = player2.deck[deck_index]
        n: int = deck_index + 1

        if player1_card > player2_card:
            player1.deck.rotate(-n)
            cards: Deque[Card] = deque()
            for _ in range(n):
                cards.append(player2.deck.popleft())
            player1.deck.extend(cards)
            nb_rounds += 1
            deck_index = 0
        elif player1_card < player2_card:
            cards: Deque[Card] = deque()
            for _ in range(n):
                cards.append(player1.deck.popleft())
            player2.deck.extend(cards)
            player2.deck.rotate(-n)
            nb_rounds += 1
            deck_index = 0
        else:
            deck_index += 4

    return get_game_result(player1, player2, nb_rounds)


if __name__ == "__main__":
    player1, player2 = read_game_input()
    game_result = play_game(player1, player2)
    print(game_result)
