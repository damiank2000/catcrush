
import pygame

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
