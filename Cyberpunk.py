import pygame as pg

pg.init()
window = pg.display.set_mode((500,500)) #создание экрана и базовых переменных
clock = pg.time.Clock()
keyleft = False
keyright = False
spdx = 3
spdy = 3
over = True
background = pg.transform.scale(pg.image.load('EGS_Cyberpunk2077_CDPROJEKTRED_S2_03_1200x1600_b1847981214ac013.jpg'), (500, 500))

class Area(): #создание функций для работы с хитбоксами
    def __init__(self, x, y, widht, height):
        self.rect = pg.Rect(x, y, widht, height)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

class Picture(Area): #создание функций для отрисовки объектов
    def __init__(self, filename, x, y, widht, height):
        Area.__init__(self, x, y, widht, height)
        self.image = pg.image.load(filename)

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Label(Area): #создание функций для отрисовки текста
    def set_text(self, text, fsize = 32, text_color=(0, 0, 0)):
        self.image = pg.font.Font(None, fsize).render(text, True, text_color)

    def draw(self, x, y):
        window.blit(self.image, (self.rect.x, self.rect.y))

platformx = 200 #создание объектов
ball = Picture('skipball.png', 220, 290, 50, 50)
platform = Picture('platform.png', platformx, 350, 100, 30)
enemies = list() #реализация удобного способа создания врагов
n = 9
enmx = 5
enmy = 5
for i in range(3):
    x = enmx + (27*i)
    y = enmy + (50*i)
    for gh in range(n):
        enemy = Picture('Arasaka.png', x, y, 50, 50)
        enemies.append(enemy)
        x += 55
    n -= 1

while over: #начинается игровой цикл
    window.blit(background, (0,0)) #отрисовка фона, мяча и платформы, врага
    ball.draw()
    platform.draw()
    for enemy in enemies: 
        enemy.draw()
        if enemy.rect.colliderect(ball.rect): #проверка на соприкосновение
            enemies.remove(enemy)
            spdy *= -1
    for event in pg.event.get(): #проверка событий
        if event.type == pg.QUIT:
            over = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                keyleft = True
            elif event.key == pg.K_RIGHT:
                keyright = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                keyright = False
            elif event.key == pg.K_LEFT:
                keyleft = False
    if keyleft: #движение по клавишам стрелок
        platform.rect.x -=3
    elif keyright:
        platform.rect.x +=3
    if ball.colliderect(platform.rect): #соприкосновение мяча с платформой
        spdy *= -1
    if ball.rect.y < 0: #границы
        spdy *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        spdx *= -1
    if len(enemies) == 0: #условие выигрыша
        background = pg.transform.scale(pg.image.load('Без названия123_20260329200036.png'), (500, 500))
        window.blit(background, (0,0))
        timeText = Label(180, 150, 50, 50)
        timeText.set_text('победив', 80, (145, 215, 165))
        timeText.draw(10, 10)
        over = False
        pg.display.update()
    if ball.rect.y > 370: #условие проигрыша
        background = pg.transform.scale(pg.image.load('Без названия123_20260329192529.png'), (500, 500))
        window.blit(background, (0,0))
        timeText = Label(100, 150, 50, 50)
        timeText.set_text('пшл вон лузер', 80, (255, 0, 0))
        timeText.draw(10, 10)
        over = False
        pg.display.update()
    ball.rect.x += spdx
    ball.rect.y += spdy
    pg.display.update() #обновление сцены по кол-ву кадров ниже
    clock.tick(50)
