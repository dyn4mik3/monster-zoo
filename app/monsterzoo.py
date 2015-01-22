import random
import json

class MonsterZooGame(object):
    pass

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

    def add(self, card):
        self.cards.append(card)

    def draw(self, num=1):
        return [self.pop_first_card() for x in range(num)]

    def pop_first_card(self):
        return self.cards.pop(0)

    def shuffle(self):
        random.shuffle(self.cards)

    def is_empty(self):
        return len(self.cards) == 0

    def __str__(self):
        # print statements will return json representation of variables
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Hand(Deck):
    pass

class Discard(Deck):
    pass

class Zoo(Deck):
    pass

