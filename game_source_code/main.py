import pygame
import websockets
import json
import asyncio
import subprocess
import numpy as np
from fighter import Fighter
from cipher import encrypt

pygame.init()
pygame.mixer.init()  # for loading audio
# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BattleBlade")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 120, 0)


# define character variables
class Character:
    def __init__(
        self,
        name,
        width,
        height,
        scale,
        offset,
        steps,
        path_sp,
        path_ht,
        path_th,
        path_audio,
        audio_vol,
    ):
        self.name = name
        self.width = width
        self.height = height
        self.scale = scale
        self.offset = offset
        self.data = [width, height, scale, offset]
        self.animation_steps = steps
        self.sheet = pygame.image.load(path_sp).convert_alpha()
        self.highlight = pygame.image.load(path_ht).convert_alpha()
        self.thumbnail = pygame.image.load(path_th).convert_alpha()
        self.audio = pygame.mixer.Sound(path_audio)
        self.volume = self.audio.set_volume(audio_vol)


# Change order here to change display order in grid
characters = [
    Character(
        "Warrior",
        162,
        162,
        4,
        [72, 56],
        [10, 8, 1, 7, 7, 3, 7],
        "assets/images/sprites/warrior.png",
        "assets/images/highlights/warrior.png",
        "assets/images/thumbnails/warrior.png",
        "assets/audio/sword.wav",
        0.5,
    ),
    Character(
        "Wizard",
        250,
        250,
        3,
        [112, 107],
        [8, 8, 1, 8, 8, 3, 7],
        "assets/images/sprites/wizard.png",
        "assets/images/highlights/wizard.png",
        "assets/images/thumbnails/wizard.png",
        "assets/audio/magic.wav",
        0.5,
    ),
    Character(
        "Psyduck",
        35,
        33,
        4,
        [0, -18],
        [6, 6, 2, 4, 7, 3, 6],
        "assets/images/sprites/psyduck.png",
        "assets/images/highlights/psyduck.png",
        "assets/images/thumbnails/psyduck.png",
        "assets/audio/laser.wav",
        5,
    ),
    Character(
        "Broly",
        110,
        110,
        2,
        [30, 15],
        [1, 6, 6, 3, 5, 1, 1],
        "assets/images/sprites/broly.png",
        "assets/images/highlights/broly.png",
        "assets/images/thumbnails/broly.png",
        "assets/audio/punch.mp3",
        0.75,
    ),
    Character(
        "Batman",
        100,
        100,
        2,
        [35, 0],
        [1, 7, 8, 5, 7, 3, 4],
        "assets/images/sprites/batman.png",
        "assets/images/highlights/batman.png",
        "assets/images/thumbnails/batman.jpg",
        "assets/audio/punch.mp3",
        0.75,
    ),
    Character(
        "Superman",
        130,
        130,
        2,
        [45, 25],
        [5, 6, 6, 5, 5, 4, 3],
        "assets/images/sprites/superman.png",
        "assets/images/highlights/superman.png",
        "assets/images/thumbnails/superman.png",
        "assets/audio/punch.mp3",
        0.75,
    ),
    Character(
        "Doom",
        150,
        170,
        1.5,
        [0, 40],
        [1, 8, 4, 5, 7, 3, 6],
        "assets/images/sprites/doom.png",
        "assets/images/highlights/doom.png",
        "assets/images/thumbnails/doom.png",
        "assets/audio/punch.mp3",
        0.75,
    ),
    Character(
        "Wolverine",
        150,
        170,
        1.5,
        [0, 40],
        [1,1,1,1,1,1,1],
        "assets/images/sprites/wolverine.gif",
        "assets/images/highlights/wolverine.jpg",
        "assets/images/thumbnails/wolverine.jpg",
        "assets/audio/punch.mp3",
        0.75,
    )
    # Add more characters here if needed
]

# images for selection screen
TH_SIZE = 75
HI_HEIGHT = 250
HI_WIDTH = 175

thumbnail_list = []
highlight_list = []

for char in characters:
    thumbnail_list.append(pygame.transform.scale(char.thumbnail, (TH_SIZE, TH_SIZE)))
    highlight_list.append(pygame.transform.scale(char.highlight, (HI_WIDTH, HI_HEIGHT)))

# load bg music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
countdown_sound=pygame.mixer.Sound("assets/audio/ha.mp3")
countdown_sound.set_volume(0.25)
intro_sound=pygame.mixer.Sound("assets/audio/intro.mp3")
intro_sound.set_volume(0.5)

# load background images
# Change order of backgrounds here
bg_img_path = ["forest.jpg","alto.png","space.png", "beach.gif", "cemet.gif"]
bg_img_list = []
for path in bg_img_path:
    img = pygame.image.load("assets/images/backgrounds/" + path).convert_alpha()
    bg_img_list.append(img)

# load icons
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()
vs_img = pygame.image.load("assets/images/icons/vs.png").convert_alpha()
vs = pygame.transform.scale(vs_img, (150, 100))
red_wifi_img = pygame.image.load("assets/images/icons/red_wifi.png").convert_alpha()
red_wifi = pygame.transform.scale(red_wifi_img, (100, 100))
green_wifi_img = pygame.image.load("assets/images/icons/green_wifi.png").convert_alpha()
green_wifi = pygame.transform.scale(green_wifi_img, (100, 100))

# define fonts
large_font = pygame.font.Font("assets/fonts/afogand.ttf", 80)
score_font = pygame.font.Font("assets/fonts/afogand.ttf", 30)
command_font = pygame.font.Font("assets/fonts/afogand.ttf", 40)
simple_font = pygame.font.Font("assets/fonts/cakewalk.ttf", 40)


# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def display_boost(font, text_col, x, y, condition):
    text = "Health boosted"
    if condition:
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))


# function for drawing background
def draw_bg(ind):
    scaled_bg = pygame.transform.scale(bg_img_list[ind], (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


# function for drawing fighter health bars
def draw_health_bar(health, x, y, fighter_no):
    ratio = health / 100
    if fighter_no == 1:
        if fighter_1.invincible:
            pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
            pygame.draw.rect(screen, RED, (x, y, 400, 30))
            pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))
        else:
            pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
            pygame.draw.rect(screen, RED, (x, y, 400, 30))
            pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))
    if fighter_no == 2:
        if fighter_2.invincible:
            pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
            pygame.draw.rect(screen, RED, (x, y, 400, 30))
            pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))
        else:
            pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
            pygame.draw.rect(screen, RED, (x, y, 400, 30))
            pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


# define grid variables
NUM_ROWS = 2
NUM_COLS = 4
BOX_SIZE = 85
SHIFT = BOX_SIZE - TH_SIZE
HORI_SP = 5
VER_SP = 5
X0 = 350
Y0 = 350
row_p1 = 0
col_p1 = 0
row_p2 = 1
col_p2 = 3
p1_ind = row_p1 * NUM_COLS + col_p1
p2_ind = row_p2 * NUM_COLS + col_p2


def draw_thumbnails():
    ind = 0
    # Draw the grid boxes
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            x = X0 + col * (HORI_SP + BOX_SIZE)
            y = Y0 + row * (VER_SP + BOX_SIZE)
            pygame.draw.rect(screen, WHITE, (x, y, BOX_SIZE, BOX_SIZE))
            if ind < len(thumbnail_list):
                screen.blit(thumbnail_list[ind], (x + SHIFT / 2, y + SHIFT / 2))
                ind += 1


# define game variables
rounds = 5  # specify any odd no as no of rounds
round_count = 1
intro_screen = True
intro_count = 4
score = [0, 0]  # player scores: [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
last_count_update = pygame.time.get_ticks()
winner = 0
player1_connected = False
player2_connected = False
player1_selected = False
player2_selected = False
bg_ind = 0

# define loop variables
start_screen = True
select_screen = False
run = False
winner_screen = False


# Function to get IPv4 address of PC
def get_ipv4_address():
    result = subprocess.run(["ipconfig"], capture_output=True, text=True)
    output_lines = result.stdout.split("\n")
    check = False
    for line in output_lines:
        if "Wireless LAN adapter Wi-Fi:" in line:
            check = True
        if "Media disconnected" in line and check:
            return "localhost"
        if "IPv4 Address" in line and check:
            return line.split(":")[-1].strip()


trigger = asyncio.Event()  # game over trigger


# For sending winner message and closing connection
async def end_connection(websocket):
    await trigger.wait()
    # event = {"type": "win", "player": winner}
    # await websocket.send(json.dumps(event))
    # print("sent")
    await websocket.close()
    # print("closed")
    return


def is_valid_json(my_json):
    try:
        json.loads(my_json)
        return 1
    except ValueError:
        return 0


# dictionary for player commands
custom_data = np.full(14, False)


# function to move selection on grid
def move_on_grid(player, key):
    global player1_selected, player2_selected
    global row_p1, col_p1, row_p2, col_p2
    if player == 1 and player1_selected == True:
        return

    if player == 2 and player2_selected == True:
        return

    if player == 1 and key == 3:  # up
        row_p1 -= 1
        # print(row_p1)
        row_p1 = max(0, row_p1)

    elif player == 1 and key == 25:  # down
        row_p1 += 1
        # print(row_p1)
        row_p1 = min(NUM_ROWS - 1, row_p1)

    elif player == 1 and key == 1:  # left
        col_p1 -= 1
        # print(col_p1)
        col_p1 = max(0, col_p1)

    elif player == 1 and key == 2:  # right
        col_p1 += 1
        # print(col_p1)
        col_p1 = min(NUM_COLS - 1, col_p1)

    elif player == 1 and key == 10:  # select character
        player1_selected = True

    elif player == 2 and key == 3:  # up
        row_p2 -= 1
        row_p2 = max(0, row_p2)

    elif player == 2 and key == 25:  # down
        row_p2 += 1
        row_p2 = min(NUM_ROWS - 1, row_p2)

    elif player == 2 and key == 1:  # left
        col_p2 -= 1
        col_p2 = max(0, col_p2)

    elif player == 2 and key == 2:  # right
        col_p2 += 1
        col_p2 = min(NUM_COLS - 1, col_p2)

    elif player == 2 and key == 10:  # select character
        player2_selected = True


# Websocket server
async def websocket_server(websocket, path):
    print('connection established')
    global player1_connected
    global player2_connected
    global custom_data

    if trigger.is_set():
        return

    asyncio.create_task(end_connection(websocket))

    try:
        async for message in websocket:


            if trigger.is_set():
                return
            
            if is_valid_json(message) == 0:
                await websocket.send(message)
                return

            event = json.loads(message)
            player = event.get("player")
            key = event.get("control")
            print(f"{player} : {key}")
            if player == 1:
                player1_connected = True
            elif player == 2:
                player2_connected = True

            if select_screen:
                move_on_grid(player, key)

            elif run and not select_screen:
                custom_data = np.array(
                    [
                        (key == 1) & (player == 1),
                        (key == 2) & (player == 1),
                        (key == 3) & (player == 1),
                        (key == 4) & (player == 1),
                        (key == 5) & (player == 1),
                        (key == 1) & (player == 2),
                        (key == 2) & (player == 2),
                        (key == 3) & (player == 2),
                        (key == 4) & (player == 2),
                        (key == 5) & (player == 2),
                        (key == 6) & (player == 1),  # health boost
                        (key == 6) & (player == 2),
                        (key == 7) & (player == 1),  # invincible
                        (key == 7) & (player == 2),
                    ]
                )

            else:
                pass

    except websockets.exceptions.ConnectionClosedError:
        pass


# Start WebSocket server
ip = get_ipv4_address()
if ip is None:
    ip = "localhost"

start_server = websockets.serve(websocket_server, ip, 8765)

asyncio.get_event_loop().run_until_complete(start_server)

# Encoded ip
key = "battleblade"
alphabet = "0123456789.abcdefghijklmnopqrstuvwxyz"
if ip != "localhost":
    enc_ip = encrypt(ip, key, alphabet)
else:
    enc_ip = "Offline : localhost"

flag_start = False
start_update = pygame.time.get_ticks()
print("\nWelcome to BattleBlade")
# start_screen loop
font=230
curr_font = pygame.font.Font("assets/fonts/afogand.ttf", font)
alpha=0
while start_screen:

    clock.tick(FPS)

    # draw background and text
    # draw_bg(bg_ind)
    intro_sound.play()
  
    transition_update = pygame.time.get_ticks()
  
    while(font>=70):
        draw_text("BattleBlade", curr_font, ORANGE,-50+alpha, (SCREEN_HEIGHT / 5))
        pygame.display.update()
        curr_font=pygame.font.Font("assets/fonts/afogand.ttf", font)
        if(pygame.time.get_ticks()-transition_update >=15):
            draw_text("BattleBlade", curr_font, ORANGE, -50+alpha, SCREEN_HEIGHT / 5)
            alpha+=(323/150)
            pygame.display.update()
            screen.fill((0,0,0))
            pygame.display.update()
            font-=1
            transition_update = pygame.time.get_ticks()
    draw_text("BattleBlade", curr_font, ORANGE, -50+alpha, SCREEN_HEIGHT / 5)
    # draw_text("Press Space to Start", command_font, ORANGE, (SCREEN_WIDTH / 3)-25 , (SCREEN_HEIGHT / 5)+70)
  
    draw_text(
        "Get ready for the Ultimate Battle",
        command_font,
        RED,
        SCREEN_WIDTH / 4 - 60,
        SCREEN_HEIGHT / 3,
    )
    draw_text(
        "Enter code to connect",
        command_font,
        RED,
        SCREEN_WIDTH / 4 + 50,
        SCREEN_HEIGHT / 2,
    )
    draw_text(
        enc_ip, simple_font, YELLOW, SCREEN_WIDTH / 4 + 100, SCREEN_HEIGHT / 2 + 50
    )

    # Automatically start game once both connected
    if player1_connected and player2_connected:
        if not flag_start:
            flag_start = True
            start_update = pygame.time.get_ticks()
        if flag_start and (pygame.time.get_ticks() - start_update) >= 3000:
            select_screen = True
            start_screen = False

    # Green symbol if connected otherwise red
    if player1_connected:
        screen.blit(green_wifi, (200, 410))
    else:
        screen.blit(red_wifi, (200, 410))

    if player2_connected:
        screen.blit(green_wifi, (700, 410))
    else:
        screen.blit(red_wifi, (700, 410))

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_screen = False

    asyncio.get_event_loop().run_until_complete(asyncio.sleep(0))

    # update display
    pygame.display.update()

flag_select = False
select_update = pygame.time.get_ticks()
# select screen loop
while select_screen:

    clock.tick(FPS)
    intro_sound.stop()
    screen.fill((0,0,0))
    # draw background and grid
    # draw_bg(bg_ind)
    draw_thumbnails()
    pygame.draw.rect(screen, RED, (250, 50, HI_WIDTH, HI_HEIGHT))
    pygame.draw.rect(screen, RED, (240, 300, HI_WIDTH+20, 50))
    pygame.draw.rect(screen, YELLOW, (575, 50, HI_WIDTH, HI_HEIGHT))
    pygame.draw.rect(screen, YELLOW, (565, 300, HI_WIDTH + 40, 50))
    p1_ind = row_p1 * NUM_COLS + col_p1
    p2_ind = row_p2 * NUM_COLS + col_p2

    # render highlighted image
    if p1_ind < len(highlight_list):
        screen.blit(highlight_list[p1_ind], (250, 50))
        draw_text(characters[p1_ind].name, command_font, YELLOW, 260, 300)
    else:
        pygame.draw.rect(screen, RED, (250, 50, HI_WIDTH, HI_HEIGHT))
    if p2_ind < len(highlight_list):
        screen.blit(
            pygame.transform.flip(highlight_list[p2_ind], True, False), (575, 50)
        )
        draw_text(characters[p2_ind].name, command_font, RED, 585, 300)
    else:
        pygame.draw.rect(screen, YELLOW, (575, 50, HI_WIDTH, HI_HEIGHT))

    # highlight selected rectangle
    screen.blit(vs, (425, 150))
    x1 = X0 + col_p1 * (HORI_SP + BOX_SIZE)
    y1 = Y0 + row_p1 * (VER_SP + BOX_SIZE)
    pygame.draw.rect(screen, RED, (x1, y1, BOX_SIZE, BOX_SIZE), SHIFT // 2)
    x2 = X0 + col_p2 * (HORI_SP + BOX_SIZE)
    y2 = Y0 + row_p2 * (VER_SP + BOX_SIZE)

    if x1 == x2 and y1 == y2:
        pygame.draw.rect(screen, ORANGE, (x2, y2, BOX_SIZE, BOX_SIZE), SHIFT // 2)

    else:
        pygame.draw.rect(screen, YELLOW, (x2, y2, BOX_SIZE, BOX_SIZE), SHIFT // 2)

    # break out if both have selected their characters

    if player1_selected and player2_selected:
        if not flag_select:
            flag_select = True
            select_update = pygame.time.get_ticks()
        if flag_select and (pygame.time.get_ticks() - select_update) >= 1500:
            select_screen = False
            run = True
            last_count_update = pygame.time.get_ticks()

    # key = pygame.key.get_pressed()

    # if key[pygame.K_KP1]:
    #     select_screen = False
    #     run = True
    #     last_count_update = pygame.time.get_ticks()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            select_screen = False

    asyncio.get_event_loop().run_until_complete(asyncio.sleep(0))

    # update display
    pygame.display.update()

# create two instances of fighters
if p1_ind >= 7:
    p1_ind = 0
if p2_ind >= 7:
    p2_ind = 1
sprites = [characters[p1_ind], characters[p2_ind]]
fighter_1 = Fighter(
    1,
    200,
    310,
    False,
    sprites[0].data,
    sprites[0].sheet,
    sprites[0].animation_steps,
    sprites[0].audio,
)
fighter_2 = Fighter(
    2,
    700,
    310,
    True,
    sprites[1].data,
    sprites[1].sheet,
    sprites[1].animation_steps,
    sprites[1].audio,
)


while run:

    clock.tick(FPS)

    # draw background
    draw_bg(bg_ind)

    # show player stats
    draw_health_bar(fighter_1.health, 20, 20, 1)
    draw_health_bar(fighter_2.health, 580, 20, 2)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)
    display_boost(score_font, ORANGE, 120, 60, fighter_1.health_boost)
    display_boost(score_font, ORANGE, 640, 60, fighter_2.health_boost)
    # update countdown
    if intro_count <= 0:
        # move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_2, round_over, custom_data)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_1, round_over, custom_data)
        custom_data = np.array(
            [
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
            ]
        )

    elif intro_screen:
        # show round no
        draw_text(
            (f"Round : {round_count}"),
            large_font,
            RED,
            SCREEN_WIDTH / 3,
            SCREEN_HEIGHT / 3,
        )
        if (pygame.time.get_ticks() - last_count_update) >= 1500:
            intro_screen = False
            last_count_update = pygame.time.get_ticks()
    else:
        # display count timer
        if(intro_count==4):
            countdown_sound.play()
        if(intro_count>=2):
            draw_text(str((intro_count)-1), large_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        #update count timer
        if(intro_count==1):
            draw_text("FIGHT!", large_font, RED, (SCREEN_WIDTH / 2)-70, SCREEN_HEIGHT / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # update fighters
    fighter_1.update()
    fighter_2.update()

    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    fighter_1.draw_timer(screen, 100, 80, 20)
    fighter_2.draw_timer(screen, 670, 80, 20)
    # check for player defeat
    if round_over == False:
        # if player1 is dead => increase score of player2
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        # if player2 is dead => increase score of player1
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # display victory image for cooldown time
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            # if game is won by some player, exit to winner screen
            if score[0] == (rounds // 2 + 1) or score[1] == (rounds // 2 + 1):
                if score[0] == (rounds // 2 + 1):
                    winner = 1
                else:
                    winner = 2
                run = False
                winner_screen = True
                trigger.set()  # game over trigger

            # else continue with next round
            else:
                round_count += 1
                round_over = False
                bg_ind = (bg_ind + 1) % len(bg_img_list)
                intro_screen = True
                intro_count = 4
                last_count_update = pygame.time.get_ticks()
                fighter_1 = Fighter(
                    1,
                    200,
                    310,
                    False,
                    sprites[0].data,
                    sprites[0].sheet,
                    sprites[0].animation_steps,
                    sprites[0].audio,
                )
                fighter_2 = Fighter(
                    2,
                    700,
                    310,
                    True,
                    sprites[1].data,
                    sprites[1].sheet,
                    sprites[1].animation_steps,
                    sprites[1].audio,
                )

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    asyncio.get_event_loop().run_until_complete(asyncio.sleep(0))

    # update display
    pygame.display.update()

# winner_screen loop
while winner_screen:

    clock.tick(FPS)

    # draw background and text
    # draw_bg(bg_ind)
    screen.fill((0,0,0))
    draw_text(
        f"P-{winner} : {sprites[winner-1].name} wins !!!",
        large_font,
        RED,
        (SCREEN_WIDTH / 3)-60,
        SCREEN_HEIGHT / 3,
    )
    draw_text(
        "Press Space to Exit",
        command_font,
        RED,
        SCREEN_WIDTH / 3 + 10,
        (SCREEN_HEIGHT / 3) + 100,
    )

    # break out if space pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        winner_screen = False

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            winner_screen = False

    asyncio.get_event_loop().run_until_complete(asyncio.sleep(0))

    # update display
    pygame.display.update()


# exit pygame
pygame.quit()
