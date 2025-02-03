import random
from data import GAME_OVER_PHRASES
from data import PHRASES 

class Game:
    '''Defines all game switches and values'''
    def __init__(self):
        # no init
        print('Init')

    def reset(self):
        self.done = False
        self.score = 0
        self.allowMatch = True
        self.selected = None
        self.swap = None
        self.phraseCounter = 0
        self.phrase = ''
        self.turns = 20
        self.gameOver = False
        self.matchCount = 0
        self.fishServed = False
        self.chickenServed = False
        self.isEatingChicken = False
        self.eatChickenTimer = 0

    def tick(self):
        self.phraseCounter += 1
        if self.phraseCounter == 500:
            if (self.gameOver):
                self.phrase = random.choice(GAME_OVER_PHRASES)
            else:
                self.phrase = random.choice(PHRASES)
                self.phraseCounter = 0
        if self.eatChickenTimer > 0:
            self.eatChickenTimer -= 1
        elif self.isEatingChicken == True:
            self.isEatingChicken = False
            self.setPhrase('')

    def isTimeToServeFish(self):
        return self.matchCount == 10 and not self.fishServed

    def isTimeToServeChicken(self):
        return self.matchCount == 15 and not self.chickenServed

    def serveFish(self):
        self.setPhrase('DO WANT FISH')
        self.fishServed = True
        
    def serveChicken(self):
        self.setPhrase('GIVE CHICKEN NOWS!!1')
        self.chickenServed = True
        
    def setPhrase(self, phrase):
        print(phrase)
        self.phrase = phrase
        self.phraseCounter = 0

    def eatChicken(self):
        self.isEatingChicken = True
        self.eatChickenTimer = 50
        self.setPhrase('NOM NOM NOM')