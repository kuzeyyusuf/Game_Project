import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 900, 580
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chimp Test + Mage Animation")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BLUE = (80, 80, 255)
RED = (200, 0, 0)

def extract_flame_frames(sheet, frame_width, frame_height):
    frames = []
    for i in range(sheet.get_width() // frame_width):
        x = i * frame_width
        frame = sheet.subsurface((x, 0, frame_width, frame_height))
        frames.append(frame)
    return frames

font = pygame.font.SysFont(None, 36)


background_layer1 = pygame.image.load("Assets/background_layer_1.png")
background_layer1 = pygame.transform.scale(background_layer1, (WIDTH, HEIGHT))

background_layer2 = pygame.image.load("Assets/background_layer_2.png")
background_layer2 = pygame.transform.scale(background_layer2, (WIDTH, HEIGHT))

background_layer3 = pygame.image.load("Assets/background_layer_3.png")
background_layer3 = pygame.transform.scale(background_layer3, (WIDTH, HEIGHT))

combat_ground = pygame.image.load("Assets/combat_ground.png").convert_alpha()
combat_ground = pygame.transform.scale(combat_ground, (280, 160))  # Genişliği ve yüksekliği ayarlayabilirsin


flame_frames = []
flame_start_frames = []
flame_end_frames = []


flame_frames += extract_flame_frames(pygame.image.load("Assets/burning_loop_1.png").convert_alpha(), 24, 32)
flame_frames += extract_flame_frames(pygame.image.load("Assets/burning_loop_2.png").convert_alpha(), 20, 24)
flame_frames += extract_flame_frames(pygame.image.load("Assets/burning_loop_3.png").convert_alpha(), 15, 24)
flame_frames += extract_flame_frames(pygame.image.load("Assets/burning_loop_4.png").convert_alpha(), 10, 20)
flame_frames += extract_flame_frames(pygame.image.load("Assets/burning_loop_5.png").convert_alpha(), 8, 8)

flame_start_frames += extract_flame_frames(pygame.image.load("Assets/burning_start_1.png").convert_alpha(), 24, 32)
flame_start_frames += extract_flame_frames(pygame.image.load("Assets/burning_start_2.png").convert_alpha(), 20, 24)
flame_start_frames += extract_flame_frames(pygame.image.load("Assets/burning_start_3.png").convert_alpha(), 15, 24)
flame_start_frames += extract_flame_frames(pygame.image.load("Assets/burning_start_4.png").convert_alpha(), 10, 20)
flame_start_frames += extract_flame_frames(pygame.image.load("Assets/burning_start_5.png").convert_alpha(), 8, 8)

flame_end_frames += extract_flame_frames(pygame.image.load("Assets/burning_end_1.png").convert_alpha(), 24, 32)
flame_end_frames += extract_flame_frames(pygame.image.load("Assets/burning_end_2.png").convert_alpha(), 20, 24)
flame_end_frames += extract_flame_frames(pygame.image.load("Assets/burning_end_3.png").convert_alpha(), 15, 24)
flame_end_frames += extract_flame_frames(pygame.image.load("Assets/burning_end_4.png").convert_alpha(), 10, 20)
flame_end_frames += extract_flame_frames(pygame.image.load("Assets/burning_end_5.png").convert_alpha(), 8, 8)

# Grid layout
GRID_SIZE = 4
CELL_SIZE = 100
PADDING = 10
MARGIN_X = (640 - (GRID_SIZE * (CELL_SIZE + PADDING))) // 2
MARGIN_Y = 60

# Game state
mage_hp = 50
knight_hp = 50
current_player = 1  # 1: Mage, 2: Knight
current_count = 2
sequence = []
clicked_sequence = []
revealed = False
countdown_active = False
countdown_start_time = 0
COUNTDOWN_DURATION = 4000
game_over = False
shake_timer = 0
shake_duration = 300
shake_magnitude = 8
flame_phase = "start"
flame_index = 0
flame_timer = 0
flame_speed = 100


awaiting_enter_to_start = True
awaiting_next_round = False
last_failed_level = None
hit_threshold = None
dice_roll_result = None
awaiting_dice_roll = False
dice_result_shown = False
message = ""

# --- Mage animation ---
def extract_frames(sheet, cols, rows, w, h, skip=[], flip=False):
    frames = []
    for i in range(cols * rows):
        if i in skip:
            continue
        x = (i % cols) * w
        y = (i // cols) * h
        frame = sheet.subsurface((x, y, w, h))
        if flip:
            frame = pygame.transform.flip(frame, True, False)
        frames.append(frame)
    return frames


idle_sheet = pygame.image.load("Assets/Sprites/Idle.png").convert_alpha()
attack_sheet = pygame.image.load("Assets/Sprites/Attack.png").convert_alpha()
hurt_sheet = pygame.image.load("Assets/Sprites/Take Hit.png").convert_alpha()
death_sheet = pygame.image.load("Assets/Sprites/Death.png").convert_alpha()

knight_idle_sheet = pygame.image.load("Assets/Idle.png").convert_alpha()
knight_attack_sheet = pygame.image.load("Assets/Attacks.png").convert_alpha()
knight_hurt_sheet = pygame.image.load("Assets/Hurt.png").convert_alpha()
knight_death_sheet = pygame.image.load("Assets/Death.png").convert_alpha()

idle_frames = extract_frames(idle_sheet, 8, 1, 150, 150)
attack_frames = extract_frames(attack_sheet, 8, 1, 150, 150)
hurt_frames = extract_frames(hurt_sheet, 4, 1, 150, 150)
death_frames = extract_frames(death_sheet, 5, 1, 150, 150)

knight_idle_frames = extract_frames(knight_idle_sheet, 2, 4, 128, 64, flip=True)
knight_attack_frames = extract_frames(knight_attack_sheet, 8, 5, 128, 64, flip=True)
knight_hurt_frames = extract_frames(knight_hurt_sheet, 2, 2, 128, 64, skip=[3], flip=True)
knight_death_frames = extract_frames(knight_death_sheet, 2, 2, 128, 64, flip=True)


mage_state = "idle"
mage_frame_index = 0
mage_timer = 0
mage_death_done = False

mage_speed = {
    "idle": 150,
    "attack": 100,
    "hurt": 200,
    "death": 250
}

mage_x = 610
mage_y = HEIGHT // 2 - 75
# Knight karakterin durumu
knight_state = "idle"
knight_idle_index = 0
knight_attack_index = 0
knight_hurt_index = 0
knight_death_index = 0

knight_timer = 0
knight_animation_speed = 100
knight_death_finished = False

knight_x = 660
knight_y = HEIGHT // 2 -40


def generate_sequence(count):
    positions = random.sample(range(GRID_SIZE * GRID_SIZE), count)
    numbers = list(range(1, count + 1))
    random.shuffle(numbers)
    return list(zip(positions, numbers))

# HP çubuğu çizimi
def draw_hp_bar(x, y, hp, max_hp, color):
    bar_width = 100
    bar_height = 10
    fill_width = int((hp / max_hp) * bar_width)
    pygame.draw.rect(screen, BLACK, (x, y, bar_width, bar_height))  # Çerçeve
    pygame.draw.rect(screen, color, (x, y, fill_width, bar_height))  # Dolu kısım


def get_cell_rect(index):
    row = index // GRID_SIZE
    col = index % GRID_SIZE
    x = MARGIN_X + col * (CELL_SIZE + PADDING)
    y = MARGIN_Y + row * (CELL_SIZE + PADDING)
    return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

def draw_grid_cell(rect, is_revealed=False, is_clicked=False):
    base_color = (200, 200, 200) if is_revealed else (180, 180, 180)
    border_color = (100, 100, 100)
    highlight_color = (255, 255, 255)

    # Ana kutu
    pygame.draw.rect(screen, base_color, rect, border_radius=4)

    # Parlak kenarlar (üst ve sol)
    pygame.draw.line(screen, highlight_color, rect.topleft, rect.topright, 2)
    pygame.draw.line(screen, highlight_color, rect.topleft, rect.bottomleft, 2)

    # Gölge kenarlar (alt ve sağ)
    pygame.draw.line(screen, border_color, rect.bottomleft, rect.bottomright, 2)
    pygame.draw.line(screen, border_color, rect.topright, rect.bottomright, 2)

    # Çerçeve
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=4)

    # Tıklanmışsa maviyle doldur
    if is_clicked:
        pygame.draw.rect(screen, (80, 80, 255), rect, 0, border_radius=4)


def start_new_round(success=True):
    global sequence, clicked_sequence, message, awaiting_next_round
    global current_count, awaiting_enter_to_start
    global last_failed_level, hit_threshold, awaiting_dice_roll, dice_roll_result, dice_result_shown
    global mage_state, mage_frame_index, mage_timer

    if success:
        current_count += 1
        message = f" Success! Press ENTER for next round ({current_count})"
        awaiting_next_round = True
        awaiting_enter_to_start = False
    else:
        last_failed_level = current_count
        hit_threshold = max(20 - last_failed_level, 5)
        awaiting_dice_roll = True
        dice_result_shown = False
        dice_roll_result = None
        message = " Wrong! Press ENTER to roll D20"
        current_count = 2
        awaiting_next_round = False
        awaiting_enter_to_start = False

        # Mage attack başlat

        mage_frame_index = 0
        mage_timer = 0

sequence = generate_sequence(current_count)

running = True
while running:
    # Ekran sarsıntısı
    shake_offset = [0, 0]
    if shake_timer > 0:
        shake_offset[0] = random.randint(-shake_magnitude, shake_magnitude)
        shake_offset[1] = random.randint(-shake_magnitude, shake_magnitude)
        shake_timer -= dt

    dt = clock.tick(FPS)
    now = pygame.time.get_ticks()
    screen.blit(background_layer1, (0 + shake_offset[0], 0 + shake_offset[1]))
    screen.blit(background_layer2, (0 + shake_offset[0], 0 + shake_offset[1]))
    screen.blit(background_layer3, (0 + shake_offset[0], 0 + shake_offset[1]))
    screen.blit(combat_ground, (560 + shake_offset[0], 220 + shake_offset[1]))

    # Oyuncu sırası göstergesi
    if not game_over:
        if current_player == 1:
            turn_text = font.render(" Mage's Turn", True, (0, 0, 0))
        else:
            turn_text = font.render(" Knight's Turn", True, (0, 0, 0))

        screen.blit(turn_text, (10, 10))

    flame_timer += dt
    if flame_timer >= flame_speed:
        flame_timer = 0
        flame_index += 1

        if flame_phase == "start":
            if flame_index >= len(flame_start_frames):
                flame_index = 0
                flame_phase = "loop"

        elif flame_phase == "loop":
            if flame_index >= len(flame_frames):
                flame_index = 0
                flame_phase = "end"

        elif flame_phase == "end":
            if flame_index >= len(flame_end_frames):
                flame_index = 0
                flame_phase = "start"

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Oyunu sıfırla
                mage_hp = 50
                knight_hp = 50
                mage_state = "idle"
                mage_frame_index = 0
                mage_timer = 0
                mage_death_done = False

                knight_state = "idle"
                knight_idle_index = 0
                knight_attack_index = 0
                knight_hurt_index = 0
                knight_death_index = 0
                knight_timer = 0
                knight_death_finished = False

                current_player = 1
                current_count = 2
                sequence = generate_sequence(current_count)
                clicked_sequence.clear()
                revealed = False
                countdown_active = False
                countdown_start_time = 0
                message = ""
                awaiting_enter_to_start = True
                awaiting_next_round = False
                last_failed_level = None
                hit_threshold = None
                dice_roll_result = None
                awaiting_dice_roll = False
                dice_result_shown = False
                game_over = False

            if event.key == pygame.K_RETURN and not game_over:
                if awaiting_dice_roll and not dice_result_shown:
                    dice_roll_result = random.randint(1, 20)
                    dice_result_shown = True
                    if dice_roll_result >= hit_threshold:
                        message = f" Hit! (Rolled {dice_roll_result}) "
                        damage = dice_roll_result
                        if current_player == 2:
                            # Knight saldırıyor
                            knight_state = "attack"
                            knight_attack_index = 0
                            knight_timer = 0

                            # Mage hasar alıyor
                            mage_state = "hurt"
                            mage_frame_index = 0
                            mage_timer = 0
                            shake_timer = shake_duration
                            mage_hp -= damage
                            if mage_hp <= 0:
                                mage_state = "death"
                                mage_frame_index = 0
                                mage_timer = 0
                                message += " ️ Mage is defeated! Press R to restart"
                                game_over = True

                        else:
                            # Mage saldırıyor
                            mage_state = "attack"
                            mage_frame_index = 0
                            mage_timer = 0

                            # Knight hasar alıyor
                            knight_state = "hurt"
                            knight_hurt_index = 0
                            knight_timer = 0
                            shake_timer = shake_duration
                            knight_hp -= damage
                            if knight_hp <= 0:
                                knight_state = "death"
                                knight_death_index = 0
                                knight_timer = 0
                                message += "  Knight is defeated! Press R to restart"
                                game_over = True
                    else:
                        message = f" Miss! (Rolled {dice_roll_result}) - Press ENTER to restart"

                elif awaiting_dice_roll and dice_result_shown:
                    sequence = generate_sequence(current_count)
                    clicked_sequence.clear()
                    revealed = False
                    countdown_active = False
                    countdown_start_time = 0
                    message = ""
                    awaiting_dice_roll = False
                    dice_result_shown = False
                    dice_roll_result = None
                    last_failed_level = None
                    hit_threshold = None
                    awaiting_enter_to_start = True
                    # Oyuncu sırasını değiştir
                    current_player = 2 if current_player == 1 else 1


                elif awaiting_next_round:
                    sequence = generate_sequence(current_count)
                    clicked_sequence.clear()
                    revealed = False
                    countdown_active = False
                    countdown_start_time = 0
                    message = ""
                    awaiting_next_round = False
                    awaiting_enter_to_start = True

                elif awaiting_enter_to_start:
                    revealed = True
                    countdown_active = True
                    countdown_start_time = now
                    awaiting_enter_to_start = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not revealed and not awaiting_next_round and not awaiting_enter_to_start and not awaiting_dice_roll:
            pos = pygame.mouse.get_pos()
            for idx, num in sequence:
                rect = get_cell_rect(idx)
                if rect.collidepoint(pos) and (idx, num) not in clicked_sequence:
                    clicked_sequence.append((idx, num))
                    expected = len(clicked_sequence)
                    if num != expected:
                        start_new_round(success=False)
                    elif expected == current_count:
                        start_new_round(success=True)
                    break

    # Countdown
    if countdown_active:
        elapsed = now - countdown_start_time
        if elapsed >= COUNTDOWN_DURATION:
            revealed = False
            countdown_active = False
        else:
            remaining = (COUNTDOWN_DURATION - elapsed) // 1000 + 1
            countdown_text = font.render(f"Look! {remaining}", True, BLACK)
            screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, 20))

    # Draw grid
    for i in range(GRID_SIZE * GRID_SIZE):
        rect = get_cell_rect(i)

        matched = [(idx, n) for idx, n in sequence if idx == i]
        clicked = any(idx == i for (idx, n) in clicked_sequence)
        revealed_now = matched and revealed

        draw_grid_cell(rect, is_revealed=revealed_now, is_clicked=clicked)

        if matched and revealed:
            idx, num = matched[0]
            text = font.render(str(num), True, BLACK)
            screen.blit(text, text.get_rect(center=rect.center))

    # Show hit threshold
    if last_failed_level and not dice_result_shown:
        text = font.render(f"To Hit: Roll ≥ {hit_threshold} on a D20", True, BLACK)
        screen.blit(text, (560, 180))

    # Show result message
    if message:
        label = font.render(message, True, RED if "Wrong" in message or "Miss" in message else BLACK)
        screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT - 40))
    # === HP göstergesi sağ alt köşe ===
    heart_text = font.render("", True, RED)
    heart_x = WIDTH - 270
    heart_y = HEIGHT - 200
    screen.blit(heart_text, (heart_x, heart_y))

    # Mage ismi ve canı
    mage_label = font.render("Mage", True, BLACK)
    mage_hp_text = font.render(f"HP: {mage_hp}", True, BLACK)
    screen.blit(mage_label, (heart_x, heart_y + 30))
    screen.blit(mage_hp_text, (heart_x, heart_y + 55))

    # Knight ismi ve canı
    knight_label = font.render("Knight", True, BLACK)
    knight_hp_text = font.render(f"HP: {knight_hp}", True, BLACK)
    screen.blit(knight_label, (heart_x + 90, heart_y + 30))
    screen.blit(knight_hp_text, (heart_x + 90, heart_y + 55))

    # Mage animation update
    mage_timer += dt
    if mage_timer >= mage_speed[mage_state]:
        mage_timer = 0
        mage_frame_index += 1

        if mage_state == "idle":
            mage_frame_index %= len(idle_frames)
        elif mage_state == "attack":
            if mage_frame_index >= len(attack_frames):
                mage_frame_index = 0
                mage_state = "idle"
        elif mage_state == "hurt":
            if mage_frame_index >= len(hurt_frames):
                mage_frame_index = 0
                mage_state = "idle"
        elif mage_state == "death":
            if mage_frame_index >= len(death_frames):
                mage_frame_index = len(death_frames) - 1
                mage_death_done = True

    # Draw mage frame
    if mage_state == "idle":
        mage_frame = idle_frames[mage_frame_index]
    elif mage_state == "attack":
        mage_frame = attack_frames[min(mage_frame_index, len(attack_frames) - 1)]
    elif mage_state == "hurt":
        mage_frame = hurt_frames[min(mage_frame_index, len(hurt_frames) - 1)]
    elif mage_state == "death":
        mage_frame = death_frames[min(mage_frame_index, len(death_frames) - 1)]

    screen.blit(mage_frame, (mage_x + shake_offset[0], mage_y + shake_offset[1]))
    # --- Knight animasyon kontrolü ---
    knight_timer += dt

    if knight_state == "idle":
        if knight_timer >= knight_animation_speed:
            knight_timer = 0
            knight_idle_index = (knight_idle_index + 1) % len(knight_idle_frames)
        knight_frame = knight_idle_frames[knight_idle_index]

    elif knight_state == "attack":
        if knight_timer >= knight_animation_speed:
            knight_timer = 0
            knight_attack_index += 1
            if knight_attack_index >= 10:
                knight_attack_index = 0
                knight_state = "idle"
        knight_frame = knight_attack_frames[min(knight_attack_index, len(knight_attack_frames) - 1)]

    elif knight_state == "hurt":
        if knight_timer >= 250:
            knight_timer = 0
            knight_hurt_index += 1
            if knight_hurt_index >= len(knight_hurt_frames):
                knight_hurt_index = 0
                knight_state = "idle"
        knight_frame = knight_hurt_frames[knight_hurt_index]

    elif knight_state == "death":
        if knight_timer >= 300:
            knight_timer = 0
            knight_death_index += 1
            if knight_death_index >= len(knight_death_frames):
                knight_death_index = len(knight_death_frames) - 1
                knight_death_finished = True
        knight_frame = knight_death_frames[knight_death_index]

    # Ekrana çiz
    screen.blit(knight_frame, (knight_x + shake_offset[0], knight_y + shake_offset[1]))

    # HP çubukları
    draw_hp_bar(mage_x, mage_y + 175, mage_hp, 50, RED)
    draw_hp_bar(knight_x + 60, knight_y + 140, knight_hp, 50, RED)
    # Flame
    if flame_phase == "start":
        flame_image = flame_start_frames[flame_index]
    elif flame_phase == "loop":
        flame_image = flame_frames[flame_index]
    elif flame_phase == "end":
        flame_image = flame_end_frames[flame_index]


    flame_width = flame_image.get_width()
    flame_height = flame_image.get_height()

    for x in range(0, WIDTH, flame_width):
        screen.blit(flame_image, (x, HEIGHT - flame_height))

    pygame.display.flip()

pygame.quit()
sys.exit()
