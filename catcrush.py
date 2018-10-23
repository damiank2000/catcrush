import pygame
import random
import os

_image_library = {}

BLOCKTYPES = [
    'NONE',
    'RED',
    'GREEN',
    'BLUE',
    'YELLOW',
    'CYAN',
    'MAGENTA',
    'FISH',
    'CHICKEN'
    ]

COLOURS = {
    'NONE':(0, 0, 0),
    'RED':(255, 0, 0),
    'GREEN':(0, 255, 0),
    'BLUE':(0, 0, 255),
    'YELLOW':(0, 255, 255),
    'CYAN':(255, 255, 0),
    'MAGENTA':(255, 0, 255),
    'FISH':(100, 100, 100),
    'CHICKEN':(100, 100, 100)
    }

IMAGES = {
    'NONE':'',
    'RED':'cat1.jpg',
    'GREEN':'cat2.jpg',
    'BLUE':'cat3.jpg',
    'YELLOW':'cat4.jpg',
    'CYAN':'cat5.jpg',
    'MAGENTA':'cat6.jpg',
    'FISH':'fish.jpg',
    'CHICKEN':'chicken.jpg'
    }

PHRASES = [
    '',
    'GIVE ME FUDZ',
    'I WANT CANDY NOT',
    'BAD KITTY',
    'meow (food)'
    ]

GAME_OVER_PHRASES = [
    '',
    'GAME OVAZ',
    'YOU IS BAD AT THIS'
    ]

def load_sound(sound_filename, directory):
    fullname = os.path.join(directory, sound_filename)
    sound = pygame.mixer.Sound(fullname)
    return sound

def getRandomBlockType():
    return random.choice(BLOCKTYPES[1:7])

def attract_mode():
    for x in range(0, 5):
        for y in range(0, 12):
            pygame.draw.rect(screen, random_colour(), pygame.Rect(30+(y*60), 30+(x*60), 60, 60))

def getImage(path, scale):
    global _image_library
    scaled_image = _image_library.get(path)
    if scaled_image == None:
        full_path = rootFolder + path
        canonicalized_path = full_path.replace('/', os.sep)
        image = pygame.image.load(canonicalized_path)
        scaled_image = pygame.transform.scale(image, (scale[0], scale[1]))
        _image_library[path] = scaled_image
    return scaled_image

class Block:
    '''Represents a colour block'''

    isMatched = False
    isGone = False
    isFalling = False
    sizepercentage = 100
    fallCount = 0
    
    def __init__(self, blockType):
        self.blockType = blockType

    def match(self):
        self.isMatched = True

    def fall(self):
        self.isFalling = True
        self.fallCount = 100

    def animate(self):
        if self.isMatched and not self.isGone:
            self.sizepercentage = self.sizepercentage + 20
        if self.sizepercentage >= 200:
            self.isGone = True
        if self.isFalling:
            self.fallCount = self.fallCount - 20
            if self.fallCount <= 0:
                self.isFalling = False
                self.isFalling = 0

class TextButton:
    '''Simple text button'''

    def __init__(self, text, position, size):
        self.text = text
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)

    def collidepoint(self, point):
        return self.rect.collidepoint(point)        

    def draw(self, screen):
        pygame.draw.rect(screen, (150, 150, 150), self.rect)
        textSurface = myfont.render(self.text, False, (250, 250, 250))
        screen.blit(textSurface, self.position)

class GraphicalToggleButton:
    '''Simple graphical toggle button'''

    def __init__(self, imageOn, imageOff, position, size):
        self.imageOn = getImage(imageOn, size)
        self.imageOff = getImage(imageOff, size)
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)
        self.on = True

    def collidepoint(self, point):
        if self.rect.collidepoint(point):
            self.on = not self.on
            return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, (150, 150, 150), self.rect)
        if self.on == True:
            screen.blit(self.imageOn, self.position)
        else:
            screen.blit(self.imageOff, self.position)
        
class Grid:
    '''Represents a grid of colour blocks'''

    rows = 0
    columns = 0
    blocks = []

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        for x in range(0, rows):
            blockrow = []
            for y in range(0, columns):
                blockrow.append(Block(getRandomBlockType()))
            self.blocks.append(blockrow)

    def canMatch(self, row, column):
        return not self.blocks[row][column] is None \
               and self.blocks[row][column].isMatched == False \
               and self.blocks[row][column].isFalling == False

    def matchesBlockType(self, row, column, blockType):
        return not self.blocks[row][column] is None \
               and self.blocks[row][column].blockType == blockType

    def getMatches(self):
        matches = []
        for rowIndex in range(0, self.rows):
            for columnIndex in range(1, self.columns - 1):
                if self.canMatch(rowIndex, columnIndex) \
                   and self.canMatch(rowIndex, columnIndex - 1) \
                   and self.canMatch(rowIndex, columnIndex + 1):
                    blockType = self.blocks[rowIndex][columnIndex].blockType
                    if self.matchesBlockType(rowIndex, columnIndex - 1, blockType) \
                    and self.matchesBlockType(rowIndex, columnIndex + 1, blockType):
                        matches.append(self.blocks[rowIndex][columnIndex])
                        matches.append(self.blocks[rowIndex][columnIndex-1])
                        matches.append(self.blocks[rowIndex][columnIndex+1])
            
        for rowIndex in range(1, self.rows - 1):
            for columnIndex in range(0, self.columns):
                if self.canMatch(rowIndex, columnIndex) \
                   and self.canMatch(rowIndex - 1, columnIndex) \
                   and self.canMatch(rowIndex + 1, columnIndex):
                    blockType = self.blocks[rowIndex][columnIndex].blockType
                    #print("("+str(rowIndex)+","+str(columnIndex)+") checking vertically for colour " + str(colour))
                    if self.matchesBlockType(rowIndex - 1, columnIndex, blockType) \
                       and self.matchesBlockType(rowIndex + 1, columnIndex, blockType):
                        matches.append(self.blocks[rowIndex][columnIndex])
                        matches.append(self.blocks[rowIndex-1][columnIndex])
                        matches.append(self.blocks[rowIndex+1][columnIndex])
        return matches

    def anyMatches(self):
        return len(self.getMatches()) > 0

    def clear(self):
        for rowIndex in range(0, self.rows):
            for columnIndex in range(0, self.columns):
                self.blocks[rowIndex][columnIndex] = None

    def inBounds(self, position):
        return position[0] >= 0 \
               and position[0] < self.rows \
               and position[1] >= 0 \
               and position[1] < self.columns

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

    def tick(self):
        self.phraseCounter += 1
        if self.phraseCounter == 500:
            if (self.gameOver):
                self.phrase = random.choice(GAME_OVER_PHRASES)
            else:
                self.phrase = random.choice(PHRASES)
                self.phraseCounter = 0

    def isTimeToServeFish(self):
        return self.matchCount == 10 and not self.fishServed

    def isTimeToServeChicken(self):
        return self.matchCount == 15 and not self.chickenServed

    def serveFish(self):
        self.setPhrase('DO WANT FISH')
        self.fishServed = True
        
    def serveChicken(self):
        self.setPhrase('NOM NOM NOM')
        self.chickenServed = True
        
    def setPhrase(self, phrase):
        self.phrase = phrase
        self.phraseCounter = 0

def meow():
    if sound == True:
        meowSound.play()

# set up environment    
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
rootFolder = './'
meowSound = load_sound("cat.wav", rootFolder)
myfont = pygame.font.SysFont('AlphaFridgeMagnets', 30)
sound = True
restartButton = TextButton('RESTART', (550, 500), (110, 40))
soundToggleButton = GraphicalToggleButton('sound_on.png', 'sound_off.png', (700, 500), (40, 40))
game = Game()

# start new game
grid = Grid(6, 12)
game.reset()

# main game loop
while not game.done:

    # draw screen
    for rowIndex in range(0, grid.rows):
        for columnIndex in range(0, grid.columns):
            block = grid.blocks[rowIndex][columnIndex]
            x = 30+(columnIndex*60)
            y = 30+(rowIndex*60)
            pygame.draw.rect(screen, 0, pygame.Rect(x, y, 60, 60))
            if not block is None:
                block.animate()
                size = 56
                xoffset = (60 - size) / 2
                yoffset = ((60 - size) / 2) - (60 * block.fallCount / 100)
                colour=COLOURS[block.blockType]
                pygame.draw.rect(screen, colour, pygame.Rect(x+xoffset, y+yoffset, size, size))
                image = IMAGES[block.blockType]
                screen.blit(getImage(image, (54, 54)), (x+xoffset+1, y+yoffset+1))

                if game.selected == (rowIndex, columnIndex):
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x+xoffset, y+yoffset, size, size))
                elif game.swap == (rowIndex, columnIndex):
                    pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(x+xoffset, y+yoffset, size, size))


    game.tick()

    # draw grumpy cat
    pygame.draw.rect(screen, 0, pygame.Rect(100, 450, 200, 200))
    screen.blit(getImage("grumpycat.jpg", (200, 160)), (300, 400))
    textSurface = myfont.render(game.phrase, False, (250, 250, 250))
    screen.blit(textSurface, (100, 450))

    # draw score
    pygame.draw.rect(screen, 0, pygame.Rect(500, 400, 300, 200))
    textSurface = myfont.render('SCORE: ' + str(game.score), False, (250, 250, 250))
    screen.blit(textSurface, (550, 400))
    pygame.draw.rect(screen, 0, pygame.Rect(500, 450, 300, 200))
    textSurface = myfont.render('TURNS: ' + str(game.turns), False, (250, 250, 250))
    screen.blit(textSurface, (550, 450))

    # draw controls
    restartButton.draw(screen)
    soundToggleButton.draw(screen)

    # blank out top
    pygame.draw.rect(screen, 0, pygame.Rect(0, 0, 800, 30))

    # flip the display buffer
    pygame.display.flip()
        
    # respond to events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            position = pygame.mouse.get_pos()
            if restartButton.collidepoint(position):
                grid.clear()
                game.reset()
            elif soundToggleButton.collidepoint(position):
                sound = soundToggleButton.on
            elif not game.gameOver:
                row = int((position[1] - 30) / 60)
                column = int((position[0] - 30) / 60)
                if not game.selected is None \
                   and grid.inBounds((row, column)) \
                   and ((abs(row - game.selected[0]) == 1 and abs(column - game.selected[1]) == 0) \
                        or (abs(row - game.selected[0]) == 0 and abs(column - game.selected[1]) == 1)):
                   game.swap = (row, column)
                elif grid.inBounds((row, column)): 
                    game.selected = (row, column)
                    game.swap = None

    # apply gravity
    for rowIndex in range(grid.rows - 2, -1, -1):
        for columnIndex in range(0, grid.columns):
            if grid.canMatch(rowIndex, columnIndex) \
                and grid.blocks[rowIndex+1][columnIndex] is None:
                    grid.blocks[rowIndex][columnIndex].fall()
                    grid.blocks[rowIndex+1][columnIndex] = grid.blocks[rowIndex][columnIndex]
                    grid.blocks[rowIndex][columnIndex] = None

    # bring in new blocks from the top
    for columnIndex in range(0, grid.columns):
        if grid.blocks[0][columnIndex] is None:
            if game.isTimeToServeFish():
                grid.blocks[0][columnIndex] = Block('FISH')
                game.serveFish()
            elif game.isTimeToServeChicken():
                grid.blocks[0][columnIndex] = Block('CHICKEN')
                game.serveChicken()
            else:    
                grid.blocks[0][columnIndex] = Block(getRandomBlockType())
            grid.blocks[0][columnIndex].fall()

    # check for matches
    if game.allowMatch == True:
        matches = grid.getMatches()
        for match in matches:
            game.score += 30
            match.match()

    # remove blocks where removal animation has finished
    for rowIndex in range(0, grid.rows):
        for columnIndex in range(0, grid.columns):
            if not grid.blocks[rowIndex][columnIndex] is None \
                and grid.blocks[rowIndex][columnIndex].isGone == True:
                grid.blocks[rowIndex][columnIndex] = None

    # check number of turns
    if game.turns == 0:
        game.gameOver= True
        
    # perform the requested block swap if there is one
    if game.selected is not None and game.swap is not None:
        sourceBlock = grid.blocks[game.selected[0]][game.selected[1]]
        swapBlock = grid.blocks[game.swap[0]][game.swap[1]]
        if sourceBlock.blockType == 'FISH':
            sourceBlock.match()
            targetBlockType = swapBlock.blockType
            for rowIndex in range(0, grid.rows):
                for columnIndex in range(0, grid.columns):
                    if grid.canMatch(rowIndex, columnIndex):
                        if grid.blocks[rowIndex][columnIndex].blockType == targetBlockType:
                            grid.blocks[rowIndex][columnIndex].match()
            game.turns = game.turns - 1
            game.matchCount += 1
            meow()
        else:
            # try a swap
            grid.blocks[game.selected[0]][game.selected[1]] = swapBlock
            grid.blocks[game.swap[0]][game.swap[1]] = sourceBlock

            if not grid.anyMatches():
                # no match, swap back
                sourceBlock = grid.blocks[game.selected[0]][game.selected[1]]
                swapBlock = grid.blocks[game.swap[0]][game.swap[1]]
                grid.blocks[game.selected[0]][game.selected[1]] = swapBlock
                grid.blocks[game.swap[0]][game.swap[1]] = sourceBlock
            else:
                # match
                game.turns = game.turns - 1
                game.matchCount += 1
                meow()
            
        game.selected = None
        game.swap = None    
        
    clock.tick(60)
    



