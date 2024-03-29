import pygame
from fighter import Fighter
import websockets
import json
import asyncio
import numpy as np

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

# define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

# load background image
# bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# load spritesheets
warrior_sheet = pygame.image.load(
    "assets/images/warrior/Sprites/warrior.png"
).convert_alpha()
wizard_sheet = pygame.image.load(
    "assets/images/wizard/Sprites/wizard.png"
).convert_alpha()

# load victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# define font
large_font = pygame.font.Font("assets/fonts/turok.ttf", 70)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
command_font = pygame.font.Font("assets/fonts/turok.ttf", 40)


# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


# function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


# define game variables
round_count = 1
intro_screen = True
intro_count = 3
score = [0, 0]  # player scores: [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
last_count_update = pygame.time.get_ticks()
winner = 0
player1_connected = False
player2_connected = False
# define loop variables
start_screen = True
run = False
winner_screen = False

# create two instances of fighters
fighter_1 = Fighter(
    1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx
)
fighter_2 = Fighter(
    2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx
)

# dictionary for player commands
# global custom_data
custom_data = np.full(10, False)

cnt = 0


# Websocket server
async def websocket_server(websocket, path):
    global player1_connected
    global player2_connected
    global custom_data
    global cnt
    # player_number = await websocket.recv()
    # if player_number == "1":
    #     player1_connected = True
    # elif player_number == "2":
    #     player2_connected = True
    try:
        async for message in websocket:

            msg = json.loads(message)
            player = msg.get("player")
            if player == 1:
                player1_connected = True

            elif player == 2:
                player2_connected = True

            key = msg.get("control")
            print(cnt)
            cnt += 1
            print(f"{player} : {key}")
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
                ]
            )
            print(f"Received : {custom_data}")
            if winner_screen and not run:  # If the game has ended
                await websocket.close()  # Close the WebSocket connection
                break  # Break the loop

    except websockets.exceptions.ConnectionClosedError:
        pass


# Start WebSocket server
start_server = websockets.serve(websocket_server, "10.81.73.10", 8765)

asyncio.get_event_loop().run_until_complete(start_server)

flag = False
first_update = pygame.time.get_ticks()
# start_screen loop
while start_screen:

    clock.tick(FPS)

    # draw background and text
    draw_bg()
    draw_text("BattleBlade", large_font, YELLOW, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 5)
    # draw_text("Get ready for the Ultimate battle", large_font, RED, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3)
    draw_text(
        "Get ready for the Ultimate battle",
        # "Press Space to Start",
        command_font,
        RED,
        SCREEN_WIDTH / 4,
        (SCREEN_HEIGHT / 2),
    )

    if player1_connected and player2_connected:
        if not flag:
            flag = True
            first_update = pygame.time.get_ticks()
        if flag and (pygame.time.get_ticks() - first_update) >= 5000:
            run = True
            start_screen = False
            # first_update = pygame.time.get_ticks()
            last_count_update = pygame.time.get_ticks()
            # time.sleep(10)

    if player1_connected:
        draw_text(
            "Player 1 connected!",
            command_font,
            RED,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 3,
        )

    if player2_connected:
        draw_text(
            "Player 2 connected!",
            command_font,
            RED,
            SCREEN_WIDTH / 6,
            SCREEN_HEIGHT / 3 + 50,
        )

    # break out if space pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        run = True
        start_screen = False
        last_count_update = pygame.time.get_ticks()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_screen = False

    asyncio.get_event_loop().run_until_complete(asyncio.sleep(0))

    # update display
    pygame.display.update()
# game loop
while run:

    clock.tick(FPS)

    # draw background
    draw_bg()

    # show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    # update countdown
    if intro_count <= 0:
        # move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_2, round_over, custom_data)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_1, round_over, custom_data)
        # for i in range(0, 10):
        #     if custom_data[i]:
        #         print("Resetting")
        #         break
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
        draw_text(
            str(intro_count), large_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3
        )
        # update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # update fighters
    fighter_1.update()
    fighter_2.update()

    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

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
            if score[0] == 2:
                winner = 1
                run = False
                winner_screen = True
            elif score[1] == 2:
                winner = 2
                run = False
                winner_screen = True
            # else continue with next round
            else:
                round_count += 1
                round_over = False
                intro_screen = True
                intro_count = 3
                last_count_update = pygame.time.get_ticks()
                fighter_1 = Fighter(
                    1,
                    200,
                    310,
                    False,
                    WARRIOR_DATA,
                    warrior_sheet,
                    WARRIOR_ANIMATION_STEPS,
                    sword_fx,
                )
                fighter_2 = Fighter(
                    2,
                    700,
                    310,
                    True,
                    WIZARD_DATA,
                    wizard_sheet,
                    WIZARD_ANIMATION_STEPS,
                    magic_fx,
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
    draw_bg()
    draw_text(
        f"Player {winner} wins !!!",
        large_font,
        RED,
        SCREEN_WIDTH / 3,
        SCREEN_HEIGHT / 3,
    )
    draw_text(
        "Press Space to Exit",
        command_font,
        RED,
        SCREEN_WIDTH / 3 + 10,
        (SCREEN_HEIGHT / 3) + 70,
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