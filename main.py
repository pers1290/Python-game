import pygame
import math
import copy

# игровые настройки
WIDTH = 1200
HEIGHT = 800
FPS = 60
TILE = 100
FPS_POS = (WIDTH - 65, 5)
SENSETIV = 0.004

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
player_pos = (1350, 1450)
player_angle = 300

# спрайты
DOUBLE_PI = 2 * math.pi
CENTER_RAY = NUM_RAYS // 2 - 1


def player_speed():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
        return 3.1
    else:
        return 1.6


# карта
_ = False
text_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 5, 1],
    [1, _, _, _, 1, 1, 1, 1, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 2, _, _, 3, _, _, _, _, 6, _, 1, _, 1, 2, 1, 1, 1, _, 5, 3, 1, 1, 1, _, 1, 1, 1, 1, 1, _, 1],
    [1, _, 7, _, _, 1, _, 6, 6, _, 1, _, 1, _, 1, _, _, _, _, 1, 1, _, _, _, 1, _, _, _, _, _, 1, _, 1],
    [1, _, 1, _, _, 1, _, 6, 6, _, _, _, 1, _, 1, _, 1, 7, _, _, _, _, 1, _, _, _, _, 5, 6, _, 1, _, 3],
    [1, _, 1, _, _, 1, _, 6, 6, _, 7, _, 1, _, 1, _, 7, 7, 1, 1, 1, _, 1, _, 1, 1, _, 1, 1, _, 1, _, 6],
    [1, _, 9, _, _, 1, _, _, _, _, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, 1, 7, _, _, 1, _, _, _, 6],
    [1, _, 1, _, _, 1, 2, 1, 1, 1, 1, _, 1, _, _, _, 1, 1, _, 1, _, 1, 1, 1, 1, _, _, _, 1, _, 1, _, 6],
    [1, _, 1, _, _, _, _, 1, 7, 7, _, _, 1, 5, 1, 1, 1, 1, _, 1, _, _, 7, _, _, _, _, 1, 1, _, 1, _, 6],
    [1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1, 1, _, 7, 1, 1, 1, _, _, _, _, 9, _, 6],
    [1, _, 1, _, 1, _, 5, _, 9, 1, 1, 1, 1, _, 1, _, _, 1, _, 1, _, _, _, _, _, _, _, _, 1, _, 1, _, 4],
    [1, _, _, _, 1, _, 5, _, 0, _, _, _, 1, _, 1, 1, _, 1, _, 1, _, 1, _, _, _, 1, 1, 1, 1, 1, 6, _, 1],
    [1, _, 6, _, 5, _, 5, _, 1, _, 1, _, 1, _, 7, 1, _, 6, _, 1, 4, 1, _, 7, _, 1, _, _, _, _, 1, _, 7],
    [1, _, 1, _, 1, _, _, _, 1, _, _, 1, 8, _, 8, 1, _, 7, _, 4, _, 1, 1, 1, 1, 7, _, 6, 6, _, 1, _, 1],
    [1, _, 1, _, 1, 1, 1, 1, 1, _, _, 1, 8, _, 8, 1, _, 1, _, _, _, _, _, _, _, _, _, 6, 6, _, 1, _, 1],
    [1, _, 1, _, _, _, _, _, _, _, _, 1, 8, 8, 8, 6, _, 5, 1, 9, 1, 1, 1, 1, 1, 1, _, _, _, _, 1, _, 1],
    [1, _, 1, 1, 1, 1, 4, 1, 1, _, 6, _, 1, 1, 1, 7, _, _, _, _, _, _, _, _, _, 1, 4, 1, 6, 1, 9, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, 1, _, _, 4, 3, _, _, _, _, _, _, _, _, 1],
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


def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.side = 50
        self.rect1 = pygame.Rect(*player_pos, self.side, self.side)

    def pos(self):
        return self.x, self.y

    def st(self, dx, dy):
        next_r = self.rect1.copy()
        next_r.move_ip(dx, dy)
        hit = next_r.collidelistall(walls1)

        if len(hit):
            del_x = 0
            del_y = 0
            for i in hit:
                rect2 = walls1[i]
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


class Sprites:
    def __init__(self):
        self.sprite_types = {
            'lol': pygame.image.load('data/lol.png').convert_alpha()
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_types['lol'], True, (7.1, 2.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['lol'], True, (7.1, 2.1), 1.8, 0.4)
        ]


class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static
        self.pas = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.shift = shift
        self.scale = scale

    def object_locate(self, player, walls):
        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)


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

    def background(self):
        pygame.draw.rect(self.sc, (40, 10, 0), (0, HEIGHT / 2, WIDTH, HEIGHT / 2))
        pygame.draw.rect(self.sc, (20, 20, 20), (0, 0, WIDTH, HEIGHT / 2))

    def ray_casting(self, player_pos, player_angle, sc):
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
            sc.blit(wall_column, (ray * SCALE, HEIGHT // 2 - proj_height // 2))
            cur_angle += DELTA_ANGLE

    def fps(self, clock):
        d_fps = str(int(clock.get_fps()))
        rend = self.font.render(d_fps, 0, (0, 150, 0))
        self.sc.blit(rend, FPS_POS)

    def mini_map(self, player):
        self.sc_map.fill((100, 100, 100))
        map_x, map_y = player.x // MAP_SCALE // 2, player.y // MAP_SCALE // 2
        pygame.draw.circle(self.sc_map, (0, 150, 0), (int(map_x * 1.1), int(map_y * 1.1)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, (50, 0, 0), ((x * 1.15), y * 1.15, MAP_TILE, MAP_TILE))
        self.sc.blit(self.sc_map, MAP_POS)
        a = 0
        a1 = 5
        l = 1
        lvl = f'lvl: {l}'
        text = f'Собрано: {a} /{a1}'
        rend1 = self.font.render(lvl, 0, (50, 0, 0))
        rend = self.font.render(text, 0, (50, 0, 0))
        self.sc.blit(rend, (30, HEIGHT - 65))
        self.sc.blit(rend1, (250, HEIGHT - 65))


def main():
    pygame.init()
    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    sc_map = pygame.Surface(MINIMAP_RES)
    clock = pygame.time.Clock()
    player = Player()
    drawing = Drawing(sc, sc_map)
    pygame.mouse.set_visible(False)
    pygame.mixer.init()
    pygame.mixer.music.load("data/music2.mp3")
    pygame.mixer.music.play(-1, 0.0)
    vol = 0.2
    pygame.mixer.music.set_volume(vol)

    while True:

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
                    pygame.mixer.music.set_volume(vol)
                if event.key == pygame.K_UP:
                    vol += 0.1
                    pygame.mixer.music.set_volume(vol)

        sc.fill((0, 0, 0))
        player.movement()

        # print(player.pos()[0] / TILE, player.pos()[1] / TILE)

        drawing.background()
        drawing.ray_casting((int(player.x), int(player.y)), player.angle, sc)
        drawing.fps(clock)
        drawing.mini_map(player)

        pygame.display.flip()
        clock.tick()


if __name__ == '__main__':
    main()
