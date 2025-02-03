import random
from Block import Block
from data import BLOCKTYPES

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
                blockrow.append(Block(self.getRandomBlockType()))
            self.blocks.append(blockrow)

    def getRandomBlockType(self):
        return random.choice(BLOCKTYPES[1:7])
    
    def isMatchable(self, row, column):
        return not self.blocks[row][column] is None \
               and self.blocks[row][column].isMatchable

    def getBlock(self, position):
        return self.blocks[position[0]][position[1]]

    def setBlock(self, position, block):
        self.blocks[position[0]][position[1]] = block

    def moveBlock(self, sourcePosition, targetPosition):
        block = self.getBlock(sourcePosition)
        self.setBlock(targetPosition, block)
        self.setBlock(sourcePosition, None)

    def swapBlocks(self, sourcePosition, swapPosition):
        sourceBlock = self.getBlock(sourcePosition)
        swapBlock = self.getBlock(swapPosition)
        self.setBlock(sourcePosition, swapBlock)
        self.setBlock(swapPosition, sourceBlock)

    def removeBlock(self, position):
        self.setBlock(position, None)

    def matchesBlockType(self, row, column, blockType):
        return not self.blocks[row][column] is None \
               and self.blocks[row][column].blockType == blockType

    def isMatchingBlock(self, row, column, block):
        blockAtLocation = self.blocks[row][column]
        return blockAtLocation \
               and blockAtLocation.isMatchable() \
               and blockAtLocation.blockType == block.blockType

    def getBlocks(self, coordinateArray):
        blocks = []
        for coordinate in coordinateArray:
            if (coordinate[0] >= 0 and coordinate[0] < self.rows) \
                and (coordinate[1] >= 0 \
                     and coordinate[1] < self.columns):
                blocks.append(self.blocks[coordinate[0]][coordinate[1]])
            else:
                return None;
        return blocks
    
    def threeHorizontalMatchPattern(self, rowIndex, columnIndex):
        return self.getBlocks([[rowIndex, columnIndex+1], [rowIndex, columnIndex+2]])

    def fourHorizontalMatchPattern(self, rowIndex, columnIndex):
        return self.getBlocks([[rowIndex, columnIndex+1], [rowIndex, columnIndex+2], [rowIndex, columnIndex+3]])

    def fiveHorizontalMatchPattern(self, rowIndex, columnIndex):
        return self.getBlocks([[rowIndex, columnIndex+1],
                               [rowIndex, columnIndex+2],
                               [rowIndex, columnIndex+3],
                               [rowIndex, columnIndex+4]
                               ])

    def threeVerticalMatchPattern(self, rowIndex, columnIndex):
        return self.getBlocks([[rowIndex+1, columnIndex], [rowIndex+2, columnIndex]])

    def fourVerticalMatchPattern(self, rowIndex, columnIndex):
        return self.getBlocks([[rowIndex+1, columnIndex], [rowIndex+2, columnIndex], [rowIndex+3, columnIndex]])

    def fiveVerticalMatchPattern(self, rowIndex, columnIndex):
        return self.getBlocks([[rowIndex+1, columnIndex],
                               [rowIndex+2, columnIndex],
                               [rowIndex+3, columnIndex],
                               [rowIndex+4, columnIndex]
                               ])

    def fourSquareMatchPattern(self, rowIndex, columnIndex):
        return self.getBlocks([[rowIndex, columnIndex+1], [rowIndex+1, columnIndex+1], [rowIndex+1, columnIndex]])

    def getMatches(self):
        matches = []
        self.findMatches(matches, self.fiveHorizontalMatchPattern)
        self.findMatches(matches, self.fiveVerticalMatchPattern)    
        self.findMatches(matches, self.fourSquareMatchPattern)
        self.findMatches(matches, self.fourHorizontalMatchPattern)
        self.findMatches(matches, self.fourVerticalMatchPattern)    
        self.findMatches(matches, self.threeHorizontalMatchPattern)
        self.findMatches(matches, self.threeVerticalMatchPattern)    
        return matches

    def findMatches(self, matches, matchStrategy):
        for rowIndex in range(0, self.rows):
            for columnIndex in range(0, self.columns):
                block = self.blocks[rowIndex][columnIndex]
                blocksToCompare = matchStrategy(rowIndex, columnIndex)
                if block \
                        and block.isMatchable() \
                        and blocksToCompare \
                        and all(block.matches(otherBlock) for otherBlock in blocksToCompare):
                    [x.match() for x in [*blocksToCompare, block]]
                    matches.extend([*blocksToCompare, block])

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
