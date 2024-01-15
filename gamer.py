import pygame
import math

import sqlite3


# игровые настройки
WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
TILE = 100
FPS_POS = (WIDTH - 65, 5)
SENSETIV = 0.003
TIME_POS = (10, 10)
LIFE1 = 3
LIFE_POS = (10, 40)

# текстуры
TEXTURE_WIDTH = 1080
TEXTURE_HEIGHT = 1080
TEXTURE_SCALE = TEXTURE_HEIGHT // TILE

# миникарта
MINIMAP = 4
MINIMAP_RES = (WIDTH // MINIMAP, HEIGHT // MINIMAP)
MAP_SCALE = 2 + MINIMAP
MAP_TILE = TILE // MAP_SCALE // 2
MAP_POS = (20, HEIGHT - HEIGHT // MINIMAP - 40)

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 300
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(FOV / 2))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

# игрок
player_pos = (1351, 1451)
player_angle = 300

# спрайты
DOUBLE_PI = 2 * math.pi
CENTER_RAY = NUM_RAYS // 2 - 1
FAKE_RAYS = 100

MOMEY_MINI = [(1, 1), (6, 2), (3, 15), (5, 13), (11, 16), (13, 1), (20, 17), (20, 11), (23, 3),
              (29, 15), (30, 6)]
MOMEY_MINI2 = [(1, 1), (6, 2), (3, 15), (5, 13), (11, 16), (13, 1), (20, 17), (20, 11), (23, 3),
               (29, 15), (30, 6)]
A = 10
ANGLE = 0
LVL = 1
starttime = 0
g = 0


def player_speed():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
        return 10
    else:
        return 5


# карта
_ = False
text_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 5, 1],
    [1, _, _, _, 1, 1, 1, 1, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 2, _, _, 3, _, _, _, _, 6, _, 1, _, 1, 2, 1, 1, 1, _, 5, 3, 1, 1, 1, _, 1, 1, 1, 1, 1, _, 1],
    [1, _, 7, _, _, 1, _, 6, 6, _, 1, _, 1, _, 1, _, _, _, 1, 1, 1, _, _, _, 1, _, _, _, _, _, 1, _, 1],
    [1, _, 1, _, _, 1, _, 6, 6, _, _, _, 1, _, 1, _, 1, _, _, _, _, _, 1, _, _, _, _, 5, 6, _, 1, _, 3],
    [1, _, 1, _, _, 1, _, 6, 6, _, 7, _, 1, _, 1, _, 7, 7, 1, 1, 1, _, 1, _, 1, 1, _, 1, 1, _, 1, _, 6],
    [1, _, 9, _, _, 1, _, _, _, _, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, 1, 7, _, _, 1, _, _, _, 6],
    [1, _, 1, _, _, 1, 2, 1, 1, 1, 1, _, 1, _, _, _, 1, 1, _, 1, _, 1, 1, 1, 1, _, _, _, 1, _, 1, _, 6],
    [1, _, 1, _, _, _, _, 1, 7, 7, _, _, 1, 5, 1, 1, 1, 1, _, 1, _, _, 7, _, _, _, _, 1, 1, _, 1, _, 6],
    [1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1, 1, _, 7, 1, 1, 1, _, _, _, _, 9, _, 6],
    [1, _, 1, _, 1, _, 5, _, 9, 1, 1, 1, 1, _, 1, _, _, 1, _, 1, _, _, _, _, _, _, _, _, 1, _, 1, _, 4],
    [1, _, _, _, 1, _, 5, _, 0, _, _, _, 1, _, 1, 1, _, 1, _, 1, _, 1, _, _, _, 1, 1, 1, 1, 1, 6, _, 1],
    [1, _, 6, _, 5, _, 5, _, 1, _, 1, _, 1, _, 7, 1, _, 6, _, 1, _, 1, _, 7, _, 1, _, _, _, _, 1, _, 7],
    [1, _, 1, _, 1, _, _, _, 1, _, _, 1, 8, _, 8, 1, _, 7, _, 4, _, 1, 1, 1, 1, 7, _, 6, 6, _, 1, _, 1],
    [1, _, 1, _, 1, 1, 1, 1, 1, _, _, 1, 8, _, 8, 1, _, 1, _, _, _, _, _, _, _, _, _, 6, 6, _, 1, _, 1],
    [1, _, 1, _, _, _, _, _, _, _, 1, 1, 8, 8, 8, 6, _, 5, 1, 9, 1, 1, 1, 1, _, 1, _, _, _, _, 1, _, 1],
    [1, _, 1, 1, 1, 1, 4, 1, 1, _, 6, _, 1, 1, 1, 7, _, _, _, _, _, _, _, _, _, 1, 4, 1, 6, 1, 9, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, 1, _, _, 4, 3, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 5, 1]

]

text_map2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 5, 1],
    [1, _, _, _, 1, _, 1, 1, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 2, _, 1, _, _, _, _, _, 6, _, 1, _, 1, 2, 1, 1, 1, _, 5, 3, 1, 1, 1, _, 1, 1, 1, 1, 1, _, 1],
    [1, _, 7, _, 1, _, 1, 6, 6, _, 1, _, 1, _, 1, _, _, _, 7, _, 1, _, _, _, 1, _, 1, _, _, _, 1, _, 1],
    [1, _, _, _, 1, _, _, 6, 6, _, _, _, 1, _, 1, _, 1, _, _, _, 4, _, 1, _, _, _, 5, _, 6, _, 1, _, 3],
    [1, _, 1, 4, 1, 1, _, 6, 6, _, 7, _, 1, _, 1, _, 7, 7, 1, 1, 1, _, 1, _, 1, 1, 1, _, 1, _, 1, _, 6],
    [1, _, 9, _, _, _, _, _, _, _, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, 1, 7, 1, _, 1, _, _, _, 6],
    [1, _, 1, _, 1, 1, _, 1, 1, 1, 1, _, 1, _, _, _, 1, 1, _, 1, _, 1, 1, 1, 1, _, 1, _, _, _, 1, _, 6],
    [1, _, 1, _, _, _, _, 2, 1, _, _, _, 1, 5, 1, 1, 1, 1, _, 1, _, _, _, _, _, _, _, 1, 1, 9, 1, _, 6],
    [1, _, 1, _, 1, _, _, _, _, _, 1, _, _, _, _, _, _, 1, _, 1, 1, 1, 7, 1, 1, 1, _, _, _, _, 9, _, 6],
    [1, _, 1, _, 1, _, 5, _, 9, 1, 1, 1, 1, _, 1, _, _, 1, _, 1, _, _, _, _, _, _, _, _, 1, _, 1, _, 4],
    [1, _, 3, _, 1, _, 5, _, _, _, _, _, 1, _, 1, 1, _, 1, _, 1, _, 1, _, _, _, 1, 1, 1, 1, _, 6, _, 1],
    [1, _, 6, _, 5, _, 5, _, 1, 6, _, _, 1, _, 7, 1, _, 6, _, 1, _, 1, _, 7, 1, 1, _, _, _, _, 1, _, 7],
    [1, _, 1, _, 1, _, _, _, 1, 3, _, 1, 8, _, 8, 1, _, 7, _, 4, _, 1, 1, 1, 1, 7, _, 6, 6, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, 1, 1, _, _, 1, 8, _, 8, 1, _, 1, _, _, _, _, _, _, _, _, _, 6, 6, _, 1, _, 1],
    [1, _, 1, _, _, _, 1, _, _, _, 7, 1, 8, 8, 8, 6, _, 5, 1, 9, 1, 1, 1, 1, _, 1, _, _, _, _, 1, _, 1],
    [1, _, 1, 1, 9, 1, 4, _, 1, _, _, _, 1, 1, 1, 7, _, _, _, _, _, _, _, _, _, 1, 4, 1, 6, 1, 9, _, 1],
    [1, _, _, _, _, _, _, _, 9, 1, 1, _, _, _, _, _, _, _, 1, 1, _, _, 4, 3, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 5, 1]

]

WORLD_WIDTH = len(text_map[0]) * TILE
WORLD_HEIGHT = len(text_map[0]) * TILE
world_map = {}
mini_map = set()
walls1 = []
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char:
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            walls1.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == 1:
                world_map[(i * TILE, j * TILE)] = 1
            elif char == 2:
                world_map[(i * TILE, j * TILE)] = 2
            elif char == 3:
                world_map[(i * TILE, j * TILE)] = 3
            elif char == 4:
                world_map[(i * TILE, j * TILE)] = 4
            elif char == 5:
                world_map[(i * TILE, j * TILE)] = 5
            elif char == 6:
                world_map[(i * TILE, j * TILE)] = 6
            elif char == 7:
                world_map[(i * TILE, j * TILE)] = 7
            elif char == 8:
                world_map[(i * TILE, j * TILE)] = 8
            elif char == 9:
                world_map[(i * TILE, j * TILE)] = 9

WORLD_WIDTH = len(text_map[0]) * TILE
WORLD_HEIGHT = len(text_map[0]) * TILE
world_map2 = {}
mini_map2 = set()
walls2 = []
for j, row in enumerate(text_map2):
    for i, char in enumerate(row):
        if char:
            mini_map2.add((i * MAP_TILE, j * MAP_TILE))
            walls2.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == 1:
                world_map2[(i * TILE, j * TILE)] = 1
            elif char == 2:
                world_map2[(i * TILE, j * TILE)] = 2
            elif char == 3:
                world_map2[(i * TILE, j * TILE)] = 3
            elif char == 4:
                world_map2[(i * TILE, j * TILE)] = 4
            elif char == 5:
                world_map2[(i * TILE, j * TILE)] = 5
            elif char == 6:
                world_map2[(i * TILE, j * TILE)] = 6
            elif char == 7:
                world_map2[(i * TILE, j * TILE)] = 7
            elif char == 8:
                world_map2[(i * TILE, j * TILE)] = 8
            elif char == 9:
                world_map2[(i * TILE, j * TILE)] = 9


def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


class Player:
    def __init__(self, walls):
        self.walls = walls
        self.x, self.y = player_pos
        self.angle = player_angle
        self.side = 50
        self.rect1 = pygame.Rect(*player_pos, self.side, self.side)

    @property
    def pos(self):
        return self.x, self.y

    def st(self, dx, dy):
        next_r = self.rect1.copy()
        next_r.move_ip(dx, dy)
        hit = next_r.collidelistall(self.walls)

        if len(hit):
            del_x = 0
            del_y = 0
            for i in hit:
                rect2 = self.walls[i]
                if dx > 0:
                    del_x += next_r.right - rect2.left
                else:
                    del_x += rect2.right - next_r.left
                if dy > 0:
                    del_y += next_r.bottom - rect2.top
                else:
                    del_y += rect2.bottom - next_r.top

            if abs(del_x - del_y) < 10:
                dx = 0
                dy = 0
            elif del_x > del_y:
                dy = 0
            elif del_x < del_y:
                dx = 0
        self.x += dx
        self.y += dy

    def movement(self):
        self.keys()
        self.mouse()
        self.rect1.center = self.x, self.y

    def mouse(self):
        if pygame.mouse.get_focused():
            diff = pygame.mouse.get_pos()[0] - WIDTH // 2
            pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
            self.angle += diff * SENSETIV

    def keys(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()
        if keys[pygame.K_w]:
            dx = player_speed() * cos_a
            dy = player_speed() * sin_a
            self.st(dx, dy)
        if keys[pygame.K_s]:
            dx = -player_speed() * cos_a
            dy = -player_speed() * sin_a
            self.st(dx, dy)
        if keys[pygame.K_a]:
            dx = player_speed() * sin_a
            dy = -player_speed() * cos_a
            self.st(dx, dy)
        if keys[pygame.K_d]:
            dx = -player_speed() * sin_a
            dy = player_speed() * cos_a
            self.st(dx, dy)
        if keys[pygame.K_LEFT]:
            self.angle -= 0.015
        if keys[pygame.K_RIGHT]:
            self.angle += 0.015

        self.angle %= DOUBLE_PI


class Drawing:
    def __init__(self, sc, sc_map):
        self.sc = sc
        self.sc_map = sc_map
        self.font = pygame.font.SysFont('Areal', 36, bold=True)
        self.texture = {1: pygame.image.load('data/e00.png').convert(),
                        2: pygame.image.load('data/e11.png').convert(),
                        3: pygame.image.load('data/e22.png').convert(),
                        4: pygame.image.load('data/e33.png').convert(),
                        5: pygame.image.load('data/e44.png').convert(),
                        6: pygame.image.load('data/e55.png').convert(),
                        7: pygame.image.load('data/e66.png').convert(),
                        8: pygame.image.load('data/e10.png').convert(),
                        9: pygame.image.load('data/e88.png').convert()
                        }
        global starttime

    def background(self):
        pygame.draw.rect(self.sc, (40, 10, 0), (0, HEIGHT / 2, WIDTH, HEIGHT / 2))
        pygame.draw.rect(self.sc, (20, 20, 20), (0, 0, WIDTH, HEIGHT / 2))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)

    def ray_casting(self, player_pos, player_angle, world_map):
        val = []
        texture_v = 1
        texture_h = 1
        cur_angle = player_angle - FOV / 2
        xo, yo = player_pos
        xm, ym = mapping(xo, yo)
        for ray in range(NUM_RAYS):
            sin_a = math.sin(cur_angle)
            cos_a = math.cos(cur_angle)
            if cos_a >= 0:
                x = xm + TILE
                dx = 1
            else:
                x = xm
                dx = -1
            for i1 in range(0, WORLD_WIDTH, TILE):
                depth_v = (x - xo) / cos_a
                yv = yo + depth_v * sin_a
                tile_v = mapping(x + dx, yv)
                if tile_v in world_map:
                    texture_v = world_map[tile_v]
                    break
                x += dx * TILE

            if sin_a >= 0:
                y = ym + TILE
                dy = 1
            else:
                y = ym
                dy = -1
            for i2 in range(0, WORLD_HEIGHT, TILE):
                depth_h = (y - yo) / sin_a
                xh = xo + depth_h * cos_a
                tile_h = mapping(xh, y + dy)
                if tile_h in world_map:
                    texture_h = world_map[tile_h]
                    break
                y += dy * TILE

            if depth_v < depth_h:
                depth, offset, texture = depth_v, yv, texture_v
            else:
                depth, offset, texture = depth_h, xh, texture_h
            offset = int(offset) % TILE
            depth *= math.cos(player_angle - cur_angle)
            depth = max(depth, 0.00001)
            proj_height = min(int(PROJ_COEFF / depth), 2 * HEIGHT)
            wall_column = self.texture[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
            wall_pos = (ray * SCALE, HEIGHT // 2 - proj_height // 2)
            val.append((depth, wall_column, wall_pos))
            cur_angle += DELTA_ANGLE
        return val

    def fps(self, clock):
        d_fps = str(int(clock.get_fps()))
        rend = self.font.render(d_fps, 0, (0, 150, 0))
        self.sc.blit(rend, FPS_POS)

    def time(self):
        time = int((pygame.time.get_ticks() // 1000)) - int(starttime)
        minut = 0
        while int(time) >= 60:
            minut += 1
            time = int(time) - 60
        if int(time) < 10:
            time = f'0{time}'
        d_time = f'Время прохождения: {minut}. {time}'
        myfont = pygame.font.Font("data/shrift.ttf", 24)
        rend = myfont.render(d_time, 0, (0, 150, 0))
        self.sc.blit(rend, TIME_POS)

    def life(self):
        d_life = f'Осталось {LIFE1} жизни'
        myfont = pygame.font.Font("data/shrift.ttf", 24)
        rend = myfont.render(d_life, 0, (0, 150, 0))
        self.sc.blit(rend, LIFE_POS)

    def mini_map(self, player, mini_map, money_pos):
        global A
        global ANGLE
        g = 1.15
        jk = 2.5
        money = pygame.image.load('data/coi.png').convert_alpha()
        new_money = pygame.transform.scale(money, (8, 8))
        self.sc_map.fill((100, 100, 100))
        map_x, map_y = player.x // MAP_SCALE // 2, player.y // MAP_SCALE // 2
        pygame.draw.circle(self.sc_map, (0, 150, 0), (int(map_x * 1.1), int(map_y * 1.1)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, (50, 0, 0), ((x * 1.15), y * 1.15, MAP_TILE, MAP_TILE))
        s = ((int(map_x) - 5) // 8, (int(map_y) - 5) // 8)
        if s in money_pos:
            pygame.mixer.music.load('data/coin.mp3')
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/coin.mp3'))
            pygame.mixer.Channel(1).set_volume(0.3)
            d = money_pos.index(s)
            del money_pos[d]
            A += 1

        for i in money_pos:
            coin_rect = new_money.get_rect(center=(i[0] * g * 8 + jk, i[1] * g * 8 + jk))
            new_width = round(math.sin(math.radians(ANGLE)) * coin_rect.width)
            ANGLE += 1
            rot_coin = new_money if new_width >= 0 else pygame.transform.flip(new_money, True, False)
            rot_coin = pygame.transform.scale(rot_coin, (abs(new_width), coin_rect.height))
            self.sc_map.blit(rot_coin, rot_coin.get_rect(center=(i[0] * g * 8 + jk, i[1] * g * 8 + jk)))
        self.sc.blit(self.sc_map, MAP_POS)
        a2 = 11
        l = LVL
        lvl = f'lvl: {l}'
        myfont = pygame.font.Font("data/shrift.ttf", 24)
        text = f'Собрано: {A} из {a2}'
        rend1 = myfont.render(lvl, 0, (50, 0, 0))
        rend = myfont.render(text, 0, (50, 0, 0))
        self.sc.blit(rend, (30, HEIGHT - 65))
        self.sc.blit(rend1, (250, HEIGHT - 65))


class Sprites:
    def __init__(self, sprite):
        self.sprite = sprite
        self.sprite_types = {'money': pygame.image.load('data/coi.png').convert_alpha(),
                             'sirenhead': pygame.image.load('data/lol.png').convert_alpha()}

        self.list_of_objects = [SpriteObject(self.sprite_types['sirenhead'], True, (13.50, 11.50), 0.5, 0.8)]
        for i in self.sprite:
            if i != '1':
                self.list_of_objects.append(SpriteObject(self.sprite_types[i[0]], i[1], i[2], i[3], i[4]))
        self.list_of_objects.append(SpriteObject(self.sprite_types['sirenhead'], True, (13.50, 12.50), 0.5, 0.8))


class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static
        self.pas = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.shift = shift
        self.scale = scale

    def object_locate(self, player, walls):
        fake_walls0 = [walls[0] for i in range(FAKE_RAYS)]
        fake_walls1 = [walls[-1] for i in range(FAKE_RAYS)]
        fake_walls = fake_walls0 + walls + fake_walls1

        if not self.static:
            return (False,)

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= NUM_RAYS - 1 + 2 * FAKE_RAYS and distance_to_sprite < fake_walls[fake_ray][0]:
            proj_height = min(int(PROJ_COEFF / distance_to_sprite * self.scale), 2 * HEIGHT)
            proj_height = max(proj_height, 0.00001)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            sprite_pos = (current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)


class Interaction:
    def __init__(self, player, sprites, drawing, walls, obj, text_map):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.walls = walls
        self.obj = obj
        self.side = 20
        self.rect_sirenhead = pygame.Rect(self.obj.x, self.obj.y, 20, 20)
        self.text_map = text_map

    def find_path_step(self, start, target):
        height = len(text_map)
        width = len(text_map[0])
        INF = 1000
        x, y = start
        distance = [[INF] * width for _ in range(height)]
        distance[y][x] = 0
        prev = [[None] * width for _ in range(height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (0, 1), (1, 0), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < width and 0 < next_y < height and not self.text_map[next_y][next_x] and distance[next_y][next_x] == INF:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == INF or start == target:
            return (start[0] * 100 + 50, start[1] * 100 + 50)
        while prev[y][x] != start:
            x, y = prev[y][x]
        return x * 100 + 50, y * 100 + 50



    def npc_move(self):
        return self.find_path_step((round(self.obj.x // 100), round(self.obj.y // 100)), (round(self.player.x // 100), round(self.player.y // 100)))

    def move(self, x, y):
        if x > self.obj.x:
            self.obj.x += 4
        elif x < self.obj.x:
            self.obj.x -= 4
        if x > self.obj.y:
            self.obj.y += 4
        elif x < self.obj.y:
            self.obj.y -= 4

def main():
    list_of_objects = [
        ['money', True, (2.28, 1.67), 1.8, 0.4],
        ['money', True, (5.59, 13.24), 1.8, 0.4],
        ['money', True, (3.53, 15.69), 1.8, 0.4],
        ['money', True, (11.46, 16.60), 1.8, 0.4],
        ['money', True, (20.40, 17.33), 1.8, 0.4],
        ['money', True, (30.68, 6.46), 1.8, 0.4],
        ['money', True, (13.68, 1.64), 1.8, 0.4],
        ['money', True, (23.28, 3.57), 1.8, 0.4],
        ['money', True, (29.47, 15.73), 1.8, 0.4],
        ['money', True, (6.60, 2.57), 1.8, 0.4],
        ['money', True, (20.60, 11.60), 1.8, 0.4]
    ]
    user_text = ''
    posis = [(), (2, 1), (5, 13), (3, 15), (11, 16), (20, 17), (30, 6), (13, 1), (23, 3), (29, 15), (6, 2), (20, 11)]

    pygame.init()
    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('DARK MAZE')
    sc_map = pygame.Surface(MINIMAP_RES)
    clock = pygame.time.Clock()
    sprites = Sprites(list_of_objects)
    sprites2 = Sprites(list_of_objects)
    player = Player(walls1)
    player2 = Player(walls2)
    drawing = Drawing(sc, sc_map)
    interaction = Interaction(player, sprites, drawing, walls1, sprites.list_of_objects[0], text_map)
    interaction2 = Interaction(player, sprites, drawing, walls1, sprites.list_of_objects[-1], text_map)
    interaction_2 = Interaction(player2, sprites2, drawing, walls2, sprites.list_of_objects[0], text_map2)
    interaction2_2 = Interaction(player2, sprites2, drawing, walls2, sprites.list_of_objects[-1], text_map2)
    ENEMY_EVENT_TYPE = 30
    delay = 50
    pygame.time.set_timer(ENEMY_EVENT_TYPE, delay)
    pygame.mixer.init()
    pygame.font.init()
    f = pygame.font.Font("data/shrift.ttf", 130)
    pygame.mixer.music.load("data/music2.mp3")
    pygame.mixer.Channel(0).play(pygame.mixer.Sound("data/music2.mp3"), -1)
    # pygame.mixer.Channel(2).play(pygame.mixer.Sound("data/priexal.mp3"))
    vol = 0.5
    pygame.mixer.Channel(0).set_volume(vol)
    fon = pygame.image.load('data/meny.png').convert()
    fom = pygame.transform.scale(fon, (1200, 800))
    fon2 = pygame.image.load('data/meny2.png').convert()
    fom2 = pygame.transform.scale(fon2, (1200, 800))
    fon3 = pygame.image.load('data/meny3.png').convert()
    fom3 = pygame.transform.scale(fon3, (1200, 800))
    image = pygame.image.load('data/arrow.png').convert_alpha()
    image = pygame.transform.scale(image, (25, 25))
    pygame.mixer.Channel(0).set_volume(vol)
    pygame.mouse.set_visible(False)
    star = pygame.image.load('data/star.png').convert_alpha()
    star2 = pygame.image.load('data/star2.png').convert_alpha()
    star_01 = pygame.transform.scale(star, (50, 50))
    star_02 = pygame.transform.scale(star2, (50, 50))
    star_03 = pygame.transform.scale(star, (23, 23))
    drav2 = False
    true = True
    sd = [(410, 550), (480, 550), (550, 550), (620, 550), (690, 550)]
    fh = [(110, 12), (140, 12), (170, 12), (200, 12), (230, 12)]
    with open('star.txt', 'r', encoding="utf-8") as d:
        fd = ''.join(d.readlines())
        if len(fd) > 0:
            fg = []
            for z in fd:
                fg.append(int(z))
            df = round(sum(fg) / len(fg))
        else:
            df = 0
    # pygame.mixer.Channel(2).set_volume(0.5)

    FLAG_1 = True
    FLAG_2 = False
    FLAG_3 = False
    FLAG_4 = False
    FLAG_5 = False
    FLAG_6 = False
    FLAG_7 = False
    FLAG_8 = False
    FLAG_9 = False
    global A
    global LVL
    global g
    global starttime
    k = 1
    x, y = 0, 0

    while True:

        if FLAG_1:
            sc.blit(fom, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if vol < 0:
                    vol = 0.0
                if vol > 1:
                    vol = 1.0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_DOWN:
                        vol -= 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                    if event.key == pygame.K_UP:
                        vol += 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x <= 678 and x >= 523 and y <= 418 and y >= 275:
                        FLAG_1 = False
                        if user_text == '':
                            FLAG_3 = True
                        else:
                            FLAG_4 = True
                    if x <= 1187 and x >= 1068 and y <= 124 and y >= 8:
                        FLAG_1 = False
                        FLAG_2 = True
                if event.type == pygame.MOUSEMOTION:
                    sc.blit(image, event.pos)
                    x, y = event.pos
            if x != 0 and y != 0:
                sc.blit(image, (x, y))
            pygame.display.flip()

        if FLAG_2:
            sc.blit(fom2, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if vol < 0:
                    vol = 0.0
                if vol > 1:
                    vol = 1.0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_DOWN:
                        vol -= 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                    if event.key == pygame.K_UP:
                        vol += 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x <= 1187 and x >= 1068 and y <= 124 and y >= 8:
                        FLAG_2 = False
                        if user_text == '':
                            FLAG_1 = True
                        else:
                            FLAG_3 = True
                            user_text = ''
                if event.type == pygame.MOUSEMOTION:
                    sc.blit(image, event.pos)
                    x, y = event.pos
            if x != 0 and y != 0:
                sc.blit(image, (x, y))
            pygame.display.flip()

        if FLAG_3:
            sc.blit(fom3, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if vol < 0:
                    vol = 0.0
                if vol > 1:
                    vol = 1.0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_DOWN:
                        vol -= 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                    if event.key == pygame.K_UP:
                        vol += 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    # print(x, y)
                    if x <= 678 and x >= 523 and y <= 418 and y >= 275:
                        FLAG_3 = False
                        if user_text != '':
                            global LVL1
                            a = 'game.db'
                            con = sqlite3.connect(a)
                            cur = con.cursor()
                            if str(cur.execute(
                                    f'''select name from game_db where name = "{user_text}"''').fetchall()) != '[]':
                                starttime = pygame.time.get_ticks() // 1000
                                FLAG_4 = True
                            else:
                                with con:
                                    cur.execute(f'''INSERT INTO game_db(name, lvl1, lvl2)
                                     VALUES('{user_text}', '', '')''')
                                starttime = pygame.time.get_ticks() // 1000
                                FLAG_4 = True
                            con.close()


                        else:
                            FLAG_1 = True
                    if x <= 1187 and x >= 1068 and y <= 124 and y >= 8:
                        FLAG_2 = True
                        FLAG_3 = False
                if event.type == pygame.MOUSEMOTION:
                    sc.blit(image, event.pos)
                    x, y = event.pos

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    if len(user_text) < 7:
                        if event.key == pygame.K_a:
                            user_text += 'a'
                        if event.key == pygame.K_b:
                            user_text += 'b'
                        if event.key == pygame.K_c:
                            user_text += 'c'
                        if event.key == pygame.K_d:
                            user_text += 'd'
                        if event.key == pygame.K_e:
                            user_text += 'e'
                        if event.key == pygame.K_f:
                            user_text += 'f'
                        if event.key == pygame.K_g:
                            user_text += 'g'
                        if event.key == pygame.K_h:
                            user_text += 'h'
                        if event.key == pygame.K_i:
                            user_text += 'i'
                        if event.key == pygame.K_j:
                            user_text += 'j'
                        if event.key == pygame.K_k:
                            user_text += 'k'
                        if event.key == pygame.K_l:
                            user_text += 'l'
                        if event.key == pygame.K_m:
                            user_text += 'm'
                        if event.key == pygame.K_n:
                            user_text += 'n'
                        if event.key == pygame.K_o:
                            user_text += 'o'
                        if event.key == pygame.K_p:
                            user_text += 'p'
                        if event.key == pygame.K_q:
                            user_text += 'q'
                        if event.key == pygame.K_r:
                            user_text += 'r'
                        if event.key == pygame.K_s:
                            user_text += 's'
                        if event.key == pygame.K_t:
                            user_text += 't'
                        if event.key == pygame.K_u:
                            user_text += 'u'
                        if event.key == pygame.K_v:
                            user_text += 'v'
                        if event.key == pygame.K_w:
                            user_text += 'w'
                        if event.key == pygame.K_x:
                            user_text += 'x'
                        if event.key == pygame.K_y:
                            user_text += 'y'
                        if event.key == pygame.K_z:
                            user_text += 'z'
                        if event.key == pygame.K_KP0:
                            user_text += '0'
                        if event.key == pygame.K_KP1:
                            user_text += '1'
                        if event.key == pygame.K_KP2:
                            user_text += '2'
                        if event.key == pygame.K_KP3:
                            user_text += '3'
                        if event.key == pygame.K_KP4:
                            user_text += '4'
                        if event.key == pygame.K_KP5:
                            user_text += '5'
                        if event.key == pygame.K_KP6:
                            user_text += '6'
                        if event.key == pygame.K_KP7:
                            user_text += '7'
                        if event.key == pygame.K_KP8:
                            user_text += '8'
                        if event.key == pygame.K_KP9:
                            user_text += '9'
                        if event.key == pygame.K_0:
                            user_text += '0'
                        if event.key == pygame.K_1:
                            user_text += '1'
                        if event.key == pygame.K_2:
                            user_text += '2'
                        if event.key == pygame.K_3:
                            user_text += '3'
                        if event.key == pygame.K_4:
                            user_text += '4'
                        if event.key == pygame.K_5:
                            user_text += '5'
                        if event.key == pygame.K_6:
                            user_text += '6'
                        if event.key == pygame.K_7:
                            user_text += '7'
                        if event.key == pygame.K_8:
                            user_text += '8'
                        if event.key == pygame.K_9:
                            user_text += '9'

            d_name = f'Введите своё имя'
            myfont = pygame.font.Font("data/shrift.ttf", 50)
            rend = myfont.render(d_name, 0, (180, 180, 180))
            sc.blit(rend, (420, 200))

            st_text = f.render(user_text, 0, (94, 138, 14))
            sc.blit(st_text, (321, 440))
            if x != 0 and y != 0:
                sc.blit(image, (x, y))
            pygame.display.flip()


        if FLAG_4:
            next_pos = sprites.list_of_objects[0].pas
            next_pos2 = sprites.list_of_objects[-1].pas
            # per = schedule.every(1).seconds.do(time)
            # schedule.cancel_job(per)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if vol < 0:
                    vol = 0.0
                if vol > 1:
                    vol = 1.0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        vol -= 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                    if event.key == pygame.K_UP:
                        vol += 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())

                elif event.type == ENEMY_EVENT_TYPE:
                    next_pos = interaction.npc_move()
                    next_pos2 = interaction2.npc_move()

            if (sprites.list_of_objects[0].x, sprites.list_of_objects[0].y) != next_pos:
                if next_pos[0] > sprites.list_of_objects[0].x:
                    sprites.list_of_objects[0].x += 5
                elif next_pos[0] < sprites.list_of_objects[0].x:
                    sprites.list_of_objects[0].x -= 5
                else:
                    pass
                if next_pos[1] > sprites.list_of_objects[0].y:
                    sprites.list_of_objects[0].y += 5
                elif next_pos[1] < sprites.list_of_objects[0].y:
                    sprites.list_of_objects[0].y -= 5

            if (sprites.list_of_objects[-1].x, sprites.list_of_objects[-1].y) != next_pos2:
                if next_pos2[0] > sprites.list_of_objects[-1].x:
                    sprites.list_of_objects[-1].x += 5
                elif next_pos2[0] < sprites.list_of_objects[-1].x:
                    sprites.list_of_objects[-1].x -= 5
                else:
                    pass
                if next_pos2[1] > sprites.list_of_objects[-1].y:
                    sprites.list_of_objects[-1].y += 5
                elif next_pos2[1] < sprites.list_of_objects[-1].y:
                    sprites.list_of_objects[-1].y -= 5


            player.movement()
            sc.fill((0, 0, 0))

            # print(player.pos()[0] / TILE, player.pos()[1] / TILE)

            x_new = int(player.x / TILE)
            y_new = int(player.y / TILE)

            drawing.background()
            walls = drawing.ray_casting((int(player.x), int(player.y)), player.angle, world_map)
            drawing.world(walls + [obj.object_locate(player, walls) for obj in sprites.list_of_objects if obj != 1])
            drawing.fps(clock)
            drawing.time()
            drawing.mini_map(player, mini_map, MOMEY_MINI)

            drawing.life()
            clock.tick(80)

            pygame.display.flip()
            clock.tick()

            if (x_new, y_new) in posis:
                s = posis.index((x_new, y_new))
                sprites.list_of_objects[s] = 1

            if x_new == 13 and y_new == 14 and A == 1:
                FLAG_4 = False
                minut = 0
                bestminut = 0
                FLAG_5 = True
                timelvl1 = int((pygame.time.get_ticks() // 1000)) - int(starttime)
                A = 10
                LVL = 2

        if FLAG_5:
            sc.fill((0, 0, 0))
            a = 'game.db'
            con = sqlite3.connect(a)
            cur = con.cursor()
            result = cur.execute(f"""SELECT lvl1 FROM game_db
                        WHERE name = '{user_text}'""").fetchall()
            if result[0][0] == '':
                with con:
                    cur.execute(f'''UPDATE game_db
                    SET lvl1 = {timelvl1}
                    WHERE name = "{user_text}"''')
            elif int(result[0][0]) > timelvl1:
                with con:
                    cur.execute(f'''UPDATE game_db
                    SET lvl1 = {timelvl1}
                    WHERE name = "{user_text}"''')

            result1 = cur.execute(f"""SELECT lvl1 FROM game_db""").fetchall()
            sp = []
            for element in result1:
                if element[0] != '':
                    sp.append(element[0])
            best = min(sp)
            bestname = cur.execute(f"""SELECT name FROM game_db WHERE lvl1 = {best}""").fetchall()
            # print(best, bestname[0][0])
            con.close()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if vol < 0:
                    vol = 0.0
                if vol > 1:
                    vol = 1.0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_DOWN:
                        vol -= 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                    if event.key == pygame.K_UP:
                        vol += 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                if event.type == pygame.MOUSEMOTION:
                    sc.blit(image, event.pos)
                    x, y = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if k == 1:
                        FLAG_5 = False
                        FLAG_6 = True
            while int(timelvl1) >= 60:
                minut += 1
                timelvl1 = int(timelvl1) - 60
                if int(timelvl1) < 10:
                    timelvl1 = f'0{timelvl1}'
            while int(best) >= 60:
                bestminut += 1
                best = int(best) - 60

            d_time = f'Время прохождения: {minut} мин {timelvl1} сек'
            myfont = pygame.font.Font("data/shrift.ttf", 24)
            rend = myfont.render(d_time, 0, (255, 0, 0))
            sc.blit(rend, (430, 500))
            d_besttime = f'Лучший результат:'
            d_besttime1 = f'{bestname[0][0]} {bestminut} мин {best} сек'
            rend1 = myfont.render(d_besttime, 0, (0, 150, 0))
            rend2 = myfont.render(d_besttime1, 0, (0, 150, 0))
            sc.blit(rend1, (500, 550))
            sc.blit(rend2, (520, 600))
            st_text = f.render('ВЫ ПРОШЛИ 1 LVL', 0, (255, 0, 0))
            sc.blit(st_text, (100, 320))
            if x != 0 and y != 0:
                sc.blit(image, (x, y))
            pygame.display.flip()

        if FLAG_6:
            sc.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if vol < 0:
                    vol = 0.0
                if vol > 1:
                    vol = 1.0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_DOWN:
                        vol -= 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                    if event.key == pygame.K_UP:
                        vol += 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                if event.type == pygame.MOUSEMOTION:
                    sc.blit(image, event.pos)
                    x, y = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    FLAG_6 = False
                    starttime = pygame.time.get_ticks() // 1000
                    FLAG_7 = True
            st_text = f.render('LEVAL 2', 0, (255, 0, 0))
            sc.blit(st_text, (380, 330))
            if x != 0 and y != 0:
                sc.blit(image, (x, y))

            pygame.display.flip()

        if FLAG_7:
            sprites2.list_of_objects[0].x, sprites2.list_of_objects[0].y = 1350, 1150
            sprites2.list_of_objects[-1].x, sprites2.list_of_objects[-1].y = 1350, 1250
            next_pos_2 = (sprites2.list_of_objects[0].x, sprites2.list_of_objects[0].y)
            next_pos2_2 = (sprites2.list_of_objects[-1].x, sprites2.list_of_objects[-1].y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if vol < 0:
                    vol = 0.0
                if vol > 1:
                    vol = 1.0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        vol -= 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                    if event.key == pygame.K_UP:
                        vol += 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())

                elif event.type == ENEMY_EVENT_TYPE:
                    next_pos_2 = interaction_2.npc_move()
                    next_pos2_2 = interaction2_2.npc_move()
                    print(next_pos, next_pos2)

            if (sprites2.list_of_objects[0].x, sprites2.list_of_objects[0].y) != next_pos_2:
                if next_pos_2[0] > sprites2.list_of_objects[0].x:
                    sprites2.list_of_objects[0].x += 5
                elif next_pos_2[0] < sprites2.list_of_objects[0].x:
                    sprites2.list_of_objects[0].x -= 5
                else:
                    pass
                if next_pos_2[1] > sprites2.list_of_objects[0].y:
                    sprites2.list_of_objects[0].y += 5
                elif next_pos_2[1] < sprites2.list_of_objects[0].y:
                    sprites2.list_of_objects[0].y -= 5
            else:
                print(1)

            if (sprites2.list_of_objects[-1].x, sprites2.list_of_objects[-1].y) != next_pos2_2:
                if next_pos2_2[0] > sprites2.list_of_objects[-1].x:
                    sprites2.list_of_objects[-1].x += 5
                elif next_pos2_2[0] < sprites2.list_of_objects[-1].x:
                    sprites2.list_of_objects[-1].x -= 5
                else:
                    pass
                if next_pos2_2[1] > sprites2.list_of_objects[-1].y:
                    sprites2.list_of_objects[-1].y += 5
                elif next_pos2_2[1] < sprites2.list_of_objects[-1].y:
                    sprites2.list_of_objects[-1].y -= 5
            else:
                print(2)

            player2.movement()
            sc.fill((0, 0, 0))

            # print(player.pos()[0] / TILE, player.pos()[1] / TILE)

            x_new = int(player2.x / TILE)
            y_new = int(player2.y / TILE)

            drawing.background()
            walls = drawing.ray_casting((int(player2.x), int(player2.y)), player2.angle, world_map2)
            drawing.world(walls + [obj.object_locate(player2, walls) for obj in sprites2.list_of_objects if obj != 1])
            drawing.fps(clock)
            drawing.time()
            drawing.mini_map(player2, mini_map2, MOMEY_MINI2)

            drawing.life()
            clock.tick(60)

            pygame.display.flip()
            clock.tick()

            if (x_new, y_new) in posis:
                s = posis.index((x_new, y_new))
                sprites2.list_of_objects[s] = 1
            if x_new == 13 and y_new == 14 and A == 11:
                FLAG_7 = False
                minut = 0
                FLAG_8 = True
                timelvl2 = int((pygame.time.get_ticks() // 1000)) - int(starttime)
                A = 10

        if FLAG_8:
            sc.fill((0, 0, 0))
            a = 'game.db'
            con = sqlite3.connect(a)
            cur = con.cursor()
            result = cur.execute(f"""SELECT lvl2 FROM game_db
                        WHERE name = '{user_text}'""").fetchall()
            if result[0][0] == '':
                with con:
                    cur.execute(f'''UPDATE game_db
                    SET lvl2 = {timelvl2}
                    WHERE name = "{user_text}"''')
            elif result[0][0] > timelvl2:
                with con:
                    cur.execute(f'''UPDATE game_db
                    SET lvl2 = {timelvl2}
                    WHERE name = "{user_text}"''')

            result1 = cur.execute(f"""SELECT lvl2 FROM game_db""").fetchall()
            sp = []
            for element in result1:
                if element[0] != '':
                    sp.append(element[0])
            best = min(sp)
            bestname = cur.execute(f"""SELECT name FROM game_db WHERE lvl2 = {best}""").fetchall()
            # print(best, bestname[0][0])
            con.close()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if vol < 0:
                    vol = 0.0
                if vol > 1:
                    vol = 1.0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_DOWN:
                        vol -= 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                    if event.key == pygame.K_UP:
                        vol += 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                if event.type == pygame.MOUSEMOTION:
                    sc.blit(image, event.pos)
                    x, y = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                        FLAG_8 = False
                        FLAG_9 = True
            while int(timelvl2) >= 60:
                minut += 1
                timelvl2 = int(timelvl2) - 60
                if int(timelvl2) < 10:
                    timelvl2 = f'0{timelvl2}'
            d_time = f'Время прохождения: {minut} мин {timelvl2} сек'
            myfont = pygame.font.Font("data/shrift.ttf", 24)
            rend = myfont.render(d_time, 0, (0, 150, 0))
            sc.blit(rend, (450, 500))
            d_besttime = f'Лучший результат:'
            d_besttime1 = f'{bestname[0][0]} {bestminut} мин {best} сек'
            rend1 = myfont.render(d_besttime, 0, (0, 150, 0))
            rend2 = myfont.render(d_besttime1, 0, (0, 150, 0))
            sc.blit(rend1, (500, 550))
            sc.blit(rend2, (520, 600))
            st_text = f.render('ВЫ ПРОШЛИ 2 LVL', 0, (255, 0, 0))
            sc.blit(st_text, (100, 330))
            if x != 0 and y != 0:
                sc.blit(image, (x, y))

            pygame.display.flip()

        if FLAG_9:
            sc.fill((0, 0, 0))
            for i in sd:
                sc.blit(star_02, i)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open('star.txt', 'a', encoding="utf-8") as f:
                        if g > 0:
                            f.write(f'{str(g)}')
                    exit()
                if vol < 0:
                    vol = 0.0
                if vol > 1:
                    vol = 1.0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        with open('star.txt', 'a', encoding="utf-8") as f:
                            if g > 0:
                                f.write(f'{str(g)}')
                        exit()
                    if event.key == pygame.K_DOWN:
                        vol -= 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                    if event.key == pygame.K_UP:
                        vol += 0.1
                        pygame.mixer.Channel(0).set_volume(vol)
                        # print(pygame.mixer.music.get_volume())
                if event.type == pygame.MOUSEMOTION:
                    sc.blit(image, event.pos)
                    x, y = event.pos
                    if true:
                        if x <= 460 and x >= 410 and y <= 600 and y >= 550:
                            g = 1
                            drav2 = True
                        elif x <= 530 and x >= 410 and y <= 600 and y >= 550:
                            g = 2
                            drav2 = True
                        elif x <= 600 and x >= 410 and y <= 600 and y >= 550:
                            g = 3
                            drav2 = True
                        elif x <= 670 and x >= 410 and y <= 600 and y >= 550:
                            g = 4
                            drav2 = True
                        elif x <= 740 and x >= 410 and y <= 600 and y >= 550:
                            g = 5
                            drav2 = True
                        else:
                            g = 0
                            drav2 = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if x <= 750 and x >= 420 and y <= 600 and y >= 550:
                        true = False
            if drav2:
                for j in sd[:g]:
                    sc.blit(star_01, j)

            st_text = f.render('КОНЕЦ', 0, (255, 0, 0))
            sc.blit(st_text, (390, 300))
            d_time = f'поддержка автора: 89645211748(тинькофф)'
            myfont = pygame.font.Font("data/shrift.ttf", 24)
            stars = pygame.font.Font("data/shrift.ttf", 24)
            ret = pygame.font.Font("data/shrift.ttf", 24)
            r = ret.render(f'рейтинг', 0, (0, 150, 0))
            st = stars.render('как вам игра?', 0, (0, 150, 0))
            rend = myfont.render(d_time, 0, (0, 150, 0))
            sc.blit(rend, (350, 440))
            sc.blit(st, (500, 490))
            sc.blit(r, (10, 10))
            if x != 0 and y != 0:
                sc.blit(image, (x, y))
            for o in fh[:df]:
                sc.blit(star_03, o)

            pygame.display.flip()


if __name__ == '__main__':
    main()