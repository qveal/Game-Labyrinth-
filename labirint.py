#!Проект лабиринт
from pygame import *
window = display.set_mode((700, 500))
display.set_caption('My second game')
font.init()
class GameSprite(sprite.Sprite):
    def __init__(self, picture, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, picture, x, y, width, height, x_speed, y_speed):
        GameSprite.__init__(self, picture, x, y, width, height)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        if self.x_speed > 0 and self.rect.x <= 620 or self.rect.x >= 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if self.rect.y <= 420 and self.y_speed > 0 or self.rect.y >= 0 and self.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def __init__(self, picture, x, y, width, height, speed):
        GameSprite.__init__(self, picture, x, y, width, height)
        self.speed = speed
        self.side = 'left'
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        elif self.rect.x >= 615:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        elif self.side == 'right':
            self.rect.x += self.speed 
class Bullet(GameSprite):
    def __init__(self, picture, x, y, width, height, x_speed):
        GameSprite.__init__(self,  picture, x, y, width, height)
        self.speed = x_speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 710:
            self.kill()



player = Player('pacman2.png', 270, 250, 80, 80, 0, 0)
w1 = GameSprite('wall.jpg', 120, 180, 250, 50)
w2 = GameSprite('wall.jpg', 370, 100, 50, 400)
barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)
bullets = sprite.Group()
enemies = sprite.Group()
enemy = Enemy('enemy.png', 600, 180, 80, 80, 1)
enemies.add(enemy)
purpose = GameSprite('purpose.png', 600, 400, 80, 80)
font = font.SysFont('Arial', 40)
win = font.render('YOU WIN!', True, (255, 255, 255))
lose = font.render('YOU LOSE', True, (255, 255, 255))
finish = False
color = (130, 170, 220)
run = True
while run:
    time.delay(50)
    for i in event.get():
        if i.type == QUIT:
            run = False 
        elif i.type == KEYDOWN:
            if i.key == K_w:
                player.y_speed = -5
            if i.key == K_a:
                player.x_speed = -5
            if i.key == K_s:
                player.y_speed = 5
            if i.key == K_d:
                player.x_speed = 5
            if i.key == K_SPACE:
                player.fire()
        elif i.type == KEYUP:
            if i.key == K_w:
                player.y_speed = 0
            if i.key == K_a:
                player.x_speed = 0
            if i.key == K_s:
                player.y_speed = 0
            if i.key == K_d:
                player.x_speed = 0
    if not finish:
        window.fill(color)
        player.update()
        bullets.update()
        player.reset()
        bullets.draw(window)
        barriers.draw(window)
        purpose.reset()
        sprite.groupcollide(enemies, bullets, True, True)
        enemies.update()
        enemies.draw(window)
        sprite.groupcollide(barriers, bullets, False, True)
        if sprite.collide_rect(player, purpose):
            finish = True
            window.blit(win, (200, 250))
        if sprite.spritecollide(player, enemies, False):
            finish = True
            window.blit(lose, (180, 250))
    display.update()
