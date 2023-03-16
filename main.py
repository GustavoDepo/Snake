from game_omjects import *
from pygame.locals import *
from database import *
import sys
import pygame as pg
import pygame_textinput

class Game:
    def __init__(self):
        pg.init()
        self.WINDOW_SIZE = 640
        self.nickName = ''
        self.TILE_SIZE = 40
        self.textinput = pygame_textinput.TextInputVisualizer()
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.x1 = 120
        self.y1 = 200
        self.x2 = self.x1 + 400
        self.y2 = self.y1 + 240

    def drawGrid(self):
        [pg.draw.line(self.screen, 'white', (x, 0), (x, self.WINDOW_SIZE)) for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        [pg.draw.line(self.screen, 'white', (0, y), (self.WINDOW_SIZE, y)) for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]

    def new_game(self):
        self.now = True
        self.database = dataBase()
        self.snake = Snake(self)
        self.food = Food(self)
        
    def update(self):
        if not self.snake.update():
            return False
        self.clock.tick(30)
        pg.display.flip()
        return True

    def draw(self):
        self.screen.fill('black')
        self.drawGrid()
        self.food.draw()
        self.snake.draw()
        self.drawScore(self.snake.length)

    def startScreen(self):

        while True:
            self.screen.fill('white')
            self.drawSomeTHink('Привет, Друг! Как тебя зовут? ', 25,
                               self.WINDOW_SIZE / 2, self.WINDOW_SIZE / 2, 'black')

            self.events = pg.event.get()

            self.textinput.update(self.events)
            self.screen.blit(self.textinput.surface,
                             (self.WINDOW_SIZE / 2 - len(self.textinput.manager.value) * 6, self.WINDOW_SIZE / 2 + 20))

            self.drawPrintYourName('Впиши свое имя с помощью клавиатуры.')

            for event in self.events:
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == K_RETURN:
                        self.nickName = self.textinput
                        return
                    if event.key == K_ESCAPE:
                        exit()

            pg.display.update()
            self.clock.tick(30)

    def gameOwerScreen(self, db):
        while True:
            self.screen.fill('white')
            self.drawSomeTHink('TOP-5 Лучших игроков', 20, self.WINDOW_SIZE / 2, self.y1 - 30, 'black')
            self.drawScorsTable()

            if self.snake.length == 20:
                self.drawSomeTHink('Ты выйграл!!!', 35, self.WINDOW_SIZE / 2, self.y1 - 70, 'green')
            else:
                self.drawSomeTHink('Ты проиграл((( Попробуй снова!!!', 35, self.WINDOW_SIZE / 2, self.y1 - 70, 'red')

            self.draw_table('№', 'Nickname', 'Score', 1)
            for i in range(len(db)):
                self.draw_table(i + 1, db[i][0], db[i][1], i + 2)


            self.events = pg.event.get()
            for event in self.events:
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
                    else:
                        self.run()

            pg.display.update()
            self.clock.tick(30)

    def draw_table(self, number, nickname, score, pos):
        self.titleFont = pg.font.Font('freesansbold.ttf', 15)
        self.titleSurf1 = self.titleFont.render(str(number), True, 'black')
        self.titleSurf2 = self.titleFont.render(nickname, True, 'black')
        self.titleSurf3 = self.titleFont.render(str(score), True, 'black')

        self.rotatedRect1 = self.titleSurf1.get_rect()
        self.rotatedRect1.center = (self.x1 + self.TILE_SIZE / 2, self.y1 + self.TILE_SIZE * (pos - 1) + self.TILE_SIZE / 2)

        self.rotatedRect2 = self.titleSurf2.get_rect()
        self.rotatedRect2.center = (self.x1 + self.TILE_SIZE * 6 / 2 + self.TILE_SIZE, self.y1 + self.TILE_SIZE * (pos - 1) + self.TILE_SIZE / 2)

        self.rotatedRect3 = self.titleSurf3.get_rect()
        self.rotatedRect3.center = (self.x1 + self.TILE_SIZE * 7 + self.TILE_SIZE * 3 / 2, self.y1 + self.TILE_SIZE * (pos - 1) + self.TILE_SIZE / 2)

        self.screen.blit(self.titleSurf1, self.rotatedRect1)
        self.screen.blit(self.titleSurf2, self.rotatedRect2)
        self.screen.blit(self.titleSurf3, self.rotatedRect3)

    def drawPrintYourName(self, text):
        self.basicfont = pg.font.Font('freesansbold.ttf', 18)
        self.pressKeySurf = self.basicfont.render(text, True, 'black')
        self.pressKeyRect = self.pressKeySurf.get_rect()
        self.pressKeyRect.center = (self.WINDOW_SIZE - len(text) * 6, self.WINDOW_SIZE - 30)
        self.screen.blit(self.pressKeySurf, self.pressKeyRect)

    def drawScore(self, score):
        self.scoreSurf = self.basicfont.render(f"Score:  {score}", True, 'white')
        self.scoreRect = self.scoreSurf.get_rect()
        self.scoreRect.topleft = (self.WINDOW_SIZE - 120, 10)
        self.screen.blit(self.scoreSurf, self.scoreRect)

    def drawScorsTable(self):
        pg.draw.rect(self.screen, 'black',
                     (self.x1, self.y1, self.x2 - self.x1 + 3, self.y2 - self.y1 + 3), 3)
        [pg.draw.line(self.screen, 'black', (self.x1, y), (self.x2, y)) for y in
         range(self.y1, self.y2, self.TILE_SIZE)]
        # вертекальные линии таблицы
        pg.draw.line(self.screen, 'black', (self.TILE_SIZE * 1 + self.x1, self.y1),
                     (self.TILE_SIZE * 1 + self.x1, self.y2))
        # 1 столбец
        pg.draw.line(self.screen, 'black', (self.TILE_SIZE * 7 + self.x1, self.y1),
                     (self.TILE_SIZE * 7 + self.x1, self.y2))
        # 2 столбец

    def drawSomeTHink(self, text, sizeFont, x, y, color):
        self.titleFont = pg.font.Font('freesansbold.ttf', sizeFont)
        self.titleSurf = self.titleFont.render(text, True, color)
        self.rotatedRect = self.titleSurf.get_rect()
        self.rotatedRect.center = (x, y)
        self.screen.blit(self.titleSurf, self.rotatedRect)

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.snake.control(event)  # Управление змейкой

    def secondScreen(self):

        while True:
            self.screen.fill('white')
            self.drawSomeTHink('В этой игре тебе нужно кушать яблочки змейкой)',
                               25, self.WINDOW_SIZE / 2, self.WINDOW_SIZE / 2, 'black')
            self.drawSomeTHink('Управление с помощью стрелочек',
                               25, self.WINDOW_SIZE / 2, self.WINDOW_SIZE / 2 + 40, 'black')
            self.drawPrintYourName('Нажми любую кнопку.')
            self.events = pg.event.get()
            for event in self.events:
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
                    else:
                        return

            pg.display.update()
            self.clock.tick(30)

    def run(self):
        self.new_game()
        self.startScreen()
        self.secondScreen()
        while self.now:
            self.check_event()
            self.now = self.update()
            self.draw()
        self.database.reg(self.textinput.manager.value, self.snake.length)
        self.gameOwerScreen(self.database.getDb())
        self.database.close()

if __name__ == '__main__':
    game = Game()
    game.run()