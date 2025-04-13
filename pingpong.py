from pygame import *
from random import randint

# Настройки окна
window = display.set_mode((700, 500))
display.set_caption('Ping-pong')
BACKCOLOR = (70, 109, 214)

# Переменные счета
score1 = 0
score2 = 0
win_score = 3  # Очки для победы

def reset_game():
    """Сброс игры до начального состояния."""
    global score1, score2, finish
    score1 = 0
    score2 = 0
    finish = False
    ball.reset_ball()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 400:
            self.rect.y += self.speed

    def update_r(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 400:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        super().__init__(player_image, player_x, player_y, w, h, player_speed)
        self.reset_ball()

    def reset_ball(self):
        """Размещает мяч в центре и задает случайное направление."""
        self.rect.x = 350
        self.rect.y = 250
        self.speed_x = randint(-4, 4) or 4
        self.speed_y = randint(-4, 4) or 4

    def update(self, player1, player2):
        global score1, score2, finish
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Отскок от верхнего и нижнего края
        if self.rect.y <= 0 or self.rect.y >= 490:
            self.speed_y *= -1

        # Отскок от ракеток с ускорением
        if self.rect.colliderect(player1.rect) or self.rect.colliderect(player2.rect):
            self.speed_x *= -1.1  # Ускорение при ударе

        # Проверка на выход за границы (гол)
        if self.rect.x <= 0:
            score2 += 1  # Игрок справа получает очко
            self.reset_ball()
        elif self.rect.x >= 700:
            score1 += 1  # Игрок слева получает очко
            self.reset_ball()

        # Проверка на победу
        if score1 >= win_score or score2 >= win_score:
            finish = True

player1 = Player("racket.png", 55, 250, 20, 100, 5)
player2 = Player("racket.png", 630, 250, 20, 100, 5)
ball = Ball("tenis_ball.png", 350, 250, 20, 20, 5)

game = True
finish = False
font.init()
font = font.SysFont('Arial', 40)

# Игровой цикл
while game:
    window.fill(BACKCOLOR)
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_r:  # Нажатие 'R' для перезапуска
            reset_game()

    if finish:
        # Отображение победного сообщения
        winner = "Игрок 1 выиграл!" if score1 >= win_score else "Игрок 2 выиграл!"
        win_text = font.render(winner, True, (255, 255, 255))
        window.blit(win_text, (200, 200))
    else:
        player1.reset()
        player1.update_l()
        player2.reset()
        player2.update_r()
        ball.reset()
        ball.update(player1, player2)

        # Отображение счета
        score_text = font.render(f"{score1} : {score2}", True, (255, 255, 255))
        window.blit(score_text, (320, 10))

    display.update()
    time.delay(10)







