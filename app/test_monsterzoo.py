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

    def test_card_in_deck(self):
        player = Player()
        card = player.deck.cards[0]
        deck = player.deck
        assert deck.is_card_in_deck(card)

    def test_play_card_from_deck(self):
        player = Player()
        card = player.deck.cards[0]
        player.deck.play_card(player, card)
        assert player.food > 0

    def test_play_card(self):
        player = Player()
        card = OneOogly()
        player.hand.add_card(card)
        player.play_from_hand(card)
        assert player.food > 0

if __name__ == '__main__':
    unittest.main()