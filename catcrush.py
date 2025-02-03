import pygame
import os
from Block import Block
from TextButton import TextButton
from GraphicalToggleButton import GraphicalToggleButton
from Grid import Grid
from Game import Game
from data import COLOURS
from data import IMAGES

_image_library = {}

def load_sound(sound_filename, directory):
    fullname = os.path.join(directory, sound_filename)
    sound = pygame.mixer.Sound(fullname)
    return sound

def attract_mode():
    for x in range(0, 5):
        for y in range(0, 12):
            pygame.draw.rect(screen, random_colour(), pygame.Rect(30+(y*60), 30+(x*60), 60, 60))

def getImage(path, scale):
    global _image_library
    scaled_image = _image_library.get(path)
    if scaled_image == None:
        full_path = rootFolder + 'images/' + path
        canonicalized_path = full_path.replace('/', os.sep)
        image = pygame.image.load(canonicalized_path)
        scaled_image = pygame.transform.scale(image, (scale[0], scale[1]))
        _image_library[path] = scaled_image
    return scaled_image

def meow():
    if sound == True:
        meowSound.play()

# set up environment    
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
rootFolder = './'
meowSound = load_sound("sounds/cat.wav", rootFolder)
myfont = pygame.font.SysFont('AlphaFridgeMagnets', 30)
sound = True
restartButton = TextButton('RESTART', (550, 500), (110, 40), myfont)
soundToggleButton = GraphicalToggleButton(getImage('sound_on.png', (40, 40)), getImage('sound_off.png', (40, 40)), (700, 500), (40, 40))
game = Game()

# start new game
grid = Grid(6, 12)
game.reset()

# main game loop
while not game.done:

    # draw screen
    screen.fill(0)
    for rowIndex in range(0, grid.rows):
        for columnIndex in range(0, grid.columns):
            block = grid.getBlock((rowIndex, columnIndex))
            x = 30+(columnIndex*60)
            y = 30+(rowIndex*60)
            pygame.draw.rect(screen, 0, pygame.Rect(x, y, 60, 60))
            if not block is None:
                block.animate()
                blockSize = 60 - ((block.animationFrame - 1) * 10)
                frameSize = blockSize - 4
                imageSize = blockSize - 6
                xoffset = (blockSize - frameSize) / 2
                yoffset = ((blockSize - frameSize) / 2) - (60 * block.fallCount / 100)
                colour=COLOURS[block.blockType]
                pygame.draw.rect(screen, colour, pygame.Rect(x+xoffset, y+yoffset, frameSize, frameSize))
                image = IMAGES[block.blockType]
                screen.blit(getImage(image, (imageSize, imageSize)), (x+xoffset+1, y+yoffset+1))

                if game.selected == (rowIndex, columnIndex):
                    pygame.draw.rect(screen, (255, 255, 255, 100), pygame.Rect(x+xoffset, y+yoffset, frameSize, frameSize))
                elif game.swap == (rowIndex, columnIndex):
                    pygame.draw.rect(screen, (200, 200, 200, 100), pygame.Rect(x+xoffset, y+yoffset, frameSize, frameSize))

    game.tick()

    # draw grumpy cat
    if game.isEatingChicken == True:
        grumpyCatPosition = (300, 200)
        speechPosition = (100, 250)
    else:
        grumpyCatPosition = (300, 400)
        speechPosition = (100, 450)
    screen.blit(getImage("grumpycat.jpg", (200, 160)), grumpyCatPosition)
    if len(game.phrase) > 0:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(speechPosition, (18*len(game.phrase), 40)))
        textSurface = myfont.render(game.phrase, False, (0, 0, 0))
        screen.blit(textSurface, speechPosition)

        
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
            if grid.isMatchable(rowIndex, columnIndex) and grid.getBlock((rowIndex+1, columnIndex)) is None:
                grid.getBlock((rowIndex, columnIndex)).fall()
                grid.moveBlock((rowIndex, columnIndex), (rowIndex+1, columnIndex))

    # bring in new blocks from the top
    for columnIndex in range(0, grid.columns):
        if grid.getBlock((0, columnIndex)) is None:
            if game.isTimeToServeFish():
                newBlock = Block('FISH')
                game.serveFish()
            elif game.isTimeToServeChicken():
                newBlock = Block('CHICKEN')
                game.serveChicken()
            else:    
                newBlock = Block(grid.getRandomBlockType())
            grid.setBlock((0, columnIndex), newBlock)
            newBlock.fall()

    # check for matches
    if game.allowMatch == True:
        matches = grid.getMatches()
        for match in matches:
            game.score += 30

    # remove blocks where removal animation has finished
    for rowIndex in range(0, grid.rows):
        for columnIndex in range(0, grid.columns):
            block = grid.getBlock((rowIndex, columnIndex))
            if not block is None and block.isGone == True:
                grid.removeBlock((rowIndex, columnIndex))

    # check number of turns
    if game.turns == 0:
        game.gameOver= True
        
    # perform the requested block swap if there is one
    if game.selected is not None:
        sourceBlock = grid.getBlock(game.selected)
        if sourceBlock.blockType == 'CHICKEN':
            for rowIndex in range(max(game.selected[0]-1, 0), game.selected[0]+2):
                for columnIndex in range(max(game.selected[1]-1, 0), game.selected[1]+2):
                    grid.blocks[rowIndex][columnIndex].match()
            game.turns = game.turns - 1
            game.matchCount += 1
            game.selected = None
            game.swap = None
            game.eatChicken()
            meow()
        elif game.swap is not None:
            swapBlock = grid.getBlock(game.swap)
            if sourceBlock.blockType == 'FISH':
                sourceBlock.match()
                targetBlockType = swapBlock.blockType
                for rowIndex in range(0, grid.rows):
                    for columnIndex in range(0, grid.columns):
                        if grid.isMatchable(rowIndex, columnIndex):
                            if grid.getBlock((rowIndex, columnIndex)).blockType == targetBlockType:
                                grid.getBlock((rowIndex, columnIndex)).match()
                game.turns = game.turns - 1
                game.matchCount += 1
                meow()
            else:
                # try a swap
                grid.swapBlocks(game.selected, game.swap)
                if not grid.anyMatches():
                    # no match, swap back
                    grid.swapBlocks(game.selected, game.swap)
                else:
                    # match
                    game.turns = game.turns - 1
                    game.matchCount += 1
                    meow()
                
            game.selected = None
            game.swap = None    
        
    clock.tick(60)
    



