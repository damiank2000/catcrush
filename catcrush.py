import pygame
import random
import os

_image_library = {}

COLOURNAMES = [
    'NONE',
    'RED',
    'GREEN',
    'BLUE',
    'YELLOW',
    'CYAN',
    'MAGENTA'
    ]

COLOURS = {
    'NONE':(0, 0, 0),
    'RED':(255, 0, 0),
    'GREEN':(0, 255, 0),
    'BLUE':(0, 0, 255),
    'YELLOW':(0, 255, 255),
    'CYAN':(255, 255, 0),
    'MAGENTA':(255, 0, 255)
    }

IMAGES = {
    'NONE':'',
    'RED':'cat1.jpg',
    'GREEN':'cat2.jpg',
    'BLUE':'cat3.jpg',
    'YELLOW':'cat4.jpg',
    'CYAN':'cat5.jpg',
    'MAGENTA':'cat6.jpg'
    }

def load_sound(sound_filename, directory):
    fullname = os.path.join(directory, sound_filename)
    sound = pygame.mixer.Sound(fullname)
    return sound

def meow():
    print("meow")

def random_colour():
    return random.choice(COLOURNAMES[1:7])

def attract_mode():
    for x in range(0, 5):
        for y in range(0, 12):
            pygame.draw.rect(screen, random_colour(), pygame.Rect(30+(y*60), 30+(x*60), 60, 60))

def get_image(path, scale):
    global _image_library
    scaled_image = _image_library.get(path)
    if scaled_image == None:
        full_path='/home/Ellie/' + path
        canonicalized_path = full_path.replace('/', os.sep)
        image = pygame.image.load(canonicalized_path)
        scaled_image = pygame.transform.scale(image, (scale[0], scale[1]))
        _image_library[path] = scaled_image
    return scaled_image

class Block:
    '''Represents a colour block'''

    isMatched = False
    isGone = False
    sizepercentage = 100
    
    def __init__(self, colour):
        self.colour = colour

    def match(self):
        self.isMatched = True

    def animate(self):
        if self.isMatched and self.colour != 'NONE' and self.sizepercentage > 0:
            self.sizepercentage = self.sizepercentage + 20
        if self.sizepercentage >= 200:
            self.isGone = True

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
                blockrow.append(Block(random_colour()))
            self.blocks.append(blockrow)

    def canMatch(self, row, column):
        return not self.blocks[row][column] is None \
               and self.blocks[row][column].isMatched == False

    def matchesColour(self, row, column, colour):
        return not self.blocks[row][column] is None \
               and self.blocks[row][column].colour == colour

    def getMatches(self):
        matches = []
        for rowIndex in range(0, self.rows):
            for columnIndex in range(1, self.columns - 1):
                if self.canMatch(rowIndex, columnIndex) \
                   and self.canMatch(rowIndex, columnIndex - 1) \
                   and self.canMatch(rowIndex, columnIndex + 1):
                    colour = self.blocks[rowIndex][columnIndex].colour
                    if self.matchesColour(rowIndex, columnIndex - 1, colour) \
                    and self.matchesColour(rowIndex, columnIndex + 1, colour):
                        matches.append(self.blocks[rowIndex][columnIndex])
                        matches.append(self.blocks[rowIndex][columnIndex-1])
                        matches.append(self.blocks[rowIndex][columnIndex+1])
            
        for rowIndex in range(1, self.rows - 1):
            for columnIndex in range(0, self.columns):
                if self.canMatch(rowIndex, columnIndex) \
                   and self.canMatch(rowIndex - 1, columnIndex) \
                   and self.canMatch(rowIndex + 1, columnIndex):
                    colour = self.blocks[rowIndex][columnIndex].colour
                    #print("("+str(rowIndex)+","+str(columnIndex)+") checking vertically for colour " + str(colour))
                    if self.matchesColour(rowIndex - 1, columnIndex, colour) \
                       and self.matchesColour(rowIndex + 1, columnIndex, colour):
                        matches.append(self.blocks[rowIndex][columnIndex])
                        matches.append(self.blocks[rowIndex-1][columnIndex])
                        matches.append(self.blocks[rowIndex+1][columnIndex])
        return matches

    
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
grid = Grid(6, 12)
meow = load_sound("cat.wav", '/home/Ellie/')
myfont = pygame.font.SysFont('AlphaFridgeMagnets', 30)

done = False
score = 0
allowMatch = True
selected = None
swap = None
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            position = pygame.mouse.get_pos()
            row = int((position[1] - 30) / 60)
            column = int((position[0] - 30) / 60)
            if not selected is None \
               and ((abs(row - selected[0]) == 1 and abs(column - selected[1]) == 0) \
                    or (abs(row - selected[0]) == 0 and abs(column - selected[1]) == 1)):
               swap = (row, column)
            else: 
                selected = (row, column)
                swap = None
            print(selected)

    pygame.display.flip()

    for rowIndex in range(0, grid.rows):
        for columnIndex in range(0, grid.columns):
            block = grid.blocks[rowIndex][columnIndex]
            x = 30+(columnIndex*60)
            y = 30+(rowIndex*60)
            pygame.draw.rect(screen, 0, pygame.Rect(x, y, 60, 60))
            if not block is None:
                block.animate()
                size = 56
                offset = 0
                offset = (60 - size) / 2
                colour=COLOURS[block.colour]
                pygame.draw.rect(screen, colour, pygame.Rect(x+offset, y+offset, size, size))
                image = IMAGES[block.colour]
                screen.blit(get_image(image, (54, 54)), (x+3, y+3))

                if selected == (rowIndex, columnIndex):
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x+offset, y+offset, size, size))
                elif swap == (rowIndex, columnIndex):
                    pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(x+offset, y+offset, size, size))

    # draw grumpy cat            
    screen.blit(get_image("grumpycat.jpg", (200, 160)), (300, 400))           
    textSurface = myfont.render('GIVE ME FUDZ', False, (250, 250, 250))
    screen.blit(textSurface, (100, 450))

    # draw score
    pygame.draw.rect(screen, 0, pygame.Rect(500, 450, 200, 200))
    textSurface = myfont.render('SCORE: ' + str(score), False, (250, 250, 250))
    screen.blit(textSurface, (500, 450))

    if allowMatch == True:
        matches = grid.getMatches()
        for match in matches:
            score += 30
            print("("+str(rowIndex)+","+str(columnIndex)+") matched")
            print("score is " + str(score))
            match.match()

    for rowIndex in range(0, grid.rows):
        for columnIndex in range(0, grid.columns):
            if not grid.blocks[rowIndex][columnIndex] is None \
                and grid.blocks[rowIndex][columnIndex].isGone == True:
                print("("+str(rowIndex)+","+str(columnIndex)+") removed")
                grid.blocks[rowIndex][columnIndex] = None

    for rowIndex in range(grid.rows - 2, -1, -1):
        for columnIndex in range(0, grid.columns):
            if grid.canMatch(rowIndex, columnIndex) \
                and grid.blocks[rowIndex+1][columnIndex] is None:
                    print("("+str(rowIndex)+","+str(columnIndex)+") falling")
                    grid.blocks[rowIndex+1][columnIndex] = grid.blocks[rowIndex][columnIndex]
                    grid.blocks[rowIndex][columnIndex] = None

    for columnIndex in range(0, grid.columns):
        if grid.blocks[0][columnIndex] is None:
            grid.blocks[0][columnIndex] = Block(random_colour())

    if selected is not None and swap is not None:
        sourceBlock = grid.blocks[selected[0]][selected[1]]
        swapBlock = grid.blocks[swap[0]][swap[1]]
        grid.blocks[selected[0]][selected[1]] = swapBlock
        grid.blocks[swap[0]][swap[1]] = sourceBlock
        print('Swapped ' + str(selected) + ' and ' + str(swap))

        if len(grid.getMatches()) == 0:
            sourceBlock = grid.blocks[selected[0]][selected[1]]
            swapBlock = grid.blocks[swap[0]][swap[1]]
            grid.blocks[selected[0]][selected[1]] = swapBlock
            grid.blocks[swap[0]][swap[1]] = sourceBlock
            print('Swapped back ' + str(selected) + ' and ' + str(swap))
        else:
            meow.play()
            
        selected = None
        swap = None
    clock.tick(60)
    
meow()


