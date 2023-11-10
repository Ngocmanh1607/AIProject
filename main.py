import pygame
import sys
from os import path
from map import list
from pygame import mixer
import math

pygame.init()
screen = pygame.display.set_mode((560, 560), 0, 0)
pygame.display.set_caption('Sokoban')
boxList = []
ballList = []
wallList = []
peopleDir = {'x': 0, 'y': 0}
clock = pygame.time.Clock()


def initData(level):
    """
    The function `initData` initializes the `wallList`, `ballList`, and `boxList` based on the given
    level data, and sets the position of the player character if there is one.

    :param level: The `level` parameter is the level number or identifier that determines which data to
    use for initializing the game
    """
    boxList.clear()
    ballList.clear()
    wallList.clear()
    data = list[level]
    index = -1
    for i in range(0, 16):
        for j in range(0, 16):
            index += 1
            item = data[index]
            if item == 1:
                wallList.append(1)
            else:
                wallList.append(0)

            if item == 2:
                ballList.append(2)
            else:
                ballList.append(0)

            if item == 3:
                boxList.append(3)
            else:
                boxList.append(0)

            if item == 4:
                peopleDir['x'] = j
                peopleDir['y'] = i


class GameApp:
    level = 0
    map = None
    background = None
    wall = None
    target = None
    box = None
    down_people = None
    left_people = None
    right_people = None
    up_people = None
    direction = 'down'
    ballNum = 0

    def __init__(self):
        self.loadFile()
        self.runGame()

    def loadFile(self):

        self.background = pygame.image.load(self.resolve('images/floor.jpeg'))
        # Scale the background image
        self.background = pygame.transform.scale(
            self.background, (560, 560))
        self.wall = pygame.image.load(self.resolve('images/wall.png'))
        self.wall = pygame.transform.scale(self.wall, (35, 35))

        self.target = pygame.image.load(self.resolve('images/target.png'))
        # scale
        self.target = pygame.transform.scale(self.target, (30, 30))
        self.box = pygame.image.load(self.resolve('images/box1.png'))
        # scale box
        self.box = pygame.transform.scale(self.box, (30, 30))

        self.down_people = pygame.image.load(self.resolve('images/robot.png'))
        # scale
        self.down_people = pygame.transform.scale(self.down_people, (50, 62))

        self.left_people = pygame.image.load(self.resolve('images/robot.png'))
        # scale
        self.left_people = pygame.transform.scale(self.left_people, (50, 62))
        self.right_people = pygame.image.load(self.resolve('images/robot.png'))
        # scale
        self.right_people = pygame.transform.scale(self.right_people, (50, 62))
        self.up_people = pygame.image.load(self.resolve('images/robot.png'))
        # scale
        self.up_people = pygame.transform.scale(self.up_people, (50, 62))

    def resolve(self, filename):
        dirName = path.dirname(__file__)
        return dirName + '/' + filename

    def renderLevel(self):
        levelText = pygame.font.SysFont("arial", 20).render(
            str(self.level + 1), True, (0, 0, 0))
        screen.blit(levelText, (490, 5))

    def renderPeople(self, i, j):
        if self.direction == 'down':
            screen.blit(self.down_people, (j*35-7, i*35-27))
        if self.direction == 'left':
            screen.blit(self.left_people, (j*35-7, i*35-27))
        if self.direction == 'right':
            screen.blit(self.right_people, (j*35-7, i*35-27))
        if self.direction == 'up':
            screen.blit(self.up_people, (j*35-7, i*35-27))

    def renderData(self):
        index = -1
        for i in range(0, 16):
            for j in range(0, 16):
                index += 1
                if wallList[index] == 1:
                    screen.blit(self.wall, (j*35, i*35 - 13))
                if ballList[index] == 2:
                    self.ballNum += 1
                    screen.blit(self.target, (j*35+2, i*35-10))
                if boxList[index] == 3:
                    screen.blit(self.box, (j*35+2, i*35 - 11))
                if peopleDir['x'] == j and peopleDir['y'] == i:
                    self.renderPeople(i, j)

    def hasGo(self, preItem, nextItem, preIndex, nextIndex, x, y):
        """
        The function checks if the player can move to a certain position based on the current and next
        items on the game board.

        :param preItem: preItem is the item (or object) that is currently present at the previous index
        in the game grid
        :param nextItem: The `nextItem` parameter represents the item at the next index in a list or
        array
        :param preIndex: The preIndex parameter represents the index of the previous item in a list or
        array
        :param nextIndex: The `nextIndex` parameter represents the index of the next item in a list or
        array
        :param x: The x parameter represents the x-coordinate of the current position of the player
        :param y: The parameter 'y' represents the current y-coordinate of the player's position on the
        game board
        :return: a boolean value.
        """
        if preItem == 0 or preItem == 2:
            peopleDir['x'] = x
            peopleDir['y'] = y
            return True
        if preItem == 3:
            if nextItem == 0 or nextItem == 2:
                boxList[preIndex] = 0
                boxList[nextIndex] = 3
                peopleDir['x'] = x
                peopleDir['y'] = y
                self.checkGameover(nextIndex)
                self.checkWin()
                return True
        return False

    def checkGameover(self, nextIndex):
        y = math.floor(nextIndex/16)
        x = nextIndex % 16
        preItem = 0
        if ballList[nextIndex] != 2:
            checkList = [
                wallList[(y-1)*16 + x],
                wallList[y*16 + x-1],
                wallList[(y+1)*16 + x],
                wallList[y*16 + x+1],
                wallList[(y-1)*16 + x]
            ]
            for item in checkList:
                if item == 0:
                    preItem = 0
                elif item == 1 and preItem == 0:
                    preItem = 1
                elif item == 1 and preItem == 1:
                    self.level = 0
                    initData(self.level)
                    break

    def checkWin(self):
        index = -1
        winNum = 0
        self.ballNum = 0
        for i in range(0, 16):
            for j in range(0, 16):
                index += 1
                if ballList[index] == 2:
                    self.ballNum += 1
                    if (boxList[index] == 3):
                        winNum += 1
        if self.ballNum == winNum:
            self.level += 1
            initData(self.level)

    def pushData(self, type):
        """
        The function `pushData` determines the direction in which an object can be pushed based on the
        surrounding items in a grid.

        :param type: The `type` parameter in the `pushData` function represents the direction in which
        the data is being pushed. It can have one of the following values: 'left', 'right', 'up', or
        'down'
        """
        x = peopleDir['x']
        y = peopleDir['y']
        curIndex = y*16+x
        if type == 'left':
            preIndex = y*16+x-1
            nextIndex = y*16+x-2
            preItem = max(
                [boxList[preIndex], ballList[preIndex], wallList[preIndex]])
            nextItem = max(
                [boxList[nextIndex], ballList[nextIndex], wallList[nextIndex]])
            if self.hasGo(preItem, nextItem, preIndex, nextIndex, x-1, y):
                self.direction = 'left'
        if type == 'right':
            preIndex = y*16+x+1
            nextIndex = y*16+x+2
            preItem = max(
                [boxList[preIndex], ballList[preIndex], wallList[preIndex]])
            nextItem = max(
                [boxList[nextIndex], ballList[nextIndex], wallList[nextIndex]])
            if self.hasGo(preItem, nextItem, preIndex, nextIndex, x+1, y):
                self.direction = 'right'
        if type == 'up':
            preIndex = (y-1)*16+x
            nextIndex = (y-2)*16+x
            preItem = max(
                [boxList[preIndex], ballList[preIndex], wallList[preIndex]])
            nextItem = max(
                [boxList[nextIndex], ballList[nextIndex], wallList[nextIndex]])
            if self.hasGo(preItem, nextItem, preIndex, nextIndex, x, y-1):
                self.direction = 'up'
        if type == 'down':
            preIndex = (y+1)*16+x
            nextIndex = (y+2)*16+x
            preItem = max(
                [boxList[preIndex], ballList[preIndex], wallList[preIndex]])
            nextItem = max(
                [boxList[nextIndex], ballList[nextIndex], wallList[nextIndex]])
            if self.hasGo(preItem, nextItem, preIndex, nextIndex, x, y+1):
                self.direction = 'down'

    def runGame(self):
        while True:
            clock.tick(300)
            screen.fill((0, 0, 0))
            screen.blit(self.background, (0, 0))
            self.renderData()
            self.renderLevel()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.pushData('left')
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.pushData('right')
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.pushData('down')
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.pushData('up')
            pygame.display.update()


if __name__ == '__main__':
    initData(0)
    GameApp()
