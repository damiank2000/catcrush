import pygame

class GraphicalToggleButton:
    '''Simple graphical toggle button'''

    def __init__(self, imageOn, imageOff, position, size):
        self.imageOn = imageOn
        self.imageOff = imageOff
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
