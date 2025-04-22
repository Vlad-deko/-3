from pygame import *

win_width = 700
win_height = 500
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))

background_image = transform.scale(image.load('fom.jpg'), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
        if self.rect.x <= win_width - 80 and self.x_speed > 0 or self.rect.x >= 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:  # идём направо, правый край персонажа - вплотную к левому краю стены
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)  # если коснулись сразу нескольких, то правый край - минимальный из возможных
        elif self.x_speed < 0:  # идем налево, ставим левый край персонажа вплотную к правому краю стены
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)  # если коснулись нескольких стен, то левый край - максимальный
        if self.rect.y <= win_height - 80 and self.y_speed > 0 or self.rect.y >= 0 and self.y_speed < 0:
            self.rect.y += self.y_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:  # идем вниз
            for p in platforms_touched:
                # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:  # идём вверх
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)  # выравниваем верхний край по нижним краям стенок, на которые наехали

    def shoot(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 20, 20, 10)
        bullets.add(bullet)


class Enemy(GameSprite):
    side = 'left'

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.side == 'left':
            self.rect.x -= self.speed
            if sprite.spritecollide(self, barriers, False):
                self.rect.x += self.speed
                self.side = 'right'
        else:
            self.rect.x += self.speed
            if sprite.spritecollide(self, barriers, False):
                self.rect.x -= self.speed
                self.side = 'left'


class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()


barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()


walls = [
    GameSprite('s1.jpg', win_width / 2 - win_width / 3, win_height / 2, 300, 30),
    GameSprite('s1.jpg', 370, 100, 50, 400),
    GameSprite('s1.jpg', 420, 350, 200, 50),
    GameSprite('s1.jpg', 520, 100, 190, 50),
    GameSprite('s1.jpg', 115, 370, 170, 30),
    GameSprite('s1.jpg', 115, 400, 50, 100),
    GameSprite('s1.jpg', 120, 0, 40, 150),
    GameSprite('s1.jpg', 690, 100, 10, 400),
]


barriers.add(walls)

packman = Player('f5.png', 167, 400, 60, 60, 0, 0)
monster1 = Enemy('monster12.png', win_width - 100, 180, 60, 40, 2)
monster2 = Enemy('monster12.png', 180, 80, 60, 40, 2)
monsters.add(monster1)
monsters.add(monster2)

final_sprite = GameSprite('fiinal.png', 420, 400, 100, 120)

finish = False

run = True
while run:

    time.delay(50)

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.shoot()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0

    if not finish:
        window.blit(background_image, (0, 0))

        barriers.draw(window)
        bullets.draw(window)
        final_sprite.reset()

        packman.reset()
        monsters.update()
        monsters.draw(window)

        sprite.groupcollide(monsters, bullets, True, True)
        sprite.groupcollide(bullets, barriers, True, False)

        packman.update()

        if sprite.spritecollide(packman, monsters, False):
            finish = True

            img = image.load('nif.jpg')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('win.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

    bullets.update()
    display.update()