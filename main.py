import sys
import random

import pygame as pg

from utils import support

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60

FONT_FILE = "font/HanyiyanKaiW-2.ttf"

enemics = [
    support.get_enemies("graphics/Enemies/Chicken/Run.png", 32, 34),
    support.get_enemies("graphics/Enemies/AngryPig/Run.png", 36, 30),
]
PLAYER_ENEMY_DESTROY = pg.USEREVENT + 1


class Enemy(pg.sprite.Sprite):
    animate_index = 0
    frame_duration = 50
    last_frame_time = pg.time.get_ticks()

    frames = []

    def __init__(self):
        super().__init__()
        self.frames = random.choice(enemics)
        self.image = self.frames[self.animate_index]
        self.rect = self.frames[0].get_rect(bottomright=(600, 300))

    def animate_state(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_frame_time >= self.frame_duration:
            self.image = self.frames[self.animate_index]
            self.animate_index = (self.animate_index + 1) % len(self.frames)
            self.last_frame_time = current_time

    def update(self, *args, **kwargs):
        self.animate_state()
        self.rect.x -= 2
        self.destroy()

    def destroy(self, *args, **kwargs):
        if self.rect.x <= 10:
            self.kill()
            pg.time.set_timer(PLAYER_ENEMY_DESTROY, 500, 1)


class Player(pg.sprite.Sprite):
    idel_index = 0
    run_index = 0
    is_idel = True
    is_run = False
    is_jump = False
    gravity = 0

    def __init__(self):
        super().__init__()
        idel_resource = "./graphics/JungleAssetPack/Character/sprites/idle.gif"
        run_resource = "./graphics/JungleAssetPack/Character/sprites/run.gif"

        self.jump_surf = pg.image.load(
            "graphics/JungleAssetPack/Character/sprites/jump.png"
        )

        self.jump_surf = pg.transform.scale(
            self.jump_surf,
            (
                self.jump_surf.get_width() * 1.5,
                self.jump_surf.get_height() * 1.5,
            ),
        )

        self.idel_frames = support.load_animation(idel_resource)
        self.image = self.idel_frames[0]
        self.rect = self.image.get_rect(midbottom=(200, 300))

        self.run_frames = support.load_animation(run_resource)

    def input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE] and self.rect.bottom >= 300:
            self.is_idel = False
            self.is_jump = True
            self.gravity = -20

        if keys[pg.K_RIGHT]:
            self.is_idel = False
            self.is_run = True

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            if not self.is_run:
                self.is_jump = False
                self.is_idel = True

    def update(self, *args, **kwargs):
        if self.is_idel:
            self.idel()
        elif self.is_jump:
            self.image = self.jump_surf
        elif self.is_run:
            self.run()

        self.input()
        self.apply_gravity()

    def run(self):
        self.image = self.run_frames[self.run_index]
        self.run_index = (self.run_index + 1) % len(self.run_frames)

    def idel(self):
        self.image = self.idel_frames[self.idel_index]
        self.idel_index = (self.idel_index + 1) % len(self.idel_frames)


def display_score():
    current_time = pg.time.get_ticks() - start_time
    score_surf = score_font.render(f"得分：{current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)


def collision_sprite():
    if pg.sprite.spritecollide(player.sprite, enemies, False):
        enemies.empty()
        return False
    return True


pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("打到小金王八蛋")
clock = pg.time.Clock()

player = pg.sprite.GroupSingle()
player.add(Player())

enemies = pg.sprite.Group()
enemies.add(Enemy())

# 字体
score_font = pg.font.Font(FONT_FILE, 25)
game_font = pg.font.Font(FONT_FILE, 25)


game_name = game_font.render("打倒小明朝", True, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

# font = pg.font.SysFont('SimHei', 50)  # 这里使用了微软雅黑字体，字号为40


sky_surface = pg.image.load("graphics/Sky.png").convert()
ground_surface = pg.image.load("graphics/ground.png").convert()
snail_surface = pg.image.load("graphics/snail/snail1.png").convert_alpha()
# player_surf = pg.image.load("graphics/player/player_walk_1.png").convert_alpha()

player_stand_surf = pg.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand_surf = pg.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(center=(400, 200))


game_active = True
start_time = pg.time.get_ticks()

# player_jump_frame_index = 0
# position(new) = position(old) + velocity×time_interval
# 使用欧拉公式模拟重力效果
# player_state = 0
while True:
    display_score()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if game_active:
            if event.type == PLAYER_ENEMY_DESTROY:
                enemies.add(Enemy())

        else:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                game_active = True
                start_time = pg.time.get_ticks()

    if game_active:
        display_score()
        screen.blit(sky_surface, (0, 0))  # (x, y)("red")
        screen.blit(ground_surface, (0, 300))  # (x, y)("red")
        display_score()

        # player class
        player.draw(screen)
        player.update()

        enemies.draw(screen)
        enemies.update()
        game_active = collision_sprite()
    else:
        screen.fill("black")
        screen.blit(player_stand_surf, player_stand_rect)
        screen.blit(game_name, game_name_rect)

    pg.display.update()
    clock.tick(FPS)
