from pygame import *
from random import randint
from time import time as timer
window = display.set_mode((750,500))
display.set_caption('Шутер')

mixer.init()
mixer.music.load('дуло.mp3')
mixer.music.play()
fire_sound = mixer.Sound('pusk.mp3')
damage_sound = mixer.Sound('попадание.mp3')
vzriv_sound = mixer.Sound('взрыв.mp3')
#шрифты
font.init()
font1 = font.Font(None,70)
win = font1.render('YOU WIN', True, (0,255,0))
lose = font1.render('YOU LOSE', True, (255,0,0))
font2 = font.Font(None, 40)

clock = time.Clock()
FPS = 60
game = True

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_size_x, player_size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def update(self):
        global last_time
        global num_fire
        global rel_time
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 670:
            self.rect.x += self.speed
        if key_pressed[K_SPACE]:
            if num_fire < 3 and rel_time == False:
                num_fire += 1
                fire_sound.play()
                self.fire()
            if num_fire >= 3 and rel_time == False:
                last_time = timer()
                rel_time = True


        
    def fire(self):
        bullet = Bullet('m-20.png', self.rect.centerx, self.rect.top, 12, 20, 20)
        bullets.add(bullet)
        
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #сколько прошло кораблей
        global lost
        #проверка выхода за Игрока
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(1,670)
            lost = lost + 1
class Boss(GameSprite):
    def update(self):
        self.rect.y += self.speed


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

background = GameSprite('bg.jpg', 0,0,0,750,500)
m_h = Player('pvo.png', 300,420,10,80,80)
boss = Boss('boss.png', randint(50, 650), 10, 100, 100, 2)
rocket = GameSprite('m-20.png', 300,400,10,20,20)
dulo = mixer.Sound('pusk.mp3')
enemys = sprite.Group()
for i in range(1, 8):
    enemy = Enemy('самолёт пригожина.png', randint(50, 650), 10, 1, 100,105)
    enemys.add(enemy)
#spisok pul`
bullets = sprite.Group()
score = 0
goal = 1000
finish = False
run = True
last_time = 0
num_fire = 0
rel_time = False
life = 3
boss_hp = 15

start_game = timer()


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    text_score = font2.render('Самолётов сбито: '+str(score), True, (255,255,255))
    text_lose = font2.render('Потерь: ' +str(lost),True,(255,255,255))
    text_life = font2.render('Жизни: ' +str(life),True,(255,0,0))

    collides = sprite.groupcollide(enemys, bullets, True, True)
    if collides:
        vzriv_sound.play()
    for c in collides:
        score = score + 1
        enemy = Enemy('самолёт пригожина.png', randint(50, 650), 10, 1, 100,105)
        enemys.add(enemy)
        



    if not finish:
        background.reset()
        window.blit(text_score, (10,10))
        window.blit(text_lose, (10,50))
        window.blit(text_life, (600,50))
        m_h.reset()
        if score > 30:
            boss.reset()

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 0.5:
                ammo_now = font2.render('нет ракет', 1, (255, 0, 0))
                window.blit(ammo_now, (260,460))
            else:
                num_fire = 0
                rel_time = False


        
        m_h.update()
        enemys.draw(window)
        bullets.draw(window)
        enemys.update()
        boss.update()
        key_pressed = key.get_pressed()
        if key_pressed[K_SPACE]:
            dulo.play()
        bullets.update()
        if sprite.spritecollide(boss, bullets, True):
            boss_hp -= 1
        if sprite.spritecollide(m_h, enemys, True) or lost >= 10:
            life -= 1
            enemy = Enemy('самолёт пригожина.png', randint(50, 650), 10, 1, 100,105)
            enemys.add(enemy)
            damage_sound.play()
        if life <= 0:
            finish = True
            window.blit(lose,(200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (750/2, 500/2))

    
        


        if boss_hp <= 0:
            boss.kill()
        display.update()
    clock.tick(FPS)