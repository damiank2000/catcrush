class Block:
    '''Represents a colour block'''

    isMatched = False
    isGone = False
    isFalling = False
    animationFrame = 1
    fallCount = 0
    
    def __init__(self, blockType):
        self.blockType = blockType

    def match(self):
        self.isMatched = True

    def fall(self):
        self.isFalling = True
        self.fallCount = 100

    def isMatchable(self):
        return not self.isMatched and not self.isFalling
    
    def matches(self, block):
        return block \
               and block.isMatchable() \
               and block.blockType == self.blockType

    def animate(self):
        if self.isMatched and not self.isGone:
            self.animationFrame = self.animationFrame + 1
        if self.animationFrame >= 5:
            self.isGone = True
        if self.isFalling:
            self.fallCount = self.fallCount - 20
            if self.fallCount <= 0:
                self.isFalling = False
                self.isFalling = 0
                