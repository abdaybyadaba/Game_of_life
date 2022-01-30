import pygame
import sys
from settings import *
from copy import deepcopy
# 25 - (вертикаль) * 60 - (горизонталь) : размерность клеток

X = 520
Y = 424
SCENE_COLOR = (216, 217, 222)
CREATURES_COLOR = (240, 73, 3)
LINES_COLOR = (37, 55, 61)
TEXT_COLOR = (210, 215, 211)
BUTTONS_BORDER_COLOR = (40, 40, 48)
BUTTONS_COLOR = (0, 136, 145)


class GameField:
    def __init__(self, scene, field_entities, p2):
        self.scene = scene
        self.field_entities = field_entities
        self.p2 = p2

    def draw(self):
        for w in range(0, WIN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.scene, LINES_COLOR, [w, 0], [w, WIN_HEIGHT - 41], 1)
        for h in range(0, WIN_HEIGHT - 20, CELL_SIZE):
            pygame.draw.line(self.scene, LINES_COLOR, [0, h], [WIN_WIDTH, h], 1)

        next_entities = deepcopy(self.field_entities)
        for i in range(len(next_entities)):
            for j in range(len(next_entities[i])):
                if self.field_entities[i][j] == 1:
                    pygame.draw.rect(self.scene, CREATURES_COLOR, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if self.p2 == 1:
                    next_entities[i][j] = GameOfLifeUtils.rules(self.field_entities, i, j)
                elif self.p2 == 2:
                    next_entities[i][j] = 0
                else:
                    next_entities[i][j] = self.field_entities[i][j]
        if self.p2 == 2:
            self.p2 = 0
        self.field_entities = deepcopy(next_entities)

class GameOfLifeUtils:
    @staticmethod
    def rules(entities, y, x):
        neighbors = (
        [y - 1, x - 1], [y - 1, x], [y - 1, x + 1], [y, x - 1], [y, x + 1], [y + 1, x - 1], [y + 1, x], [y + 1, x + 1])
        neighbors_count = 0
        for i, j in neighbors:
            try:
                if entities[i][j] == 1:
                    neighbors_count += 1
            except:
                pass
        if entities[y][x] == 1 and (neighbors_count == 2 or neighbors_count == 3):
            return 1
        if entities[y][x] == 0 and neighbors_count == 3:
            return 1
        return 0


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("chto za DICH?")
        self.clock = pygame.time.Clock()

    def button(self, position, text):
        font = pygame.font.SysFont("Arial", 30)
        text_render = font.render(text, True, TEXT_COLOR)
        w, h = 72, 32
        x, y = position
        pygame.draw.line(self.screen, BUTTONS_BORDER_COLOR, (x, y), (x + w, y), 4)
        pygame.draw.line(self.screen, BUTTONS_BORDER_COLOR, (x, y - 2), (x, y + h), 4)
        pygame.draw.line(self.screen, BUTTONS_BORDER_COLOR, (x, y + h), (x + w, y + h), 4)
        pygame.draw.line(self.screen, BUTTONS_BORDER_COLOR, (x + w, y + h), [x + w, y], 4)
        pygame.draw.rect(self.screen, BUTTONS_COLOR, (x, y, w, h))
        return self.screen.blit(text_render, (x, y-2))

    def run(self):
        p1 = True
        entities = [[1 if not (i * j) % 22 else 0 for i in range(WIN_WIDTH // CELL_SIZE)] for j in range((WIN_HEIGHT - OFFSET) // CELL_SIZE)]
        field = GameField(self.screen, entities, p1)
        p = 1

        b1, b2, b3 = self.button((X - 230, Y), "Pause"), self.button((X - 120, Y), " Start"), self.button((X - 10, Y), "Clean")

        while p == 1:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x = (pygame.mouse.get_pos()[0] // CELL_SIZE)
                    y = (pygame.mouse.get_pos()[1] // CELL_SIZE)
                    try:
                        if field.field_entities[y][x] == 0:
                            field.field_entities[y][x] = 1
                        elif field.field_entities[y][x] == 1:
                            field.field_entities[y][x] = 0
                    except:
                        pass

                    if b1.collidepoint(pygame.mouse.get_pos()):
                        field.p2 = 0
                    elif b2.collidepoint(pygame.mouse.get_pos()):
                        field.p2 = 1
                    elif b3.collidepoint(pygame.mouse.get_pos()):
                        field.p2 = 2

            self.screen.fill(SCENE_COLOR)
            b1, b2, b3 = self.button((X - 230, Y), "Pause"), self.button((X - 120, Y), " Start"), self.button((X - 10, Y), "Clean")
            field.draw()
            pygame.display.flip()


print("game_of_life __name__:", __name__)

if __name__ == "__main__":
    app = App()
    app.run()


