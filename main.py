import pygame
from random import randint, choice
import math

# Начальные значения
pygame.init()
WIN = pygame.display.set_mode((1200, 800))
B_FONT = pygame.font.Font('fonts/Bloody.ttf', 100)
B_FONT_S = pygame.font.Font('fonts/Bloody.ttf', 50)
pygame.display.set_caption("Игра в таракана")
clock = pygame.time.Clock()
eat_time = 50
game_active = False
instruction = False
name_text = B_FONT.render('ИГРА В ТАРАКАНА', False, 'red')
name_text_rect = name_text.get_rect(center=(600, 300))
instr_text = B_FONT_S.render('НАЖМИТЕ ПРОБЕЛ ДЛЯ СТАРТА', False, 'red')
instr_text_rect = name_text.get_rect(center=(600, 500))
instr_text_rect_2 = instr_text.get_rect(center=(600, 700))
get_instr = B_FONT_S.render('НАЖМИТЕ "i" ДЛЯ ИНСТРУКЦИЙ', False, 'red')
get_instr_rect = get_instr.get_rect(center=(600, 600))
move_instr = B_FONT_S.render('W бежать вперед', False, 'red')
move_instr_rect = move_instr.get_rect(center=(600, 400))
rotate_instr = B_FONT_S.render('A и D разворот', False, 'red')
rotate_instr_rect = rotate_instr.get_rect(center=(400, 300))
todo_instr = B_FONT_S.render('Жри еду, уворачивайся от пуль и тапков', False, 'red')
todo_instr_rect = todo_instr.get_rect(center=(550, 500))
eat_sound = pygame.mixer.Sound('sounds/eat.mp3')
shot_sound = pygame.mixer.Sound('sounds/shot.mp3')
back_surface = pygame.image.load('img/table.jpg')
FPS = 60


# Классы
class Hole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

        self.image = pygame.image.load('img/hole.png').convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        if holes_group.__len__() == 7:
            self.kill()


class Roach(pygame.sprite.Sprite):
    VEL = 8
    R_VEL = 5

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('img/roach.png').convert_alpha()
        self.o_image = self.image
        self.rect = self.image.get_rect(center=(300, 400))
        self.mask = pygame.mask.from_surface(self.image)
        self.vel = 0
        self.rotate_vel = 0
        self.angle = 0
        self.slowdown = 1
        self.pancollide = False

    def roach_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.vel = self.VEL
        if keys[pygame.K_s]:
            self.vel = -self.VEL / 2
        if keys[pygame.K_a]:
            self.rotate_vel = self.R_VEL
        if keys[pygame.K_d]:
            self.rotate_vel = -self.R_VEL

    def roach_rotate(self):
        self.angle += self.rotate_vel
        self.rotate_vel = 0

    def roach_rotation(self):
        self.image = pygame.transform.rotate(self.o_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def roach_move(self):
        if tapok.sprite and tapok.sprite.rect.colliderect(self.rect):
            self.slowdown = 1.2

        radians = math.radians(self.angle - 90)
        vert = math.cos(radians) * self.vel / self.slowdown
        horz = math.sin(radians) * self.vel / self.slowdown

        self.rect.x -= horz
        self.rect.y -= vert
        self.vel = 0
        self.slowdown = 1

    def roach_collision(self):
        if self.rect.right >= 1230:
            self.rect.right = 1230
        if self.rect.left <= -30:
            self.rect.left = -30
        if self.rect.bottom >= 820:
            self.rect.bottom = 820
        if self.rect.top <= -20:
            self.rect.top = -20

    def pan_collision(self, xy):
        for p in pan:
            print(xy)


    def update(self):
        self.roach_input()
        self.roach_rotate()
        self.roach_rotation()
        self.roach_move()
        self.roach_collision()


class Killers(pygame.sprite.Sprite):
    VEL = 5

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/laser.png').convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(center=(randint(100, 1100), randint(600, 700)))

        self.x_vel = 0
        self.y_vel = 0
        self.angel = 0

        self.cooldown = 90

    def restart_position(self):
        self.rect = self.image.get_rect(center=(randint(100, 1100), randint(600, 700)))

    def shoot(self):
        global game_active
        if self.cooldown:
            self.cooldown -= 1
        else:
            if roach.sprite.rect.colliderect(self.rect):
                shot_sound.play()
                if holes_group.__len__() <= 7:
                    holes_group.add(Hole(self.rect.centerx, self.rect.centery))
            if roach.sprite.rect.collidepoint(self.rect.centerx, self.rect.centery):
                roach.sprite.kill()
                game_active = False
                self.restart_position()
            self.cooldown = randint(60, 80)

    def move(self):
        if self.rect.colliderect(roach.sprite.rect):
            self.x_vel = self.x_vel / 1.1
            self.y_vel = self.y_vel / 1.1
        if not rect_centers_collision(self.rect, roach.sprite.rect):
            self.rect.centerx -= self.x_vel
            self.rect.centery -= self.y_vel

        self.x_vel = 0
        self.y_vel = 0

        # print(self.rect.centerx, self.rect.centery)

    def follow(self):
        df_x = self.rect.centerx - roach.sprite.rect.centerx
        df_y = self.rect.centery - roach.sprite.rect.centery
        self.angel = math.atan2(df_y, df_x)

        self.x_vel = math.cos(self.angel) * self.VEL
        self.y_vel = math.sin(self.angel) * self.VEL

    def update(self):
        self.follow()
        self.move()
        self.shoot()


class Tapok(Killers):
    def __init__(self, x, y):
        super().__init__()
        tapok_1 = pygame.image.load('img/tapok_border.png').convert_alpha()
        tapok_2 = pygame.image.load('img/tapok.png').convert_alpha()
        self.frames = [tapok_1, tapok_2]
        self.angel = randint(1, 180)
        self.image = pygame.transform.rotozoom(self.frames[0], self.angel, 1.5)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = 0
        self.life_time = 200
        self.attack_time = 80
        self.sound_play = True
        self.attack_allow = True
        self.sound = pygame.mixer.Sound('sounds/punch.mp3')

    def attack(self):
        global game_active
        if self.attack_time:
            self.attack_time -= 1
        else:
            self.image = pygame.transform.rotozoom(self.frames[1], self.angel, 1.5)
            self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
            self.mask = pygame.mask.from_surface(self.image)
            if pygame.sprite.collide_mask(roach.sprite, tapok.sprite) and self.attack_allow:
                roach.sprite.kill()
                game_active = False
            if self.attack_allow:
                self.sound.play()
                self.attack_allow = False
            self.attack_time = randint(70, 80)

    def delete(self):
        if self.life_time:
            self.life_time -= 1
        else:
            self.kill()
            self.life_time = 200

    def update(self):
        self.delete()
        self.attack()


class Pan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        pan_1 = pygame.image.load('img/pan_border.png').convert_alpha()
        pan_2 = pygame.image.load('img/pan.png').convert_alpha()
        self.frames = [pan_1, pan_2]
        self.angel = randint(1, 180)
        self.image = pygame.transform.rotozoom(self.frames[0], self.angel, 1.3)
        self.rect = self.image.get_rect(center=(randint(100, 1100), randint(100, 700)))
        self.mask = pygame.mask.from_surface(self.image)
        self.life_time = 50000
        self.attack_time = 100
        self.sound_play = True
        self.attack_allow = True
        self.sound = pygame.mixer.Sound('sounds/pan.mp3')

    def attack(self):
        global game_active
        if self.attack_time:
            self.attack_time -= 1
        else:
            self.image = pygame.transform.rotozoom(self.frames[1], self.angel, 1.3)
            self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
            self.mask = pygame.mask.from_surface(self.image)
            if pygame.sprite.collide_mask(roach.sprite, pan.sprite) and self.attack_allow:
                roach.sprite.kill()
                game_active = False
            if self.attack_allow:
                self.sound.play()
                self.attack_allow = False
            self.attack_time = randint(90, 100)

    def delete(self):
        if self.life_time:
            self.life_time -= 1
        else:
            self.kill()
            self.life_time = 500

    def get_mask(self):
        return self.mask

    def update(self):
        self.delete()
        self.attack()


class Food(pygame.sprite.Sprite):
    def __init__(self, ftype):
        super().__init__()

        if ftype == 'hotdog':
            self.image = pygame.image.load('img/hotdog.png').convert_alpha()

        if ftype == 'salami':
            self.image = pygame.image.load('img/salami.png').convert_alpha()

        if ftype == 'burger':
            self.image = pygame.image.load('img/burger.png').convert_alpha()

        self.rect = self.image.get_rect(center=(randint(100, 1100), randint(100, 700)))


# Группы
roach = pygame.sprite.GroupSingle()
roach.add(Roach())

killers_group = pygame.sprite.Group()

tapok = pygame.sprite.GroupSingle()
pan = pygame.sprite.GroupSingle()

food_group = pygame.sprite.Group()

holes_group = pygame.sprite.Group()

# Таймер
food_timer = pygame.USEREVENT + 1
killers_timer = pygame.USEREVENT + 2
tapok_timer = pygame.USEREVENT + 3
pan_timer = pygame.USEREVENT + 4
pygame.time.set_timer(killers_timer, 2000)
pygame.time.set_timer(food_timer, 2000)
pygame.time.set_timer(tapok_timer, 6000)
pygame.time.set_timer(pan_timer, 1000)


# Функции
def roach_pan_colliede():
    if pygame.sprite.collide_mask(roach.sprite, pan.sprite):
        for p in pan:
            if not p.attack_allow:
                for r in roach:
                    r.pan_collision(pygame.sprite.collide_mask(roach.sprite, pan.sprite))


def rect_centers_collision(rect1, rect2):
    if rect1.centerx == rect2.centerx and rect1.centery == rect2.centery:
        return True
    else:
        return False


def collision_sprite(time_counter, score):
    global eat_time
    for food in food_group:
        if pygame.sprite.spritecollide(food, roach, False):
            if time_counter == eat_time:
                food.kill()
                eat_sound.play()
                return 0, score + 1
            else:
                return time_counter + 1, score
    return 0, score


def main():
    run = True
    global game_active
    global instruction
    time_counter = 0
    score = 0
    score_text = B_FONT.render(f'счёт: {score}', False, 'red')
    score_rect = score_text.get_rect(topleft=(10, 10))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if game_active:
                if event.type == food_timer and food_group.__len__() <= 2:
                    food_group.add(Food(choice(['hotdog', 'burger', 'salami'])))
                if event.type == killers_timer and killers_group.__len__() <= 0:
                    killers_group.add(Killers())
                if event.type == tapok_timer and tapok.__len__() <= 0:
                    tapok.add(Tapok(roach.sprite.rect.centerx, roach.sprite.rect.centery))
                #Здесь должны были добовляться сковороды, но я не разобрался с их колизией
                #if event.type == pan_timer and pan.__len__() <= 0:
                 #   pan.add(Pan())

            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    instruction = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_i and not game_active:
                    instruction = True
                    game_active = False
        if game_active:
            WIN.blit(back_surface, (0, 0))
            score_text = B_FONT.render(f'счёт: {score}', False, 'red')
            WIN.blit(score_text, score_rect)

            holes_group.draw(WIN)
            holes_group.update()

            food_group.draw(WIN)

            pan.draw(WIN)
            pan.update()

            tapok.draw(WIN)
            tapok.update()

            roach.draw(WIN)
            roach.update()
            if game_active:
                killers_group.draw(WIN)
                killers_group.update()

            time_counter, score = collision_sprite(time_counter, score)
            if pan and roach:
                roach_pan_colliede()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        elif instruction:
            WIN.blit(back_surface, (0, 0))
            roach.draw(WIN)
            WIN.blit(move_instr, move_instr_rect)
            WIN.blit(instr_text, instr_text_rect_2)
            WIN.blit(rotate_instr, rotate_instr_rect)
            WIN.blit(todo_instr, todo_instr_rect)
        else:
            WIN.blit(back_surface, (0, 0))
            WIN.blit(name_text, name_text_rect)
            WIN.blit(instr_text, instr_text_rect)
            WIN.blit(get_instr, get_instr_rect)
            roach.add(Roach())
            score = 0
            holes_group.empty()
            tapok.empty()
            pan.empty()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
