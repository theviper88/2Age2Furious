import pygame
import math
import random
import statistics
import sys
import os


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2Age2Furious")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
countdown_font = pygame.font.SysFont(None, 160)
default_background_colour = (177, 211, 255)
default_text_colour = (25, 25, 30)

LOGO_IMAGE = pygame.image.load(resource_path("assets/2age2furious_logo.png")).convert_alpha()
LOGO_WIDTH = 600 
LOGO_HEIGHT = int(LOGO_IMAGE.get_height() * (LOGO_WIDTH / LOGO_IMAGE.get_width()))  # preserve aspect ratio
LOGO_IMAGE = pygame.transform.scale(LOGO_IMAGE, (LOGO_WIDTH, LOGO_HEIGHT))


THEME_OPTIONS = [
    ("Race Track", "race_track"),
    ("Forest Path", "forest_path"),
]
THEME_SWATCH_WIDTH = 190
THEME_SWATCH_HEIGHT = 120
THEME_SWATCH_GAP = 40  


MODE_OPTIONS = [
    ("vs Computer", "vs_computer"),
    ("Two Players", "two_player"),
    ("Time Trial", "time_trial"),
]
MODE_HUMAN_PLAYERS = {
    "vs_computer": 1,
    "two_player": 2,
    "time_trial": 1,
}
MODE_BUTTON_WIDTH = 190
MODE_BUTTON_HEIGHT = 120
MODE_BUTTON_GAP = 40

CONTROL_SCHEMES = [
    (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP),   # player 1: arrow keys
    (pygame.K_d, pygame.K_a, pygame.K_s, pygame.K_w),              # player 2: WASD
]

SELECTION_SWATCH_SIZE = 100
SELECTION_SWATCH_GAP = 30
SELECTION_SWATCHES_PER_ROW = 4

COUNTDOWN_NUMBER_DURATION_MS = 1000

MENU_MUSIC_PATH = "assets/aoe2_8bit_menu.mp3"
MENU_MUSIC_VOLUME = 0.2

RACE_MUSIC_PATH = "assets/aoe2_8bit_race.mp3"
RACE_MUSIC_VOLUME = 0.4

# --- Track definition ---
# The track is a rectangular "ring": the square may go anywhere inside
# TRACK_OUTER, but may not enter TRACK_INNER (the hole in the middle).
TRACK_OUTER = pygame.Rect(50, 50, 700, 500)
TRACK_INNER = pygame.Rect(150, 150, 500, 300)


TRACK_DECAL_VIL = pygame.image.load(resource_path("assets/villager.png"))
TRACK_DECAL_BOAR = pygame.image.load(resource_path("assets/boar.png"))
TRACK_DECAL_MON = pygame.image.load(resource_path("assets/monastery.png"))
TRACK_DECAL_PALM = pygame.image.load(resource_path("assets/palm_tree.png"))
DECAL_SETTINGS = [
    (TRACK_DECAL_VIL, 1, 50),
    (TRACK_DECAL_BOAR, 1, 60),
    (TRACK_DECAL_MON, 1, 200),
    (TRACK_DECAL_PALM, 2, 100),
]
TRACK_DECALS = []


TRACK_TYPE = 'race_track'   # default theme, used until the player picks one

TRACK_SURFACE_COLORS = {'race_track': (55, 55, 65), 'forest_path': (177, 177, 111)}
TRACK_HOLE_COLORS = {'race_track': (184, 164, 114), 'forest_path': (77, 122, 11)}
TRACK_BORDER_WIDTH = 4
TRACK_BORDER_COLORS = {'race_track': (200, 200, 200), 'forest_path': (177, 177, 111)}
TRACK_LINES_COLORS = {'race_track': (255, 255, 255), 'forest_path': (177, 177, 111)}
COLOR_OPTIONS_BY_THEME = {
    'race_track': [
    ("Blue", (70, 130, 220)),
    ("Red", (220, 60, 60)),
    ("Green", (60, 190, 100)),
    ("Yellow", (230, 200, 60)),
    ("Cyan", (40, 211, 211)),
    ("Purple", (160, 90, 200)),
    ("Grey", (128, 128, 128)),
    ("Orange", (230, 140, 50)),
    ],
    'forest_path': [
        ("Blue", (0, 0, 255)),
        ("Red", (255, 0, 0)),
        ("Green", (0, 255, 0)),
        ("Yellow", (255, 255, 0)),
        ("Cyan", (0, 255, 255)),
        ("Purple", (138, 43, 226)),
        ("Grey", (128, 128, 128)),
        ("Orange", (255, 165, 0)),
    ]
}
COLOR_IMAGE_PATHS_BY_THEME = { # from AoE2 game files https://ageofnotes.com/sld-extractor-online-aoe2/
    'race_track': {
        "Blue": "assets/cobra_car_blue.png",
        "Red": "assets/cobra_car_red.png",
        "Green": "assets/cobra_car_green.png",
        "Yellow": "assets/cobra_car_yellow.png",
        "Cyan": "assets/cobra_car_cyan.png",
        "Purple": "assets/cobra_car_purple.png",
        "Grey": "assets/cobra_car_grey.png",
        "Orange": "assets/cobra_car_orange.png",
    },
    'forest_path': {
        "Blue": "assets/aoe_king_blue.png",
        "Red": "assets/aoe_knight_red.png",
        "Green": "assets/aoe_king_green.png",
        "Yellow": "assets/aoe_king_yellow.png",
        "Cyan": "assets/aoe_king_cyan.png",
        "Purple": "assets/aoe_king_purple.png",
        "Grey": "assets/aoe_king_grey.png",
        "Orange": "assets/aoe_king_orange.png",
    }
}
COLOR_IMAGE_SIZES_BY_THEME = {
    'race_track': {
        "Blue": [66,36],
        "Red": [66,36],
        "Green": [66,36],
        "Yellow": [66,36],
        "Cyan": [66,36],
        "Purple": [66,36],
        "Grey": [66,36],
        "Orange": [66,36],
    },
    'forest_path': {
        "Blue": [43,43], 
        "Red": [46,40],
        "Green": [43,43], 
        "Yellow": [43,43], 
        "Cyan": [43,43], 
        "Purple": [43,43], 
        "Grey": [43,43], 
        "Orange": [43,43], 
    }
}
SOUND_EFFECTS_BY_THEME = { #from aoe2 soundboard https://www.myinstants.com/
    'race_track': {
        "track_selection": "assets/aoe_cobra_car_sound.mp3",
        "colour_selection": "assets/aoe_cobra_car_sound.mp3",
        "countdown_3_sound": "assets/aoe_taunt_3_food.mp3",
        "countdown_2_sound": "assets/aoe_taunt_2_no.mp3",
        "countdown_1_sound": "assets/aoe_taunt_1_yes.mp3",
        "race_start": "assets/aoe_viking_horn.mp3",
        "race_end":  "assets/aoe2-monk-conversion-warning-sound-clip.mp3",
        "new_game":  "assets/aoe2-14-start-the-game-already.mp3",
    },
    'forest_path': {
        "track_selection": "assets/aoe_wololo_sound.wav",
        "colour_selection": "assets/aoe_taunt_1_yes.mp3",
        "countdown_3_sound": "assets/aoe_taunt_3_food.mp3",
        "countdown_2_sound": "assets/aoe_taunt_2_no.mp3",
        "countdown_1_sound": "assets/aoe_taunt_1_yes.mp3",
        "race_start": "assets/aoe_viking_horn.mp3",
        "race_end":  "assets/aoe2-monk-conversion-warning-sound-clip.mp3",
        "new_game":  "assets/aoe2-14-start-the-game-already.mp3",
    }
}



CENTER_LINE_RECT = pygame.Rect(
    (TRACK_OUTER.left + TRACK_INNER.left) // 2,
    (TRACK_OUTER.top + TRACK_INNER.top) // 2,
    (TRACK_OUTER.right + TRACK_INNER.right) // 2 - (TRACK_OUTER.left + TRACK_INNER.left) // 2,
    (TRACK_OUTER.bottom + TRACK_INNER.bottom) // 2 - (TRACK_OUTER.top + TRACK_INNER.top) // 2,
)

START_LINE_CHECKER_SIZE = 12
START_LINE_RECT = pygame.Rect(
    TRACK_INNER.left,                      # aligns with the inner barrier's top-left corner
    TRACK_OUTER.top + TRACK_BORDER_WIDTH,
    START_LINE_CHECKER_SIZE * 2,           # two columns wide
    TRACK_INNER.top - TRACK_OUTER.top - TRACK_BORDER_WIDTH,     # spans the top straight's height
)

PLAY_AGAIN_BUTTON = pygame.Rect(0, 0, 220, 60)
PLAY_AGAIN_BUTTON.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

AI_SPEED = 5
AI_WAYPOINT_RADIUS = 100   # how close counts as "reached" (larger = cuts corners more)
AI_WAYPOINTS = [
    CENTER_LINE_RECT.topright,
    CENTER_LINE_RECT.bottomright,
    CENTER_LINE_RECT.bottomleft,
    CENTER_LINE_RECT.topleft,
]

MUTE_BUTTON = pygame.Rect(0, 0, 40, 40)
muted = False
current_music_volume = MENU_MUSIC_VOLUME



class GameObject:
    def __init__(self, x, y, width, height, image_path, colour_name, speed=5, is_ai=False):
        self.base_image = pygame.image.load(resource_path(image_path)).convert_alpha()
        self.base_image = pygame.transform.scale(self.base_image, (width, height))
        self.image = self.base_image
        self.colour_name = colour_name
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.angle = 0  # degrees, 0 = facing up
        self.laps = -1
        self.on_start_line = False
        self.start_pos = (x, y)
        self.colour_name = colour_name
        self.is_ai = is_ai
        self.waypoint_index = 0

    def move(self, dx, dy, is_valid_position):
        if dx != 0 or dy != 0:
            if dx < 0 and dy == 0:
                new_image = pygame.transform.flip(self.base_image, True, False)
                new_angle = self.angle
            else:
                new_angle = -math.degrees(math.atan2(dy, dx))
                new_image = pygame.transform.rotate(self.base_image, new_angle)
            new_rect = new_image.get_rect(center=self.rect.center)

            # Only turn if the turned car actually fits here
            if is_valid_position(new_rect):
                self.image = new_image
                self.rect = new_rect
                self.angle = new_angle

        old_x, old_y = self.rect.x, self.rect.y
        self.rect.x += dx * self.speed
        if not is_valid_position(self.rect):
            self.rect.x = old_x
        self.rect.y += dy * self.speed
        if not is_valid_position(self.rect):
            self.rect.y = old_y


    def ai_direction(self):
        """Steer toward the current waypoint. Returns (dx, dy) as -1/0/1, the same
        form the keyboard produces, so move() handles the rest."""
        target_x, target_y = AI_WAYPOINTS[self.waypoint_index]
        cx, cy = self.rect.center

        if math.hypot(target_x - cx, target_y - cy) < AI_WAYPOINT_RADIUS:
            self.waypoint_index = (self.waypoint_index + 1) % len(AI_WAYPOINTS)
            target_x, target_y = AI_WAYPOINTS[self.waypoint_index]

        # Only steer on an axis if more than one step away, otherwise it jitters around the line
        dx = 0 if abs(target_x - cx) < self.speed else (1 if target_x > cx else -1)
        dy = 0 if abs(target_y - cy) < self.speed else (1 if target_y > cy else -1)
        return dx, dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)



def start_music(MUSIC_PATH, MUSIC_VOLUME):
    global current_music_volume
    current_music_volume = MUSIC_VOLUME
    pygame.mixer.music.load(resource_path(MUSIC_PATH))
    pygame.mixer.music.set_volume(0 if muted else MUSIC_VOLUME)
    pygame.mixer.music.play(loops=-1)   # -1 means loop forever


def stop_music():
    pygame.mixer.music.fadeout(500) 


def generate_texture(width, height, base_color, variation):
    texture = pygame.Surface((width, height))
    texture.fill(base_color)
    # Speckle it with random shade variations to simulate asphalt/gravel
    for _ in range((width * height) // 5):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        shade = random.randint(-variation, variation)
        speckle_color = tuple(max(0, min(255, c + shade)) for c in base_color)
        texture.set_at((x, y), speckle_color)
    return texture


ACTIVE_COLOR_OPTIONS = []
ACTIVE_COLOR_IMAGE_PATHS = {}
ACTIVE_COLOR_IMAGE_SIZES = {}
ACTIVE_SOUNDS = {}

def apply_theme(theme_key):
    global TRACK_TYPE, TRACK_SURFACE_COLOR, TRACK_HOLE_COLOR, TRACK_BORDER_COLOR, TRACK_LINES_COLOR
    global TRACK_TEXTURE, HOLE_TEXTURE, BACKGROUND_TEXTURE, TRACK_DECALS
    global ACTIVE_COLOR_OPTIONS, ACTIVE_COLOR_IMAGE_PATHS, ACTIVE_COLOR_IMAGE_SIZES, ACTIVE_SOUNDS, swatch_rects

    TRACK_TYPE = theme_key
    TRACK_SURFACE_COLOR = TRACK_SURFACE_COLORS[TRACK_TYPE]
    TRACK_HOLE_COLOR = TRACK_HOLE_COLORS[TRACK_TYPE]
    TRACK_BORDER_COLOR = TRACK_BORDER_COLORS[TRACK_TYPE]
    TRACK_LINES_COLOR = TRACK_LINES_COLORS[TRACK_TYPE]

    TRACK_TEXTURE = generate_texture(TRACK_OUTER.width, TRACK_OUTER.height, base_color=TRACK_SURFACE_COLOR, variation=50)
    HOLE_TEXTURE = generate_texture(TRACK_INNER.width, TRACK_INNER.height, base_color=TRACK_HOLE_COLOR, variation=150)
    BACKGROUND_TEXTURE = generate_texture(SCREEN_WIDTH, SCREEN_HEIGHT, base_color=TRACK_HOLE_COLOR, variation=150)
    TRACK_DECALS = build_track_decals()

    ACTIVE_COLOR_OPTIONS = COLOR_OPTIONS_BY_THEME[theme_key]
    ACTIVE_COLOR_IMAGE_PATHS = COLOR_IMAGE_PATHS_BY_THEME[theme_key]
    ACTIVE_COLOR_IMAGE_SIZES = COLOR_IMAGE_SIZES_BY_THEME[theme_key]
    swatch_rects = build_swatch_rects()   # rebuild in case a theme ever has a different number of colours

    ACTIVE_SOUNDS = {
        event_name: pygame.mixer.Sound(resource_path(path))
        for event_name, path in SOUND_EFFECTS_BY_THEME[theme_key].items()
    }
    apply_mute()   # add this


def is_on_track(rect):
    """A position is valid if it's fully inside the outer boundary
    and doesn't overlap the inner hole."""
    return TRACK_OUTER.contains(rect) and not TRACK_INNER.colliderect(rect)


def update_lap_count(player):
    colliding = player.rect.colliderect(START_LINE_RECT)
    if colliding and not player.on_start_line:
        player.laps += 1
    player.on_start_line = colliding


def lap_status_text(player_objects):
    return "   ".join(f"{p.colour_name} Laps: {p.laps}" for p in player_objects)


def finish_title_text(winner, player_objects):
    if game_mode == "time_trial":
        return "Finished!"
    if game_mode == "vs_computer":
        return "Computer wins!" if player_objects[winner - 1].is_ai else "You win!"
    return f"Player {winner} wins!"


def build_theme_rects():
    total_width = len(THEME_OPTIONS) * THEME_SWATCH_WIDTH + (len(THEME_OPTIONS) - 1) * THEME_SWATCH_GAP
    start_x = (SCREEN_WIDTH - total_width) // 2
    y = SCREEN_HEIGHT - THEME_SWATCH_HEIGHT - 80   # was: SCREEN_HEIGHT // 2 - THEME_SWATCH_HEIGHT // 2

    rects = []
    for i in range(len(THEME_OPTIONS)):
        x = start_x + i * (THEME_SWATCH_WIDTH + THEME_SWATCH_GAP)
        rects.append(pygame.Rect(x, y, THEME_SWATCH_WIDTH, THEME_SWATCH_HEIGHT))
    return rects

theme_rects = build_theme_rects()


def build_theme_previews():
    textures = {}
    images = {}

    for name, key in THEME_OPTIONS:
        # Mini version of the track's actual texture, sized to fit the swatch
        textures[key] = generate_texture(
            THEME_SWATCH_WIDTH, THEME_SWATCH_HEIGHT,
            base_color=TRACK_SURFACE_COLORS[key], variation=50
        )

        # Use that theme's first colour option as its representative icon
        preview_colour_name = COLOR_OPTIONS_BY_THEME[key][0][0]
        preview_path = COLOR_IMAGE_PATHS_BY_THEME[key][preview_colour_name]
        preview_size = COLOR_IMAGE_SIZES_BY_THEME[key][preview_colour_name]

        preview_image = pygame.image.load(resource_path(preview_path)).convert_alpha()
        # Scale to fit inside the swatch with some margin, preserving aspect ratio
        max_dim = min(THEME_SWATCH_WIDTH, THEME_SWATCH_HEIGHT) - 20
        scale_factor = max_dim / statistics.mean(preview_size)
        scaled_size = (int(preview_size[0] * scale_factor), int(preview_size[1] * scale_factor))
        images[key] = pygame.transform.scale(preview_image, scaled_size)

    return textures, images

THEME_PREVIEW_TEXTURES, THEME_PREVIEW_IMAGES = build_theme_previews()


def get_hovered_theme(mouse_pos):
    for i, rect in enumerate(theme_rects):
        if rect.collidepoint(mouse_pos):
            return i
    return None


def build_swatch_rects():
    num_rows = math.ceil(len(ACTIVE_COLOR_OPTIONS) / SELECTION_SWATCHES_PER_ROW)

    row_width = SELECTION_SWATCHES_PER_ROW * SELECTION_SWATCH_SIZE + (SELECTION_SWATCHES_PER_ROW - 1) * SELECTION_SWATCH_GAP
    start_x = (SCREEN_WIDTH - row_width) // 2

    total_height = num_rows * SELECTION_SWATCH_SIZE + (num_rows - 1) * SELECTION_SWATCH_GAP
    start_y = (SCREEN_HEIGHT - total_height) // 2

    rects = []
    for i in range(len(ACTIVE_COLOR_OPTIONS)):
        col = i % SELECTION_SWATCHES_PER_ROW
        row = i // SELECTION_SWATCHES_PER_ROW
        x = start_x + col * (SELECTION_SWATCH_SIZE + SELECTION_SWATCH_GAP)
        y = start_y + row * (SELECTION_SWATCH_SIZE + SELECTION_SWATCH_GAP)
        rects.append(pygame.Rect(x, y, SELECTION_SWATCH_SIZE, SELECTION_SWATCH_SIZE))
    return rects


def get_hovered_swatch(mouse_pos):
    for i, rect in enumerate(swatch_rects):
        if rect.collidepoint(mouse_pos):
            return i
    return None


def build_mode_rects():
    total_width = len(MODE_OPTIONS) * MODE_BUTTON_WIDTH + (len(MODE_OPTIONS) - 1) * MODE_BUTTON_GAP
    start_x = (SCREEN_WIDTH - total_width) // 2
    y = SCREEN_HEIGHT - MODE_BUTTON_HEIGHT - 80   # same height as the theme swatches

    return [
        pygame.Rect(start_x + i * (MODE_BUTTON_WIDTH + MODE_BUTTON_GAP), y, MODE_BUTTON_WIDTH, MODE_BUTTON_HEIGHT)
        for i in range(len(MODE_OPTIONS))
    ]

mode_rects = build_mode_rects()


def get_hovered_mode(mouse_pos):
    for i, rect in enumerate(mode_rects):
        if rect.collidepoint(mouse_pos):
            return i
    return None


def apply_mute():
    """Push the current mute state onto the music and every loaded sound effect."""
    pygame.mixer.music.set_volume(0 if muted else current_music_volume)
    for sound in ACTIVE_SOUNDS.values():
        sound.set_volume(0 if muted else 1.0)


def draw_mute_button(surface):
    hovered = MUTE_BUTTON.collidepoint(pygame.mouse.get_pos())
    #pygame.draw.rect(surface, (90, 90, 100) if hovered else (60, 60, 70), MUTE_BUTTON, border_radius=8)
    #pygame.draw.rect(surface, (200, 200, 200), MUTE_BUTTON, 2, border_radius=8)

    icon_colour = (240, 240, 240)
    x, y = MUTE_BUTTON.center

    # Speaker: a small box plus a cone
    pygame.draw.rect(surface, icon_colour, (x - 12, y - 4, 6, 8))
    pygame.draw.polygon(surface, icon_colour, [(x - 6, y - 4), (x + 1, y - 10), (x + 1, y + 10), (x - 6, y + 4)])

    if muted:
        # cross where the sound waves would be
        pygame.draw.line(surface, icon_colour, (x + 5, y - 6), (x + 13, y + 6), 3)
        pygame.draw.line(surface, icon_colour, (x + 13, y - 6), (x + 5, y + 6), 3)
    else:
        # Two sound-wave arcs
        for r in (6, 11):
            pygame.draw.arc(surface, icon_colour, (x + 1 - r, y - r, 2 * r, 2 * r), -math.pi / 3, math.pi / 3, 2)


def draw_theme_select_screen(surface, hovered_index):
    surface.fill(default_background_colour)

    logo_rect = LOGO_IMAGE.get_rect(center=(SCREEN_WIDTH // 2, 160))
    surface.blit(LOGO_IMAGE, logo_rect)

    title = font.render("Choose a track theme", True, default_text_colour)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 340))
    surface.blit(title, title_rect)

    for i, rect in enumerate(theme_rects):
        name, key = THEME_OPTIONS[i]

        surface.blit(THEME_PREVIEW_TEXTURES[key], rect.topleft)   # was: pygame.draw.rect(surface, TRACK_SURFACE_COLORS[key], rect)

        preview_image = THEME_PREVIEW_IMAGES[key]
        preview_rect = preview_image.get_rect(center=rect.center)
        surface.blit(preview_image, preview_rect)

        border_color = (255, 255, 255) if i == hovered_index else (90, 90, 90)
        border_width = 4 if i == hovered_index else 2
        pygame.draw.rect(surface, border_color, rect, border_width)

        label = font.render(name, True, default_text_colour)
        label_rect = label.get_rect(center=(rect.centerx, rect.bottom + 20))
        surface.blit(label, label_rect)


def draw_mode_select_screen(surface, hovered_index):
    surface.fill(default_background_colour)

    logo_rect = LOGO_IMAGE.get_rect(center=(SCREEN_WIDTH // 2, 160))
    surface.blit(LOGO_IMAGE, logo_rect)

    title = font.render("Choose a mode", True, default_text_colour)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 340))
    surface.blit(title, title_rect)

    for i, rect in enumerate(mode_rects):
        name, _ = MODE_OPTIONS[i]
        hovered = (i == hovered_index)

        pygame.draw.rect(surface, (90, 90, 100) if hovered else (60, 60, 70), rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255) if hovered else (200, 200, 200), rect, 4 if hovered else 2, border_radius=8)

        label = font.render(name, True, (240, 240, 240))
        surface.blit(label, label.get_rect(center=rect.center))


def draw_selection_screen(surface, hovered_index, player):
    surface.fill(default_background_colour)

    title_text = "Select a colour" if NO_PLAYERS == 1 else f"Player {player}: Select a colour"
    title = font.render(title_text, True, default_text_colour)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
    surface.blit(title, title_rect)

    for i, rect in enumerate(swatch_rects):
        name, color = ACTIVE_COLOR_OPTIONS[i]
        pygame.draw.rect(surface, color, rect)

        border_color = (255, 255, 255) if i == hovered_index else (90, 90, 90)
        border_width = 4 if i == hovered_index else 2
        pygame.draw.rect(surface, border_color, rect, border_width)

        label = font.render(str(i + 1), True, (0, 0, 0)) #name
        label_rect = label.get_rect(center=rect.center)
        surface.blit(label, label_rect)


def create_ai_player(taken_names, slot):
    choices = [name for name, _ in ACTIVE_COLOR_OPTIONS if name not in taken_names]
    name = random.choice(choices)
    width, height = ACTIVE_COLOR_IMAGE_SIZES[name]
    x, y = find_start_position(width, height, slot)
    return GameObject(
        x=x, y=y, width=width, height=height,
        image_path=ACTIVE_COLOR_IMAGE_PATHS[name],
        colour_name=name,
        speed=AI_SPEED,
        is_ai=True,
    )


def draw_race_start_screen(surface, player_objects):
    surface.fill(default_background_colour)

    title_text = "GET READY!!!"
    title = countdown_font.render(title_text, True, default_text_colour)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
    surface.blit(title, title_rect)

    gap = 40  # space between the two car images
    total_width = sum(p.rect.width for p in player_objects) + gap * (len(player_objects) - 1)
    start_x = (SCREEN_WIDTH - total_width) // 2
    y = SCREEN_HEIGHT // 2 + 40

    x = start_x
    for p in player_objects:
        p.rect.topleft = (x, y)
        p.draw(surface)
        x += p.rect.width + gap


def find_start_position(width, height, slot=0):
    candidate = pygame.Rect(TRACK_OUTER.x + 40, TRACK_OUTER.y + 10 + slot * (height + 10), width, height)
    if is_on_track(candidate):
        return candidate.x, candidate.y
    return TRACK_OUTER.x + 5, TRACK_OUTER.y + 5


def draw_dashed_line(surface, color, start_pos, end_pos, width=5, dash_length=30, gap_length=20):
    x1, y1 = start_pos
    x2, y2 = end_pos
    total_length = math.hypot(x2 - x1, y2 - y1)
    step = dash_length + gap_length
    num_dashes = int(total_length // step) + 1

    for i in range(num_dashes):
        start_frac = (i * step) / total_length
        end_frac = min((i * step + dash_length) / total_length, 1)
        sx = x1 + (x2 - x1) * start_frac
        sy = y1 + (y2 - y1) * start_frac
        ex = x1 + (x2 - x1) * end_frac
        ey = y1 + (y2 - y1) * end_frac
        pygame.draw.line(surface, color, (sx, sy), (ex, ey), width)


def draw_dashed_rect(surface, color, rect, **kwargs):
    corners = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft, rect.topleft]
    for i in range(4):
        draw_dashed_line(surface, color, corners[i], corners[i + 1], **kwargs)


def draw_start_line(surface):
    num_cols = 2
    num_rows = START_LINE_RECT.height // START_LINE_CHECKER_SIZE

    for row in range(num_rows):
        for col in range(num_cols):
            color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
            checker_rect = pygame.Rect(
                START_LINE_RECT.left + col * START_LINE_CHECKER_SIZE,
                START_LINE_RECT.top + row * START_LINE_CHECKER_SIZE,
                START_LINE_CHECKER_SIZE,
                START_LINE_CHECKER_SIZE,
            )
            pygame.draw.rect(surface, color, checker_rect)


def build_track_decals(margin=15, padding=10, max_attempts=50):
    placed = []
    area = TRACK_INNER.inflate(-2 * margin, -2 * margin)   # keep decals off the barrier edge

    for source, count, size in DECAL_SETTINGS:
        for _ in range(count):
            # Fixed size: the longest side equals `size`, the other side follows
            scale = size / max(source.get_width(), source.get_height())
            width = max(1, int(source.get_width() * scale))
            height = max(1, int(source.get_height() * scale))
            image = pygame.transform.smoothscale(source, (width, height))

            # Try random spots until one doesn't overlap an already-placed decal
            for _ in range(max_attempts):
                x = random.randint(area.left, area.right - width)
                y = random.randint(area.top, area.bottom - height)
                rect = pygame.Rect(x, y, width, height)
                if not any(rect.inflate(padding, padding).colliderect(r) for _, r in placed):
                    placed.append((image, rect))
                    break

    placed.sort(key=lambda d: d[1].bottom)   # lower decals draw on top, for a simple depth effect
    return placed


def draw_track_decals(surface):
    for image, rect in TRACK_DECALS:
        surface.blit(image, rect)


def draw_track(surface):
    surface.blit(BACKGROUND_TEXTURE)  
    surface.blit(TRACK_TEXTURE, TRACK_OUTER.topleft)  
    #pygame.draw.rect(surface, TRACK_SURFACE_COLOR, TRACK_OUTER)
    surface.blit(HOLE_TEXTURE, TRACK_INNER.topleft)  
    #pygame.draw.rect(surface, TRACK_HOLE_COLOR, TRACK_INNER)
    pygame.draw.rect(surface, TRACK_BORDER_COLOR, TRACK_OUTER, TRACK_BORDER_WIDTH)
    pygame.draw.rect(surface, TRACK_BORDER_COLOR, TRACK_INNER, TRACK_BORDER_WIDTH)
    draw_dashed_rect(surface, TRACK_LINES_COLOR, CENTER_LINE_RECT, width=5, dash_length=30, gap_length=20)
    draw_start_line(surface) 
    draw_track_decals(surface)


def draw_countdown_screen(surface, player_objects, elapsed_ms):
    draw_track(surface)
    for p in player_objects:
        p.draw(surface)

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(160)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))

    seconds_left = 3 - (elapsed_ms // COUNTDOWN_NUMBER_DURATION_MS)
    number_text = str(int(seconds_left)) if seconds_left > 0 else "GO!"
    number = countdown_font.render(number_text, True, (255, 255, 255))
    number_rect = number.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    surface.blit(number, number_rect)


def draw_finish_screen(surface, winner, player_objects):
    # Draw the game scene exactly as it looked at the moment of winning
    draw_track(surface)
    for p in player_objects:
        p.draw(surface)

    # Dim the scene so text stands out clearly on top of it
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(160)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))

    title_text = finish_title_text(winner, player_objects)
    title = countdown_font.render(title_text, True, (240, 240, 240))
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(title, title_rect)

    # Laps and timer, carried over from the race screen
    lap_text = font.render(lap_status_text(player_objects), True, (240, 240, 240))
    screen.blit(lap_text, (200, 10))

    timer_text = font.render(f"{final_race_time:.2f}", True, (240, 240, 240))
    timer_rect = timer_text.get_rect(topright=(SCREEN_WIDTH - 20, 10))
    screen.blit(timer_text, timer_rect)

    mouse_pos = pygame.mouse.get_pos()
    hovered = PLAY_AGAIN_BUTTON.collidepoint(mouse_pos)
    button_color = (90, 90, 100) if hovered else (60, 60, 70)
    pygame.draw.rect(surface, button_color, PLAY_AGAIN_BUTTON, border_radius=8)
    pygame.draw.rect(surface, (200, 200, 200), PLAY_AGAIN_BUTTON, 2, border_radius=8)

    button_label = font.render("Play Again", True, (240, 240, 240))
    button_label_rect = button_label.get_rect(center=PLAY_AGAIN_BUTTON.center)
    surface.blit(button_label, button_label_rect)



# --- Main state machine ---
STATE_THEME_SELECT = "theme_select"
STATE_MODE_SELECT = "mode_select" 
STATE_PLAYER_SELECT = "player_select"
STATE_GET_READY = "get_ready"
STATE_COUNTDOWN = "countdown"
STATE_PLAY = "play"
STATE_FINISHED = "finished" 
state = STATE_THEME_SELECT

WINNING_LAPS = 5

race_start_time = 0
final_race_time = 0.0
player = 1
winner = None 
running = True

start_music(MENU_MUSIC_PATH, MENU_MUSIC_VOLUME)

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and MUTE_BUTTON.collidepoint(mouse_pos):
            muted = not muted
            apply_mute()

        elif state == STATE_THEME_SELECT and event.type == pygame.MOUSEBUTTONDOWN:
            hovered = get_hovered_theme(mouse_pos)
            if hovered is not None:
                chosen_theme_key = THEME_OPTIONS[hovered][1]
                apply_theme(chosen_theme_key)
                ACTIVE_SOUNDS["track_selection"].play()
                state = STATE_MODE_SELECT 

        elif state == STATE_MODE_SELECT and event.type == pygame.MOUSEBUTTONDOWN:
            hovered = get_hovered_mode(mouse_pos)
            if hovered is not None:
                game_mode = MODE_OPTIONS[hovered][1]
                NO_PLAYERS = MODE_HUMAN_PLAYERS[game_mode]
                players = [None] * NO_PLAYERS
                player = 1
                ACTIVE_SOUNDS["colour_selection"].play()
                state = STATE_PLAYER_SELECT
        
        elif state == STATE_PLAYER_SELECT and event.type == pygame.MOUSEBUTTONDOWN:
            ACTIVE_SOUNDS["colour_selection"].play()
            hovered = get_hovered_swatch(mouse_pos)
            if hovered is not None:
                #chosen_color = COLOR_OPTIONS[hovered][1]
                chosen_name = ACTIVE_COLOR_OPTIONS[hovered][0]   
                chosen_image = ACTIVE_COLOR_IMAGE_PATHS[chosen_name]    
                chosen_image_size = ACTIVE_COLOR_IMAGE_SIZES[chosen_name]
                start_x, start_y = find_start_position(chosen_image_size[0], chosen_image_size[1], slot=player-1)
                players[player-1] = GameObject(
                    x=start_x,
                    y=start_y,
                    width=chosen_image_size[0],
                    height=chosen_image_size[1],
                    image_path = chosen_image,
                    colour_name = chosen_name,
                )
                if player == NO_PLAYERS:
                    if game_mode == "vs_computer":
                        taken = [p.colour_name for p in players]
                        players.append(create_ai_player(taken, slot=len(players)))
                    get_ready_start_time = pygame.time.get_ticks()
                    stop_music()
                    state = STATE_GET_READY
                else:
                   player += 1

        elif state == STATE_FINISHED and event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_AGAIN_BUTTON.collidepoint(mouse_pos):
                ACTIVE_SOUNDS["new_game"].play()
                start_music(MENU_MUSIC_PATH, MENU_MUSIC_VOLUME)
                player = 1
                players = [None] * NO_PLAYERS
                winner = None
                state = STATE_THEME_SELECT
                                    
    if state == STATE_THEME_SELECT:
        hovered_index = get_hovered_theme(mouse_pos)
        draw_theme_select_screen(screen, hovered_index)

    elif state == STATE_MODE_SELECT:
        hovered_index = get_hovered_mode(mouse_pos)
        draw_mode_select_screen(screen, hovered_index)
    
    elif state == STATE_PLAYER_SELECT:
        hovered_index = get_hovered_swatch(mouse_pos)
        draw_selection_screen(screen, hovered_index, player)

    elif state == STATE_GET_READY:
        elapsed = pygame.time.get_ticks() - get_ready_start_time
        draw_race_start_screen(screen, players)
        if elapsed >= 2000:
            for p in players:
                p.rect.topleft = p.start_pos
            countdown_start_time = pygame.time.get_ticks()
            last_countdown_number = 3
            ACTIVE_SOUNDS["countdown_3_sound"].play()
            state = STATE_COUNTDOWN

    elif state == STATE_COUNTDOWN:
        elapsed = pygame.time.get_ticks() - countdown_start_time
        draw_countdown_screen(screen, players, elapsed)
        current_number = 3 - elapsed // COUNTDOWN_NUMBER_DURATION_MS
        if current_number != last_countdown_number:
            if current_number == 2:
                ACTIVE_SOUNDS["countdown_2_sound"].play()
            elif current_number == 1:
                ACTIVE_SOUNDS["countdown_1_sound"].play()
        last_countdown_number = current_number
        if elapsed >= 3 * COUNTDOWN_NUMBER_DURATION_MS:
            race_start_time = pygame.time.get_ticks()
            ACTIVE_SOUNDS["race_start"].play()
            start_music(RACE_MUSIC_PATH, RACE_MUSIC_VOLUME)
            state = STATE_PLAY

    elif state == STATE_PLAY:

        keys = pygame.key.get_pressed()
        for i, p in enumerate(players):
            if p.is_ai:
                dx, dy = p.ai_direction()
            else:
                right, left, down, up = CONTROL_SCHEMES[i]   # humans always come first, so i is their control index
                dx = keys[right] - keys[left]
                dy = keys[down] - keys[up]
            p.move(dx, dy, is_on_track)
            update_lap_count(p)

        race_elapsed_seconds = (pygame.time.get_ticks() - race_start_time) / 1000

        for i, p in enumerate(players):
            if p.laps >= WINNING_LAPS:
                winner = i + 1
                final_race_time = race_elapsed_seconds
                stop_music()
                ACTIVE_SOUNDS["race_end"].play()
                state = STATE_FINISHED
                break

        draw_track(screen)
        for p in players:
            p.draw(screen)

        lap_text = font.render(lap_status_text(players), True, (240, 240, 240))
        screen.blit(lap_text, (200, 10))

        timer_text = font.render(f"{race_elapsed_seconds:.2f}", True, (240, 240, 240))
        timer_rect = timer_text.get_rect(topright=(SCREEN_WIDTH - 20, 10))
        screen.blit(timer_text, timer_rect)

    elif state == STATE_FINISHED:
        draw_finish_screen(screen, winner, players)

    draw_mute_button(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()