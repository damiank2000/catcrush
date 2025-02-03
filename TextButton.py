import pygame

class TextButton:
    '''Simple text button'''

    def __init__(self, text, position, size, myfont):
        self.text = text
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)
        self.myfont = myfont

    def collidepoint(self, point):
        return self.rect.collidepoint(point)        

    def draw(self, screen):
        pygame.draw.rect(screen, (150, 150, 150), self.rect)
        textSurface = self.myfont.render(self.text, False, (250, 250, 250))
        screen.blit(textSurface, self.position)