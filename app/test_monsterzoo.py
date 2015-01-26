import unittest
from monsterzoo import *

class MonsterZooTestCase(unittest.TestCase):
    """Tests for 'monsterzoo.py'."""

    def test_player_creation(self):
        """Player is created with decks with cards"""
        player = Player()
        assert len(player.deck.cards) > 0

    def test_add_card(self):
        deck = Deck()
        card = OneOogly()
        deck.add_card(card)
        assert len(deck.cards) == 1

    def test_play_card_from_hand(self):
        player = Player()
        card = OneOogly()
        player.hand.add_card(card)
        player.play_from_hand(card)
        assert player.food > 0

    def test_player_hand_game_setup(self):
        game = MonsterZooGame(2)
        player = Player()
        player2 = Player()
        game.add_player(player)
        game.add_player(player2)
        game.setup_game()
        assert len(player.hand.cards) == 5

    def test_wild_hand_game_setup(self):
        game = MonsterZooGame(2)
        player = Player()
        player2 = Player()
        wild = game.wild
        game.add_player(player)
        game.add_player(player2)
        game.setup_game()
        assert len(wild.hand.cards) == 5

    def test_next_player_start(self):
        game = MonsterZooGame(2)
        player1 = Player()
        player2 = Player()
        game.add_player(player1)
        game.add_player(player2)
        game.setup_game()
        assert game.current_player == player1

    def test_next_player_start(self):
        game = MonsterZooGame(2)
        player1 = Player()
        player2 = Player()
        game.add_player(player1)
        game.add_player(player2)
        game.setup_game()
        assert game.next_player() == player2

    def test_next_turn(self):
        game = MonsterZooGame(2)
        player1 = Player()
        player2 = Player()
        game.add_player(player1)
        game.add_player(player2)
        game.setup_game()
        game.next_turn()
        assert game.current_player == player2

    def test_next_turn_twice(self):
        game = MonsterZooGame(2)
        player1 = Player()
        player2 = Player()
        game.add_player(player1)
        game.add_player(player2)
        game.setup_game()
        game.next_turn()
        game.next_turn()
        assert game.current_player == player1

    def test_player_discard_card(self):
        player1 = Player()
        player1.draw(5)
        print player1.hand

if __name__ == '__main__':
    unittest.main()