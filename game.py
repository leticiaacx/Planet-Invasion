import random
import math
# ---------------- CONSTANTES ----------------------------

# Constantes de tiles
TILE_SIZE = 64
ROWS = 15
COLS = 30

# Definir o tamanho e nome da janela
WIDTH = TILE_SIZE * COLS
HEIGHT = TILE_SIZE * ROWS
TITLE = "Planet Invasion"

# Constantes da fisica do jogo
GRAVITY = 0.5
Y_SPEED_START = 0
X_SPEED_START = 0
JUMP_FORCE = -15
X_SPEED = 5

# Constantes de animacao
HERO_IDLE_SPEED = 0.1
HERO_WALK_SPEED = 0.1

BARNACLE_ATTACK_SPEED = 0.2

BEE_WALK_SPEED = 2
BEE_WALK_ANIMATION_SPEED = 0.15

SLIMEFIRE_WALK_SPEED = 2
SLIMEFIRE_WALK_ANIMATION_SPEED = 0.1

FROG_WALK_SPEED = 1.5
FROG_WALK_ANIMATION_SPEED = 0.15

SNAIL_WALK_SPEED = 0.3
SNAIL_WALK_ANIMATION_SPEED = 0.2

SAW_ROTATION_SPEED = 0.1

# Constantes do objetivo
GOAL_ANIMATION_SPEED = 0.1

# Musica do jogo
BACKGROUND_MUSIC = "happy_adveture"

# Constantes de posicao inicial
HERO_START_POSITION = TILE_SIZE * 2, HEIGHT - (TILE_SIZE * 3)

# Estados do jogo
GAME_STATE = "MENU"
SOUND_ON = True
WINNER_STATE = "WINNER"
GAME_OVER_STATE = "GAME_OVER"

# Sistema de vidas e pontuacao
MAX_LIVES = 5
CURRENT_LIVES = MAX_LIVES
SCORE = 0
POINTS_PER_STAGE = 100
CURRENT_STAGE = 1
TOTAL_STAGES = 4

# Definicao dos botoes do menu
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 80
BUTTON_SPACING = 30

MENU_CENTER_X = WIDTH // 2
MENU_TOP_Y = HEIGHT // 2 - (BUTTON_HEIGHT * 3 + BUTTON_SPACING * 2) // 2

button_start = Rect(
    (MENU_CENTER_X - BUTTON_WIDTH // 2, MENU_TOP_Y), (BUTTON_WIDTH, BUTTON_HEIGHT)
)

button_sound = Rect(
    (MENU_CENTER_X - BUTTON_WIDTH // 2, MENU_TOP_Y + BUTTON_HEIGHT + BUTTON_SPACING),
    (BUTTON_WIDTH, BUTTON_HEIGHT),
)

button_exit = Rect(
    (
        MENU_CENTER_X - BUTTON_WIDTH // 2,
        MENU_TOP_Y + 2 * (BUTTON_HEIGHT + BUTTON_SPACING),
    ),
    (BUTTON_WIDTH, BUTTON_HEIGHT),
)

# --------------------------------------------------------

# ---------- CRIANDO LISTAS DE IMAGENS PARA ANIMACAO ----------


def animation_images_list(actor, animation, list_size):
    images_list = []
    for i in range(list_size):
        images_list.append(f"{actor}_{animation}_{i}")
    return images_list


hero_idle_images = animation_images_list("hero", "idle", 18)
hero_walk_right_images = animation_images_list("hero", "walk_right", 2)
hero_walk_left_images = animation_images_list("hero", "walk_left", 2)
barnacle_attack_images = animation_images_list("barnacle", "attack", 4)
bee_walk_right_images = animation_images_list("bee", "walkright", 2)
bee_walk_left_images = animation_images_list("bee", "walkleft", 2)
slimefire_walk_right_images = animation_images_list("slimefire", "walkright", 2)
slimefire_walk_left_images = animation_images_list("slimefire", "walkleft", 2)
goal_images = animation_images_list("goal", "animation", 2)
frog_idle_images = ["frog_idle"]
frog_jump_images = ["frog_jump"]
snail_walk_images = ["snail_walk_a", "snail_walk_b"]

# ----------------------------------------------------------------

# ___________ CRIANDO CLASSES HERO E ENEMY _______________


class Hero:
    def __init__(self, start_pos):
        self.actor = Actor("hero_idle_1")
        self.actor.pos = start_pos
        self.vx = X_SPEED_START
        self.vy = Y_SPEED_START
        self.idle_images = hero_idle_images
        self.walk_right_images = hero_walk_right_images
        self.walk_left_images = hero_walk_left_images
        self.idle_frame = 0
        self.walk_frame = 0
        self.animation_counter = 0

    def reset_position(self):
        self.actor.pos = HERO_START_POSITION
        self.vx = X_SPEED_START
        self.vy = Y_SPEED_START

    def apply_gravity(self):
        self.vy += GRAVITY
        self.actor.y += self.vy

    def jump(self, on_platform):
        if on_platform:
            self.vy = JUMP_FORCE
            if SOUND_ON:
                try:
                    sounds.jump.play()
                except:
                    pass

    def move_horizontal(self):
        self.vx = 0
        if keyboard.left:
            self.vx = -X_SPEED
        if keyboard.right:
            self.vx = X_SPEED
        self.actor.x += self.vx

    def clamp_to_screen(self):
        if self.actor.left < 0:
            self.actor.left = 0
        if self.actor.right > WIDTH:
            self.actor.right = WIDTH

    def animate(self):
        self.animation_counter += 1
        # Animação durante o pulo/queda
        if self.vy != 0:
            if self.vx > 0:
                self.actor.image = self.walk_right_images[0]
            elif self.vx < 0:
                self.actor.image = self.walk_left_images[0]
            else:
                self.actor.image = self.idle_images[0]
        # Animação parado
        elif self.vx == 0:
            if self.animation_counter % int(HERO_IDLE_SPEED * 60) == 0:
                self.idle_frame = (self.idle_frame + 1) % len(self.idle_images)
                self.actor.image = self.idle_images[self.idle_frame]
        # Animação andando
        else:
            if self.animation_counter % int(HERO_WALK_SPEED * 60) == 0:
                self.walk_frame = (self.walk_frame + 1) % len(self.walk_right_images)
                if self.vx > 0:
                    self.actor.image = self.walk_right_images[self.walk_frame]
                else:
                    self.actor.image = self.walk_left_images[self.walk_frame]
    def draw(self):
        self.actor.draw()

    def colliderect(self, other):
        return self.actor.colliderect(other)


class Enemy:
    def __init__(
        self, images_left, images_right, x, y, vx, enemy_type="generic", patrol_range=3
    ):
        self.images_left = images_left
        self.images_right = images_right
        self.actor = Actor(images_left[0])
        self.actor.x = x
        self.actor.bottom = y  # CORRIGIDO: Usar bottom para posicionar na plataforma
        self.vx = vx
        self.frame = 0
        self.animation_counter = 0
        self.enemy_type = enemy_type
        self.start_x = x
        self.patrol_range = patrol_range * TILE_SIZE
        self.min_x = x - self.patrol_range
        self.max_x = x + self.patrol_range

    def update_movement(self):
        self.actor.x += self.vx
        if self.actor.x < self.min_x or self.actor.x > self.max_x:
            self.vx = -self.vx

    def animate(self, speed=15):
        self.animation_counter += 1
        if self.animation_counter % speed == 0:
            self.frame = (self.frame + 1) % len(self.images_left)
            if self.vx > 0:
                self.actor.image = self.images_right[self.frame]

            else:
                self.actor.image = self.images_left[self.frame]

    def draw(self):
        self.actor.draw()

    def colliderect(self, other):
        return self.actor.colliderect(other)


class StaticEnemy:
    def __init__(self, image_list, x, y):
        self.images = image_list
        self.actor = Actor(image_list[0])
        self.actor.x = x
        self.actor.bottom = y  # CORRIGIDO: Usar bottom para posicionar na plataforma
        self.frame = 0

    def animate(self):
        pass  # Animacao controlada globalmente

    def draw(self):
        self.actor.draw()

    def colliderect(self, other):
        return self.actor.colliderect(other)


class JumpingFrog:
    """Sapo que salta para frente e para tras"""
    def __init__(self, x, y, vx, patrol_range=3):
        self.idle_image = "frog_idle"
        self.jump_image = "frog_jump"
        self.actor = Actor(self.idle_image)
        self.actor.x = x
        self.actor.bottom = y
        self.vx = vx
        self.start_x = x
        self.patrol_range = patrol_range * TILE_SIZE
        self.min_x = x - self.patrol_range
        self.max_x = x + self.patrol_range

        # Controle de salto
        self.is_jumping = False
        self.jump_timer = 0
        self.jump_cooldown = 60  # frames entre saltos
        self.jump_duration = 30  # duracao do salto em frames

    def update_movement(self):
        # Controla o timer de salto
        self.jump_timer += 1

        # Inicia salto quando o cooldown termina
        if not self.is_jumping and self.jump_timer >= self.jump_cooldown:
            self.is_jumping = True
            self.jump_timer = 0
            self.actor.image = self.jump_image

        # Durante o salto, move o sapo
        if self.is_jumping:
            self.actor.x += self.vx

            # Termina o salto apos a duracao
            if self.jump_timer >= self.jump_duration:
                self.is_jumping = False
                self.jump_timer = 0
                self.actor.image = self.idle_image

        # Inverte direcao nos limites
        if self.actor.x <= self.min_x or self.actor.x >= self.max_x:
            self.vx = -self.vx

    def animate(self, speed=15):
        pass  # Animacao controlada pelo movimento

    def draw(self):
        self.actor.draw()

    def colliderect(self, other):
        return self.actor.colliderect(other)


# ----------------------------------------------------------------

# ------------------ CRIANDO FASES --------------------------------


def create_ground_platform(start_col, end_col, row):
    """Cria uma plataforma horizontal"""
    platforms = []
    for col in range(start_col, end_col + 1):
        tile = Actor("tiles/tile_0000")
        tile.x = col * TILE_SIZE + TILE_SIZE // 2
        tile.y = row * TILE_SIZE + TILE_SIZE // 2
        platforms.append(tile)
    return platforms


def load_stage1():
    """FASE 1 - Tutorial Facil: Linha reta com poucos inimigos"""
    global enemies_list, goal, CURRENT_STAGE, CURRENT_LIVES, stage_platforms, stage_obstacles
    CURRENT_STAGE = 1
    CURRENT_LIVES = MAX_LIVES

    # Criar plataforma reta do inicio ao fim
    stage_platforms = create_ground_platform(0, 29, 13)
    stage_platforms.extend(create_ground_platform(0, 29, 14))
    stage_obstacles = []

    # Goal no chao, acessivel
    goal = Actor("goal_animation_0")
    goal.x = 28 * TILE_SIZE
    goal.bottom = 13 * TILE_SIZE
    goal.frame = 0

    enemies_list = []

    # Barnacles posicionados corretamente sobre a plataforma
    barnacle1 = StaticEnemy(barnacle_attack_images, 10 * TILE_SIZE, 13 * TILE_SIZE)
    barnacle2 = StaticEnemy(barnacle_attack_images, 20 * TILE_SIZE, 13 * TILE_SIZE)

    enemies_list.append(barnacle1)
    enemies_list.append(barnacle2)


def load_stage2():
    """FASE 2 - Comeca facil, depois fica mais desafiador"""
    global enemies_list, goal, CURRENT_STAGE, CURRENT_LIVES, stage_platforms, stage_obstacles
    CURRENT_STAGE = 2
    CURRENT_LIVES = MAX_LIVES

    # Plataforma reta no inicio
    stage_platforms = create_ground_platform(0, 12, 13)
    stage_platforms.extend(create_ground_platform(0, 12, 14))

    # Depois plataformas elevadas
    for col in range(15, 25):
        for row in range(10, 14):
            tile = Actor("tiles/tile_0000")
            tile.x = col * TILE_SIZE + TILE_SIZE // 2
            tile.y = row * TILE_SIZE + TILE_SIZE // 2
            stage_platforms.append(tile)
    # Plataforma final
    stage_platforms.extend(create_ground_platform(26, 29, 13))
    stage_platforms.extend(create_ground_platform(26, 29, 14))

    stage_obstacles = []

    goal = Actor("goal_animation_0")
    goal.x = 28 * TILE_SIZE
    goal.bottom = 13 * TILE_SIZE
    goal.frame = 0

    enemies_list = []

    barnacle1 = StaticEnemy(barnacle_attack_images, 8 * TILE_SIZE, 13 * TILE_SIZE)
    enemies_list.append(barnacle1)

    # Slime patrulhando no bloco elevado
    slime = Enemy(
        slimefire_walk_left_images,
        slimefire_walk_right_images,
        18 * TILE_SIZE,
        10 * TILE_SIZE,
        SLIMEFIRE_WALK_SPEED,
        "slimefire",
        patrol_range=2,
    )
    enemies_list.append(slime)

    # Barnacle no topo
    barnacle2 = StaticEnemy(barnacle_attack_images, 23 * TILE_SIZE, 10 * TILE_SIZE)
    enemies_list.append(barnacle2)


def load_stage3():
    """FASE 3 - Linha reta inicial com mais inimigos, depois desafio com abelhas"""
    global enemies_list, goal, CURRENT_STAGE, CURRENT_LIVES, stage_platforms, stage_obstacles
    CURRENT_STAGE = 3
    CURRENT_LIVES = MAX_LIVES

    # Plataforma reta longa no inicio (chao)
    stage_platforms = create_ground_platform(0, 15, 13)
    stage_platforms.extend(create_ground_platform(0, 15, 14))

    # Area intermediaria com plataformas (grande bloco direita)
    for col in range(18, 29):
        for row in range(10, 14):
            tile = Actor("tiles/tile_0000")
            tile.x = col * TILE_SIZE + TILE_SIZE // 2
            tile.y = row * TILE_SIZE + TILE_SIZE // 2
            stage_platforms.append(tile)

    stage_platforms.extend(create_ground_platform(0, 20, 4))

    stage_platforms.extend(create_ground_platform(20, 29, 7))

    stage_obstacles = []

    goal = Actor("goal_animation_0")
    goal.x = 2 * TILE_SIZE
    goal.bottom = 4 * TILE_SIZE
    goal.frame = 0

    enemies_list = []

    # SUBSTITUIDO: Sapos saltando no chao (antes eram mouses)
    frog1 = JumpingFrog(
        5 * TILE_SIZE,
        13 * TILE_SIZE,
        FROG_WALK_SPEED,
        patrol_range=3,
    )
    frog2 = JumpingFrog(
        12 * TILE_SIZE,
        13 * TILE_SIZE,
        -FROG_WALK_SPEED,
        patrol_range=3,
    )
    enemies_list.append(frog1)
    enemies_list.append(frog2)

    # Barnacles
    barnacle1 = StaticEnemy(barnacle_attack_images, 10 * TILE_SIZE, 13 * TILE_SIZE)
    barnacle2 = StaticEnemy(barnacle_attack_images, 22 * TILE_SIZE, 10 * TILE_SIZE)
    enemies_list.append(barnacle1)
    enemies_list.append(barnacle2)

    # Abelhas voando

    bee_positions = [5, 15]

    for col in bee_positions:

        bee = Enemy(
            bee_walk_left_images,
            bee_walk_right_images,
            col * TILE_SIZE,
            4 * TILE_SIZE,
            BEE_WALK_SPEED,
            "bee",
            patrol_range=2,
        )

        enemies_list.append(bee)
    # Slime
    slime = Enemy(
        slimefire_walk_left_images,
        slimefire_walk_right_images,
        24 * TILE_SIZE,
        10 * TILE_SIZE,
        SLIMEFIRE_WALK_SPEED,
        "slimefire",
        patrol_range=5,
    )
    enemies_list.append(slime)


def load_stage4():
    global enemies_list, goal, CURRENT_STAGE, CURRENT_LIVES, stage_platforms, stage_obstacles
    CURRENT_STAGE = 4
    CURRENT_LIVES = MAX_LIVES

    stage_platforms = []

    # Plataforma inicial
    stage_platforms.extend(create_ground_platform(0, 5, 13))

    # Plataformas suspensas (escada)
    for i, col in enumerate([8, 11, 14, 17, 20]):
        row = 11 - i
        for c in range(col, col + 1):
            tile = Actor("tiles/tile_0000")
            tile.x = c * TILE_SIZE + TILE_SIZE // 2
            tile.y = row * TILE_SIZE + TILE_SIZE // 2
            stage_platforms.append(tile)
    # Plataforma final alta
    stage_platforms.extend(create_ground_platform(23, 29, 6))

    stage_obstacles = []

    goal = Actor("goal_animation_0")
    goal.x = 27 * TILE_SIZE
    goal.bottom = 6 * TILE_SIZE
    goal.frame = 0

    enemies_list = []

    # Snails (lentos) no chao
    # snail1 = Enemy(
    #   snail_walk_images,
    #   snail_walk_images,
    #   3 * TILE_SIZE,
    #   13 * TILE_SIZE,
    #   SNAIL_WALK_SPEED,
    #   "snail",
    #   0.5,
    #)
    # enemies_list.append(snail1)

    # Barnacles em lugares estrategicos
    # barnacle1 = StaticEnemy(barnacle_attack_images, 11 * TILE_SIZE, 11 * TILE_SIZE)
    barnacle2 = StaticEnemy(barnacle_attack_images, 25 * TILE_SIZE, 6 * TILE_SIZE)
    # enemies_list.append(barnacle1)
    enemies_list.append(barnacle2)

    # Slimes
    slime = Enemy(
        slimefire_walk_left_images,
        slimefire_walk_right_images,
        25 * TILE_SIZE,
        6 * TILE_SIZE,
        SLIMEFIRE_WALK_SPEED,
        "slimefire",
        patrol_range=2,
    )
    enemies_list.append(slime)


# ----------- FIM CRIACAO DE FASES ------------------------------


def advance_stage():
    global CURRENT_STAGE, GAME_STATE, SCORE

    SCORE += POINTS_PER_STAGE

    if CURRENT_STAGE == 1:
        load_stage2()
        hero.reset_position()
    elif CURRENT_STAGE == 2:
        load_stage3()
        hero.reset_position()
    elif CURRENT_STAGE == 3:
        load_stage4()
        hero.reset_position()
    elif CURRENT_STAGE == 4:
        GAME_STATE = WINNER_STATE
        hero.reset_position()
        if SOUND_ON:
            try:
                sounds.victory.play()
            except:
                pass


def reset_game():
    global CURRENT_LIVES, SCORE

    CURRENT_LIVES = MAX_LIVES
    SCORE = 0
    load_stage1()
    hero.reset_position()


def lose_life():
    global CURRENT_LIVES, GAME_STATE

    CURRENT_LIVES -= 1
    if SOUND_ON:
        try:
            sounds.death.play()
        except:
            pass
    if CURRENT_LIVES <= 0:
        GAME_STATE = GAME_OVER_STATE
    else:
        hero.reset_position()


# ----------- CRIACAO DO HEROI E DOS INIMIGOS ---------------------------

hero = Hero(HERO_START_POSITION)

goal = Actor("goal_animation_0")
goal.frame = 0

# Carregar icone de coracao
try:
    heart_icon = Actor("heart")
except:
    heart_icon = None  # fallback se nao encontrar
enemies_list = []
stage_platforms = []
stage_obstacles = []
load_stage1()

# ----------------- FUNCOES DE COLISAO -----------------------


def collision_platform_x():
    platform_left = False
    platform_right = False

    for tile in stage_platforms:
        if hero.colliderect(tile):
            if hero.vx < 0:
                hero.actor.left = tile.right
                platform_left = True
            elif hero.vx > 0:
                hero.actor.right = tile.left
                platform_right = True
    return platform_left, platform_right


def collision_platform_y():
    platform_under = False
    platform_over = False

    for tile in stage_platforms:
        if hero.colliderect(tile):
            if hero.vy > 0:
                hero.actor.bottom = tile.top
                hero.vy = 0
                platform_under = True
            elif hero.vy < 0:
                hero.actor.top = tile.bottom
                hero.vy = 0
                platform_over = True
    return platform_under, platform_over


# ---------- ANIMACAO ATAQUE DO BARNACLE --------------------------------


def animate_barnacles():
    for enemy in enemies_list:
        if isinstance(enemy, StaticEnemy):
            original_bottom = enemy.actor.bottom
            enemy.frame = (enemy.frame + 1) % len(enemy.images)
            enemy.actor.image = enemy.images[enemy.frame]
            enemy.actor.bottom = original_bottom


clock.schedule_interval(animate_barnacles, BARNACLE_ATTACK_SPEED)

# ---------- ANIMACAO DO OBJETIVO --------------------------------


def animate_goal():
    goal.frame = (goal.frame + 1) % len(goal_images)
    goal.image = goal_images[goal.frame]


clock.schedule_interval(animate_goal, GOAL_ANIMATION_SPEED)

# ---------- VARIAVEIS PARA ANIMACAO DAS TELAS ----------
winner_animation_frame = 0
game_over_animation_frame = 0

# ---------- DESENHANDO ELEMENTOS NA TELA --------------------------------


def draw():
    global winner_animation_frame, game_over_animation_frame

    # TELA DE GAME OVER
    if GAME_STATE == GAME_OVER_STATE:
        screen.clear()

        # Fundo vermelho escuro
        for y in range(0, HEIGHT, 10):
            color_value = int(80 - (y / HEIGHT) * 40)
            screen.draw.filled_rect(Rect((0, y), (WIDTH, 10)), (color_value + 60, 0, 0))
        game_over_animation_frame = (game_over_animation_frame + 1) % 255

        # Banner
        banner_rect = Rect((WIDTH // 2 - 380, HEIGHT // 2 - 140), (760, 280))
        screen.draw.filled_rect(banner_rect, (40, 0, 0))

        for i in range(5):
            border = Rect(
                (banner_rect.x - i, banner_rect.y - i),
                (banner_rect.width + i * 2, banner_rect.height + i * 2),
            )
            screen.draw.rect(border, (255, 0, 0))
        # Texto GAME OVER
        screen.draw.text(
            "GAME OVER",
            center=(WIDTH // 2, HEIGHT // 2 - 50),
            fontsize=100,
            color=(255, 50, 50),
            owidth=3,
            ocolor="white",
        )

        # Pontuacao final
        screen.draw.text(
            f"Pontuacao Final: {SCORE}",
            center=(WIDTH // 2, HEIGHT // 2 + 40),
            fontsize=50,
            color="white",
            owidth=2,
            ocolor="black",
        )

        # Instrucao piscante
        if (game_over_animation_frame // 30) % 2 == 0:
            screen.draw.text(
                "Pressione ENTER para voltar ao menu",
                center=(WIDTH // 2, HEIGHT // 2 + 150),
                fontsize=40,
                color="white",
            )
        return
    # TELA DE VITORIA - Estilo Pixel Art
    if GAME_STATE == WINNER_STATE:
        screen.clear()

        # Fundo gradiente roxo para rosa (de cima para baixo)
        for y in range(0, HEIGHT, 1):
            # Gradiente suave de roxo para rosa
            progress = y / HEIGHT
            r = int(100 + (255 - 100) * progress)  # 100 -> 255
            g = int(80 + (180 - 80) * progress)    # 80 -> 180
            b = int(180 + (220 - 180) * progress)  # 180 -> 220
            screen.draw.filled_rect(Rect((0, y), (WIDTH, 1)), (r, g, b))

        # Estrelas brancas espalhadas
        import random
        random.seed(42)
        for _ in range(200):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            star_size = random.choice([2, 3, 4])
            screen.draw.filled_rect(Rect((x, y), (star_size, star_size)), (255, 255, 255))

        winner_animation_frame = (winner_animation_frame + 1) % 255

        # Nuvens pixeladas brancas no topo e embaixo
        cloud_top_positions = [
            (80, 100, 70),
            (200, 80, 80),
            (WIDTH - 200, 90, 75),
            (WIDTH - 80, 110, 65),
        ]

        cloud_bottom_positions = [
            (100, HEIGHT - 100, 70),
            (250, HEIGHT - 80, 80),
            (WIDTH - 250, HEIGHT - 90, 75),
            (WIDTH - 100, HEIGHT - 110, 65),
        ]

        for x, y, size in cloud_top_positions + cloud_bottom_positions:
            # Base da nuvem
            screen.draw.filled_circle((x, y), size, (255, 255, 255))
            screen.draw.filled_circle((x + size//2, y - 10), size * 0.7, (255, 255, 255))
            screen.draw.filled_circle((x - size//2, y + 10), size * 0.8, (255, 255, 255))
            screen.draw.filled_circle((x + size//3, y + 5), size * 0.6, (255, 255, 255))
            # Detalhes internos cinza claro
            screen.draw.filled_circle((x - 10, y + 5), size * 0.3, (220, 220, 230))
            screen.draw.filled_circle((x + 15, y), size * 0.25, (220, 220, 230))

        # Texto "YOU WIN!!!" estilo pixel art no topo
        title_y = HEIGHT // 4

        # Sombra do texto
        screen.draw.text(
            "YOU WIN!!!",
            center=(WIDTH // 2 + 3, title_y + 3),
            fontsize=100,
            color=(80, 60, 120),
        )

        # Texto principal branco
        screen.draw.text(
            "YOU WIN!!!",
            center=(WIDTH // 2, title_y),
            fontsize=100,
            color=(255, 255, 255),
        )

        # Trofeu grande centralizado
        trophy_x = WIDTH // 2
        trophy_y = HEIGHT // 2 + 20
        trophy_scale = 3  # Escala aumentada

        # Base do trofeu (marrom/dourado escuro)
        base_width = 40 * trophy_scale
        base_height = 10 * trophy_scale
        screen.draw.filled_rect(
            Rect((trophy_x - base_width//2, trophy_y + 50 * trophy_scale), (base_width, base_height)),
            (184, 134, 11)
        )
        # Contorno da base (desenhando 3 retangulos sobrepostos para simular espessura)
        for i in range(3):
            screen.draw.rect(
                Rect((trophy_x - base_width//2 - i, trophy_y + 50 * trophy_scale - i), (base_width + i*2, base_height + i*2)),
                (0, 0, 0)
            )

        # Haste (dourada)
        stem_width = 10 * trophy_scale
        stem_height = 20 * trophy_scale
        screen.draw.filled_rect(
            Rect((trophy_x - stem_width//2, trophy_y + 30 * trophy_scale), (stem_width, stem_height)),
            (255, 215, 0)
        )
        # Contorno da haste
        for i in range(3):
            screen.draw.rect(
                Rect((trophy_x - stem_width//2 - i, trophy_y + 30 * trophy_scale - i), (stem_width + i*2, stem_height + i*2)),
                (0, 0, 0)
            )

        # Copa principal (dourada/amarela com gradiente)
        cup_width = 35 * trophy_scale
        cup_height = 30 * trophy_scale

        # Corpo da copa com gradiente
        for i in range(int(cup_height)):
            y_offset = trophy_y + i
            width_at_y = int(cup_width * (0.7 + 0.3 * (i / cup_height)))
            color_intensity = int(255 - (50 * (i / cup_height)))
            screen.draw.filled_rect(
                Rect((trophy_x - width_at_y//2, y_offset), (width_at_y, 1)),
                (color_intensity, color_intensity - 40, 0)
            )

        # Contorno da copa
        for i in range(4):
            screen.draw.rect(
                Rect((trophy_x - cup_width//2 - i, trophy_y - i), (cup_width + i*2, cup_height + i*2)),
                (0, 0, 0)
            )

        # Alcas do trofeu (esquerda e direita)
        handle_width = 10 * trophy_scale
        handle_height = 15 * trophy_scale

        # Alca esquerda (desenhar como retangulo oco)
        for i in range(4):
            screen.draw.rect(
                Rect((trophy_x - cup_width//2 - handle_width - 5 - i, trophy_y + 8 - i), (handle_width + i*2, handle_height + i*2)),
                (255, 215, 0)
            )
        for i in range(2):
            screen.draw.rect(
                Rect((trophy_x - cup_width//2 - handle_width - 5 - i, trophy_y + 8 - i), (handle_width + i*2, handle_height + i*2)),
                (0, 0, 0)
            )

        # Alca direita
        for i in range(4):
            screen.draw.rect(
                Rect((trophy_x + cup_width//2 + 5 - i, trophy_y + 8 - i), (handle_width + i*2, handle_height + i*2)),
                (255, 215, 0)
            )
        for i in range(2):
            screen.draw.rect(
                Rect((trophy_x + cup_width//2 + 5 - i, trophy_y + 8 - i), (handle_width + i*2, handle_height + i*2)),
                (0, 0, 0)
            )

        # Brilho na copa
        shine_size = 8 * trophy_scale
        screen.draw.filled_rect(
            Rect((trophy_x - 15, trophy_y + 10), (shine_size, shine_size)),
            (255, 255, 200)
        )

        # Interior da copa (roxo claro para dar profundidade)
        interior_width = int(cup_width * 0.6)
        interior_height = int(cup_height * 0.3)
        screen.draw.filled_rect(
            Rect((trophy_x - interior_width//2, trophy_y + 5), (interior_width, interior_height)),
            (200, 180, 220)
        )

        # Pontuacao final abaixo do trofeu
        score_y = HEIGHT - 180
        screen.draw.text(
            f"PONTUACAO FINAL: {SCORE}",
            center=(WIDTH // 2 + 2, score_y + 2),
            fontsize=40,
            color=(80, 60, 120),
        )
        screen.draw.text(
            f"PONTUACAO FINAL: {SCORE}",
            center=(WIDTH // 2, score_y),
            fontsize=40,
            color=(255, 255, 255),
        )

        # Instrucao piscante
        if (winner_animation_frame // 30) % 2 == 0:
            screen.draw.text(
                "PRESSIONE ENTER PARA CONTINUAR",
                center=(WIDTH // 2 + 1, score_y + 61),
                fontsize=30,
                color=(100, 80, 140),
            )
            screen.draw.text(
                "PRESSIONE ENTER PARA CONTINUAR",
                center=(WIDTH // 2, score_y + 60),
                fontsize=30,
                color=(255, 255, 255),
            )

        # Particulas brilhantes animadas ao redor do trofeu
        for i in range(8):
            angle = (winner_animation_frame + i * 45) % 360
            import math
            distance = 120 + 20 * math.sin(winner_animation_frame * 0.1 + i)
            particle_x = trophy_x + int(distance * math.cos(math.radians(angle)))
            particle_y = trophy_y + 40 + int(distance * math.sin(math.radians(angle)))
            particle_size = random.choice([4, 5, 6])
            particle_color = random.choice([
                (255, 255, 255),  # Branco
                (255, 255, 200),  # Amarelo claro
                (255, 220, 100),  # Dourado
            ])
            # Estrela de 4 pontas
            screen.draw.filled_rect(
                Rect((particle_x - particle_size//2, particle_y - 1), (particle_size, 3)),
                particle_color
            )
            screen.draw.filled_rect(
                Rect((particle_x - 1, particle_y - particle_size//2), (3, particle_size)),
                particle_color
            )

        return
    if GAME_STATE == "MENU":
        screen.clear()

        # Background com gradiente mais vibrante e nuvens
        for y in range(0, HEIGHT, 8):
            # Gradiente de azul claro para azul escuro
            blue_light = int(200 - (y / HEIGHT) * 80)
            blue_dark = int(255 - (y / HEIGHT) * 100)
            screen.draw.filled_rect(
                Rect((0, y), (WIDTH, 8)), (100, blue_light, blue_dark)
            )
        # Estrelas decorativas no fundo
        import random

        random.seed(12345)
        for _ in range(50):
            star_x = random.randint(0, WIDTH)
            star_y = random.randint(0, HEIGHT // 2)
            star_size = random.randint(1, 3)
            screen.draw.filled_circle((star_x, star_y), star_size, (255, 255, 200))
        # Nuvens decorativas maiores e mais bonitas
        cloud_positions = [
            (120, 120, 60),
            (180, 110, 70),
            (240, 130, 55),
            (WIDTH - 200, 100, 65),
            (WIDTH - 120, 120, 60),
            (400, 200, 50),
            (WIDTH - 400, 180, 55),
        ]
        for x, y, size in cloud_positions:
            # Nuvens com sombra
            screen.draw.filled_circle((x + 2, y + 2), size, (180, 180, 180))
            screen.draw.filled_circle((x, y), size, (255, 255, 255))
            screen.draw.filled_circle(
                (x + size // 2, y - 5), size * 0.7, (255, 255, 255)
            )
            screen.draw.filled_circle(
                (x - size // 2, y + 5), size * 0.8, (255, 255, 255)
            )
        # Plataforma decorativa no menu com grama
        platform_y = HEIGHT - 150
        for x in range(0, WIDTH, TILE_SIZE):
            tile = Actor("tiles/tile_0000")
            tile.x = x + TILE_SIZE // 2
            tile.y = platform_y
            tile.draw()
        # HEROI PARADO no menu (animado)
        menu_hero = Actor("hero_idle_1")
        menu_hero.midbottom = (WIDTH // 4, platform_y)
        menu_hero.draw()

        # Objetivo/Bandeira no menu
        menu_goal = Actor("goal_animation_0")
        menu_goal.midbottom = (WIDTH - WIDTH // 4, platform_y)
        menu_goal.draw()

        # Banner do titulo com efeito de sombra 3D
        title_y = HEIGHT // 5
        for i in range(5, 0, -1):
            shadow_color = 50 - i * 8
            screen.draw.text(
                "PLANET INVASION",
                center=(WIDTH // 2 + i, title_y + i),
                fontsize=90,
                color=(shadow_color, shadow_color, shadow_color),
            )
        # Titulo principal com gradiente
        screen.draw.text(
            "PLANET INVASION",
            center=(WIDTH // 2, title_y),
            fontsize=90,
            color=(255, 215, 0),
            owidth=4,
            ocolor=(138, 43, 226),
        )

        # Subtitulo
        screen.draw.text(
            "Uma Aventura Espacial",
            center=(WIDTH // 2, title_y + 70),
            fontsize=35,
            color=(255, 255, 255),
            owidth=2,
            ocolor=(100, 100, 200),
        )

        # Botoes com novo visual
        button_y_start = HEIGHT // 2 + 50

        # Botao Iniciar - com animacao de pulso
        btn_start_y = button_y_start
        screen.draw.filled_rect(
            Rect(
                (button_start.x - 3, button_start.y - 3),
                (button_start.width + 6, button_start.height + 6),
            ),
            (255, 140, 0),
        )
        screen.draw.filled_rect(button_start, (255, 165, 0))
        for i in range(3):
            border_rect = Rect(
                (button_start.x - i, button_start.y - i),
                (button_start.width + i * 2, button_start.height + i * 2),
            )
            screen.draw.rect(border_rect, (255, 255, 255))
        screen.draw.text(
            "INICIAR JOGO",
            center=button_start.center,
            fontsize=48,
            color="white",
            owidth=3,
            ocolor=(139, 69, 19),
        )

        # Botao Som - estilo toggle
        screen.draw.filled_rect(
            Rect(
                (button_sound.x - 3, button_sound.y - 3),
                (button_sound.width + 6, button_sound.height + 6),
            ),
            (70, 130, 180),
        )
        screen.draw.filled_rect(button_sound, (100, 149, 237))
        for i in range(3):
            border_rect = Rect(
                (button_sound.x - i, button_sound.y - i),
                (button_sound.width + i * 2, button_sound.height + i * 2),
            )
            screen.draw.rect(border_rect, (255, 255, 255))
        texto_som = "SOM: LIGADO" if SOUND_ON else "SOM: DESLIGADO"
        screen.draw.text(
            texto_som,
            center=button_sound.center,
            fontsize=42,
            color="white",
            owidth=3,
            ocolor=(25, 25, 112),
        )

        # Botao Sair - destaque vermelho
        screen.draw.filled_rect(
            Rect(
                (button_exit.x - 3, button_exit.y - 3),
                (button_exit.width + 6, button_exit.height + 6),
            ),
            (139, 0, 0),
        )
        screen.draw.filled_rect(button_exit, (220, 20, 60))
        for i in range(3):
            border_rect = Rect(
                (button_exit.x - i, button_exit.y - i),
                (button_exit.width + i * 2, button_exit.height + i * 2),
            )
            screen.draw.rect(border_rect, (255, 255, 255))
        screen.draw.text(
            "SAIR",
            center=button_exit.center,
            fontsize=48,
            color="white",
            owidth=3,
            ocolor=(100, 0, 0),
        )

        # Informacoes do jogo em painel decorativo
        info_panel_y = HEIGHT - 80
        info_panel = Rect((WIDTH // 2 - 300, info_panel_y - 10), (600, 65))
        screen.draw.filled_rect(info_panel, (255, 255, 255, 150))
        screen.draw.rect(info_panel, (138, 43, 226))

        screen.draw.text(
            f"Recorde: {SCORE} pontos  |  Total de Fases: {TOTAL_STAGES}",
            center=(WIDTH // 2, info_panel_y + 20),
            fontsize=32,
            color=(50, 50, 50),
            owidth=1,
            ocolor=(200, 200, 200),
        )

        return
    # Desenha o jogo
    screen.clear()

    # Desenhar background com gradiente azul ceu + nuvens e estrelas
    for y in range(0, HEIGHT, 10):
        blue_value = int(135 + (y / HEIGHT) * 100)
        screen.draw.filled_rect(Rect((0, y), (WIDTH, 10)), (135, blue_value, 235))

    # Estrelas decorativas (pequenas e espalhadas)
    import random
    random.seed(42)
    for _ in range(50):
        star_x = random.randint(0, WIDTH)
        star_y = random.randint(0, HEIGHT // 2)
        star_size = random.choice([2, 3])
        screen.draw.filled_rect(Rect((star_x, star_y), (star_size, star_size)), (255, 255, 255))

    # Nuvens decorativas brancas
    cloud_positions = [
        (150, 80, 40),
        (400, 100, 50),
        (WIDTH - 200, 70, 45),
        (WIDTH - 400, 90, 38),
        (250, HEIGHT - 100, 42),
        (WIDTH - 300, HEIGHT - 120, 48),
    ]

    for x, y, size in cloud_positions:
        # Nuvem com sombra
        screen.draw.filled_circle((x + 2, y + 2), size, (200, 200, 200))
        screen.draw.filled_circle((x, y), size, (255, 255, 255))
        screen.draw.filled_circle((x + size//2, y - 8), int(size * 0.7), (255, 255, 255))
        screen.draw.filled_circle((x - size//2, y + 8), int(size * 0.8), (255, 255, 255))

    # Desenhar plataformas da fase
    for platform in stage_platforms:
        platform.draw()
    # Desenhar obstaculos
    for obstacle in stage_obstacles:
        obstacle.draw()
    hero.draw()
    goal.draw()

    for enemy in enemies_list:
        enemy.draw()
    for i in range(CURRENT_LIVES):
        x = 30 + i * 40
        y = 30

        if heart_icon:
            heart = Actor("heart")
            heart.center = (x, y)
            heart.draw()
        else:
            # Fallback: desenhar coracao simples se a imagem nao carregar
            screen.draw.filled_circle((x - 6, y - 2), 6, (220, 20, 60))
            screen.draw.filled_circle((x + 6, y - 2), 6, (220, 20, 60))
            # Corpo do coracao (usando circulos sobrepostos)
            for offset in range(12):
                radius = int(6 - (offset * 0.5))
                if radius > 0:
                    screen.draw.filled_circle((x, y + offset), radius, (220, 20, 60))
    # Fase atual - canto superior central
    screen.draw.text(
        f"Fase {CURRENT_STAGE}/{TOTAL_STAGES}",
        midtop=(WIDTH // 2, 5),
        fontsize=30,
        color="white",
        owidth=2,
        ocolor=(0, 0, 0),
    )

    # Pontuacao - canto superior direito
    screen.draw.text(
        f"Pontos: {SCORE}",
        topright=(WIDTH - 10, 5),
        fontsize=28,
        color="white",
        owidth=2,
        ocolor=(0, 0, 0),
    )


# ---------- ATUALIZANDO ELEMENTOS NA TELA --------------------------------


def update():
    global GAME_STATE

    if (
        GAME_STATE == "MENU"
        or GAME_STATE == WINNER_STATE
        or GAME_STATE == GAME_OVER_STATE
    ):
        return
    # Deslocamento e animacao dos inimigos
    for enemy in enemies_list:
        if isinstance(enemy, Enemy):
            enemy.update_movement()

            if enemy.enemy_type == "slimefire":
                enemy.animate(int(SLIMEFIRE_WALK_ANIMATION_SPEED * 60))
            elif enemy.enemy_type == "bee":
                enemy.animate(int(BEE_WALK_ANIMATION_SPEED * 60))
            elif enemy.enemy_type == "frog":
                enemy.animate(int(FROG_WALK_ANIMATION_SPEED * 60))
            elif enemy.enemy_type == "snail":
                enemy.animate(int(SNAIL_WALK_ANIMATION_SPEED * 60))
            elif enemy.enemy_type == "fly":
                enemy.animate(int(FLY_WALK_ANIMATION_SPEED * 60))
        elif isinstance(enemy, JumpingFrog):
            enemy.update_movement()
    # Gravidade e colisoes verticais
    hero.apply_gravity()
    platform_under, platform_over = collision_platform_y()

    # CORRIGIDO: Morte por queda
    if hero.actor.top > HEIGHT:
        lose_life()
        return
    # Salto do heroi
    if keyboard.space:
        hero.jump(platform_under)
    # Caminhada do heroi
    hero.move_horizontal()
    collision_platform_x()
    hero.clamp_to_screen()

    # Colisao com obstaculos
    for obstacle in stage_obstacles:
        if hero.colliderect(obstacle):
            lose_life()
            break
    # Colisao com inimigos
    for enemy in enemies_list:
        if isinstance(enemy, Enemy):
            collided = hero.colliderect(enemy.actor)
        elif isinstance(enemy, StaticEnemy):
            collided = hero.colliderect(enemy.actor)
        elif isinstance(enemy, JumpingFrog):
            collided = hero.colliderect(enemy.actor)
        else:
            collided = hero.colliderect(enemy)
        if collided:
            lose_life()
            break
    # Colisao com objetivo
    if hero.colliderect(goal):
        advance_stage()
    # Animacao do heroi
    hero.animate()


# _______________ TRATAR CLIQUES NOS BOTOES _________________________________


def on_mouse_down(pos):
    global GAME_STATE, SOUND_ON

    if GAME_STATE == "MENU":
        if button_start.collidepoint(pos):
            GAME_STATE = "JOGO"
            reset_game()
            if SOUND_ON:
                try:
                    music.play(BACKGROUND_MUSIC)
                    music.set_volume(0.5)
                except:
                    pass
        elif button_sound.collidepoint(pos):
            SOUND_ON = not SOUND_ON
            if SOUND_ON:
                if GAME_STATE == "JOGO":
                    try:
                        music.play(BACKGROUND_MUSIC)
                        music.set_volume(0.5)
                    except:
                        pass
            else:
                try:
                    music.stop()
                except:
                    pass
        elif button_exit.collidepoint(pos):
            raise SystemExit


# ------------- RETORNAR AO MENU -----------------------------


def on_key_down(key):
    global GAME_STATE
    if (
        GAME_STATE == WINNER_STATE or GAME_STATE == GAME_OVER_STATE
    ) and key == keys.RETURN:
        GAME_STATE = "MENU"
