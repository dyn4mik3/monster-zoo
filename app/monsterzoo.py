import random
import json
import uuid


class MonsterZooGame(object):
    def __init__(self, max_player_count=2):
        self.player_list = []
        self.max_player_count = max_player_count
        self.wild = Wild()
        self.current_player = None

    def add_player(self, player):
        if len(self.player_list) < self.max_player_count:
            self.player_list.append(player)
        else:
            print 'Already max players'

    def is_ready(self):
        if len(self.player_list) == self.max_player_count:
            return True
        else:
            return False

    def next_player(self):
        if self.current_player:
            # if the current player is the last one in the list, start from beginning
            if self.current_player == self.player_list[-1]:
                return self.player_list[0]
            else:
                player_index = self.player_list.index(self.current_player)
                return self.player_list[player_index+1]
        else:
            return self.player_list[0]

    def next_turn(self):
        """
        Setup for next turn. Clean up current player. Set next player.
        """
        self.current_player.clean_up()
        self.current_player = self.next_player()

    def setup_game(self):
        """
        Deal 5 cards to every player. Deal 5 cards in the Wild.
        Setup the active player.
        """
        if self.is_ready():
            for player in self.player_list:
                player.draw(5)
            self.wild.draw(5)
            self.current_player = self.next_player()
        else:
            print 'Not enough players to setup game'

    def __str__(self):
        # print statements will return json representation of variables
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


"""
General Classes
"""


class Card(object):
    def __init__(self, name="", description="", category="", family="", cost=0, food=0, image="/static/images/Oogly.png"):
        self.name = name
        self.description = description
        self.category = category
        self.family = family
        self.cost = cost
        self.food = food
        self.image = image

    def __str__(self):
        # print statements will return json representation of variables
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Deck(object):
    def __init__(self):
        self.cards = []
        self.discard = []

    def populate_deck(self, data):
        """
        Helper function to populate cards in deck. Takes in a list of cards.
        :param data: List of tuples (count, card function name)
        :return: deck object
        """
        for count, card in data:
            self.cards += [card() for x in range(count)]

    def add_card(self, card):
        """
        Adds a card to the deck.
        :param card: Card object
        :return: True if successful. False on NameError.
        """
        try:
            self.cards.append(card)
            return True
        except NameError:
            return False

    def draw(self, num=1):
        """
        Remove num of cards from deck. Return what was removed.
        :param num: Defaults to 1
        :return: Cards removed from top of deck.
        """
        return [self.cards.pop(0) for x in range(num)]

    def pop_card(self, card):
        """
        Removes and returns a specific card from the deck
        :param card: Card object that exists in the deck
        :return: Card object after removing the card from the deck
        """
        # get index for card, then pop it
        try:
            location = self.cards.index(card)
            return self.cards.pop(location)
        except ValueError:
            return False

    def shuffle(self):
        random.shuffle(self.cards)

    def is_empty(self):
        return len(self.cards) == 0

    def move_card(self, deck, card):
        deck.add_card(self.pop_card(card))

    def clean_up(self):
        """
        Move discard to bottom of deck. Clear out discard.
        """
        self.cards += self.discard
        self.discard = []

    def __str__(self):
        # print statements will return json representation of variables
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Hand(Deck):
    def __init__(self):
        self.cards = []


class Discard(Deck):
    def __init__(self):
        self.cards = []


class Zoo(Deck):
    def __init__(self):
        self.cards = []



"""
Card Data
"""


class OneOogly(Card):
    def __init__(self):
        self.name = "One Oogly"
        self.description = "1 Food"
        self.category = "Monster"
        self.family = "Oogly"
        self.cost = 2
        self.food = 1
        self.image = "/static/images/Oogly.png"

    def play(self, player):
        player.food += self.food
        print "Played One Oogly"


class TwoOogly(Card):
    def __init__(self):
        self.name = "Two Oogly"
        self.description = "2 Food"
        self.category = "Monster"
        self.family = "Oogly"
        self.cost = 3
        self.food = 2
        self.image = "/static/images/Oogly.png"

    def play(self, player):
        player.food += self.food
        print "Played Two Oogly"


"""
Deck Data
"""

WILD_DECK_CARDS = [
    (10, OneOogly),
    (20, TwoOogly)
]

STARTER_DECK_CARDS = [
    (10, OneOogly)
]


class StarterDeck(Deck):
    def __init__(self):
        self.cards = []
        self.discard = []
        self.populate_deck(STARTER_DECK_CARDS)


class WildDeck(Deck):
    def __init__(self):
        self.cards = []
        self.discard = []
        self.populate_deck(WILD_DECK_CARDS)

"""
Player Data
"""


class Player(object):
    def __init__(self, player_id=None):
        if player_id:
            self.player_id = player_id
        else:
            self.player_id = uuid.uuid4()
        self.deck = StarterDeck()
        self.zoo = Zoo()
        self.hand = Hand()
        self.discard = Discard()
        self.score = 0
        self.food = 0
        self.food_discount = 0

    def play_from_hand(self, card):
        if card in self.hand.cards:
            card.play(self)
        else:
            print "Card not in hand"

    def draw(self, num_of_cards=1):
        cards = self.deck.draw(num_of_cards)
        for card in cards:
            self.hand.cards.append(card)

    def discard(self, card):
        if card in self.hand.cards:
            self.hand.move_card(self.discard, card)
            print self.discard
        else:
            print 'Card not in hand'

    def clean_up(self):
        """
        Clean up steps for end of turn. Discard goes to bottom of deck. Food is zeroed out.
        :return:
        """
        self.food = 0
        self.deck.clean_up()


class Wild(Player):
    def __init__(self):
        self.deck = WildDeck()
        self.hand = Hand()
        self.discard = Discard()