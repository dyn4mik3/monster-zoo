"""
Handles starting a game, registering players, making sure there are enough players to start a game.
"""
import json

class Game(object):
    """
    Tracks game states.
    States: Register game --> Players join --> Players ready --> Play game --> Game Over

    Game starts with one player - the creator. Then another player is invited to join the game.
    """

    def __init__(self, game_id, max_players=2):
        self.game_id = game_id
        self.state = GameState(self.game_id)
        self.players = []
        self.player_ids = []
        self.num_of_players = 0
        self.max_players = max_players
        self.max_score = 30
        self.top_player_score = 0
        print 'Game Created.'

    def add_player(self, player_id):
        """
        Add players to the game.
        :param player: Player object
        :return: Nothing
        """
        if self.ready():
            # Game is already ready to start. Cannot add any more players.
            return False
        if player_id not in self.player_ids:
            player = Player(player_id)
            self.players.append(player)
            print self.players
            self.player_ids.append(player_id)
            print 'Player %s added to Game %s. Players list = %s' % (player_id, self, self.players)
            self.update_player_count()
            return True
        else:
            print 'Player already in game'
            return False

    def update_game_state(self):
        self.state.players = self.players
        print self.state.players
        self.update_player_count()

    def update_player_count(self):
        """
        Update self.num_of_players with count of players
        :return: # of players
        """
        player_count = len(self.players)
        self.num_of_players = player_count
        print 'Player count is now %s' % player_count
        # seems redundant to store game state players and players in Game
        self.state.players = self.players[:]
        return player_count

    def ready(self):
        """
        Check to see if game has enough players to start.
        :return: True if full. False if not.
        """
        if self.num_of_players == self.max_players:
            return True
        elif self.num_of_players > self.max_players:
            raise ValueError('More players than MAX_PLAYERS!!!')
        else:
            return False

    def start(self):
        pass

    def play(self):
        while self.top_player_score < self.max_score:
            player = self.next_player()
            self.turn(player)
            self.update_game_state()

    def update_game_state(self):
        pass

    def next_player(self):
        pass

    def turn(self, player):
        pass

class GameState(object):
    """
    All the information required to render the game on the client.
    """
    def __init__(self, game_id):
        self.game_id = game_id
        self.players = []
        self.wild_deck = WildDeck()
        self.players_decks = []
        self.players_zoos = []
        self.players_scores = []
        self.players_food = []
        self.players_discards = []

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Player(object):
    def __init__(self, player_id):
        self.player_id = player_id
        self.ready = False
        self.food = 0
        self.food_discount = 0
        self.score = 0
        self.zoo = None
        self.deck = StarterDeck()
        self.discard = None
        self.hand = None
        print 'Player Created. Player = %s' % self.player_id

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Hand(object):
    pass

class Deck(object):
    def __init__(self):
        self.cards = []

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Card(object):
    def __init__(self, name="", description="", card_type="", card_family="", cost=0, food=0, image=""):
        self.name = name
        self.description = description
        self.card_type = card_type
        self.card_family = card_family
        self.cost = cost
        self.food = food

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

"""
DECK DATA
"""

class StarterDeck(Deck):
    def __init__(self):
        self.cards = [
            OneOogly(),
            TwoOogly()
        ]

class WildDeck(Deck):
    def __init__(self):
        self.cards = [
            OneOogly(),
            OneOogly(),
            OneOogly()
        ]

"""
CARD DATA
"""


class OneOogly(Card):
    def __init__(self):
        self.name = "One Oogly"
        self.description = "1 Food"
        self.card_type = "Monster"
        self.card_family = "Oogly"
        self.cost = 2
        self.food = 1
        self.image = "/static/images/Oogly.png"

    def play(self, player):
        self.discard(player)
        player.food += self.food
        print "Played One Oogly"

class TwoOogly(Card):
    def __init__(self):
        self.name = "Two Oogly"
        self.description = "2 Food"
        self.card_type = "Monster"
        self.card_family = "Oogly"
        self.cost = 3
        self.remodel = False
        self.remodel_card = None
        self.food = 2
        self.image = "/static/images/Oogly.png"

    def play(self, player):
        self.discard(player)
        player.food += self.food
        print "Played Two Oogly"
        self.socket.render_game()