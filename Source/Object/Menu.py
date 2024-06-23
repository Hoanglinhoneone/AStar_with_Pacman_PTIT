import os

import pygame
import sys

from constants import FPS, WIDTH, HEIGHT, BLUE, BLACK, WALL, FOOD, WHITE, YELLOW, MONSTER, IMAGE_GHOST, \
    IMAGE_PACMAN

clock = pygame.time.Clock()
bg = pygame.image.load("C:/Users/Acer/PycharmProjects/pythonProject/Pacman-AI-Ptiter/Source/images/home_bg.png")
# images/home_bg.png
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
pygame.init()
font = pygame.font.SysFont('Arial', 40)
my_font = pygame.font.SysFont('Comic Sans MS', 70)

SIZE_WALL = 20


class Button:
    def __init__(self, x, y, width, height, screen, buttonText="Button", onClickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onClickFunction = onClickFunction
        self.screen = screen

        self.fillColors = {
            'normal': '#8DEEEE',
            'hover': '#2F4F4F', 
            'pressed': '#97FFFF',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (255, 255, 255))

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.onClickFunction()

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        pygame.draw.rect(self.buttonSurface, BLUE, (0, 0, self.width, self.height), 5)
        self.screen.blit(self.buttonSurface, self.buttonRect)


class Menu:
    def __init__(self, screen):
        self.clicked = False
        self.map_name = []
        self.current_map = 0
        self.done = False
        self.current_screen = 1
        self.screen = screen
        self.btnStart = Button(WIDTH // 2 - 100 + 5, HEIGHT - 170, 200, 100, screen, "Start", self._load_map)
        self.btnPrev = Button(WIDTH // 2 - 250, HEIGHT // 4 * 3 + 35, 100, 100, screen, "<", self.prevMap)
        self.btnNext = Button(WIDTH // 2 + 150, HEIGHT // 4 * 3 + 35, 100, 100, screen, ">", self.nextMap)
        self.btnPlay = Button(WIDTH // 2 - 75, HEIGHT // 4 * 3 + 35, 150, 100, screen, "PLAY", self.selectMap)

    def nextMap(self):
        if self.clicked:
            self.current_screen = 3
            self.current_map = (self.current_map + 1) % len(self.map_name)
        self.clicked = False

    def prevMap(self):
        if self.clicked:
            self.current_screen = 3
            self.current_map -= 1
            if self.current_map < 0:
                self.current_map += len(self.map_name)
        self.clicked = False

    def _load_map(self):
        if self.clicked:
            for file in os.listdir('/Users/Acer/PycharmProjects/pythonProject/Pacman-AI-Ptiter/Input'):
                self.map_name.append('/Users/Acer/PycharmProjects/pythonProject/Pacman-AI-Ptiter/Input/' + file)
            self.current_screen = 3
        self.clicked = False

    def draw_map(self, fileName):
        text_surface = my_font.render(
            'MAP {map}'.format(map=self.current_map + 1), False, WHITE)
        self.screen.blit(text_surface, (WIDTH // 2 - 80, 0))

        f = open(fileName, "r")
        x = f.readline().split()
        count_ghost = 0
        N, M = int(x[0]), int(x[1])

        MARGIN_TOP = 100
        MARGIN_LEFT = (WIDTH - M * SIZE_WALL) // 2

        for i in range(N):
            line = f.readline().split()
            for j in range(M):
                cell = int(line[j])
                if cell == WALL:
                    image = pygame.Surface([SIZE_WALL, SIZE_WALL])
                    # image.fill(color)
                    pygame.draw.rect(image, BLUE, (0, 0, SIZE_WALL, SIZE_WALL), 1)
                    top = i * SIZE_WALL + MARGIN_TOP
                    left = j * SIZE_WALL + MARGIN_LEFT
                    self.screen.blit(image, (left, top))
                elif cell == FOOD:
                    image = pygame.Surface([SIZE_WALL // 2, SIZE_WALL // 2])
                    image.fill(WHITE)
                    image.set_colorkey(WHITE)
                    pygame.draw.ellipse(image, YELLOW, [0, 0, SIZE_WALL // 2, SIZE_WALL // 2])

                    top = i * SIZE_WALL + MARGIN_TOP + SIZE_WALL // 2 - SIZE_WALL // 4
                    left = j * SIZE_WALL + MARGIN_LEFT + SIZE_WALL // 2 - SIZE_WALL // 4
                    self.screen.blit(image, (left, top))
                elif cell == MONSTER:
                    image = pygame.image.load(IMAGE_GHOST[count_ghost]).convert_alpha()
                    image = pygame.transform.scale(image, (SIZE_WALL, SIZE_WALL))
                    top = i * SIZE_WALL + MARGIN_TOP
                    left = j * SIZE_WALL + MARGIN_LEFT
                    count_ghost = (count_ghost + 1) % len(IMAGE_GHOST)
                    self.screen.blit(image, (left, top))

        x = f.readline().split()
        image = pygame.image.load(IMAGE_PACMAN[0]).convert_alpha()
        image = pygame.transform.scale(image, (SIZE_WALL, SIZE_WALL))
        top = int(x[0]) * SIZE_WALL + MARGIN_TOP
        left = int(x[1]) * SIZE_WALL + MARGIN_LEFT
        self.screen.blit(image, (left, top))

        f.close()

    def selectMap(self):
        if self.clicked:
            self.done = True

    def run(self):
        while not self.done:
            self.clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

            if self.current_screen == 1:
                self.screen.blit(bg, (0, 0))
                self.btnStart.process()

            elif self.current_screen == 3:
                self.screen.fill(BLACK)
                self.current_screen = 4
                self.draw_map(self.map_name[self.current_map])

            elif self.current_screen == 4:
                self.btnNext.process()
                self.btnPrev.process()
                self.btnPlay.process()

            pygame.display.flip()
            clock.tick(FPS)

        return  self.map_name[self.current_map]
