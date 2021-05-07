import pygame
import numpy as np
from PPdraft_grid_algorithm import adj_tiles, maze_algorithm
import AI_v2
import time

grid_size = 4

pygame.init()
pygame.font.init()
# window setup 720p
display_width = 960
display_height = 720
# colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (110, 102, 91)
# initialise game window
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Cavescapes')
# clock setup

clock = pygame.time.Clock()

game_end = False
# resources
path_img_orig = pygame.image.load('Resources/Path_ppgame.png')
lava_img_orig = pygame.image.load('Resources/Lava_ppgame.png')
portal_1_img_orig = pygame.image.load('Resources/Portal_1_ppgame.png')
portal_2_img_orig = pygame.image.load('Resources/Portal_2_ppgame.png')
dirt_path_img_orig = pygame.image.load('Resources/dirt_path_ppgame.png')
goal_img_orig = pygame.image.load('Resources/goal_ppgame.png')
skull_img_orig = pygame.image.load("Resources/skull_ppgame.png")
button_img_orig = pygame.image.load('Resources/button_ppgame.png')
button1_img_orig = pygame.image.load('Resources/button1_ppgame.png')
fast_img_orig = pygame.image.load('Resources/fast_ppgame.png')
fast1_img_orig = pygame.image.load('Resources/fast1_ppgame.png')
change_view_img_orig = pygame.image.load('Resources/change_view_ppgame.png')
change_view1_img_orig = pygame.image.load('Resources/change_view1_ppgame.png')
success_img_orig = pygame.image.load("Resources/success.png")
nextlvl_img_orig = pygame.image.load("Resources/next_level.png")

up_orig = pygame.image.load("Resources/sprites/up.png")
down_orig =pygame.image.load("Resources/sprites/down.png")
left_orig = pygame.image.load("Resources/sprites/left.png")
right_orig = pygame.image.load("Resources/sprites/right.png")

# intialise variables
size = (4*grid_size, 3*grid_size)
player_size = int((display_width/size[0])*7/8)
skull_scaling = (display_height, display_height)
button_scaling = (73,50)
end_screen_scaling = (int((3/4)*display_width),int(((3/4)*display_width)*(13/45)))

up_pic = pygame.transform.scale(up_orig, (int(player_size/2), player_size))
down_pic = pygame.transform.scale(down_orig, (int(player_size/2), player_size))
left_pic = pygame.transform.scale(left_orig, (int(player_size/2), player_size))
right_pic = pygame.transform.scale(right_orig, (int(player_size/2), player_size))

skull = pygame.transform.scale(skull_img_orig, skull_scaling)
button = pygame.transform.scale(button_img_orig, button_scaling)
button1 = pygame.transform.scale(button1_img_orig, button_scaling)
fast = pygame.transform.scale(fast_img_orig, button_scaling)
fast1 = pygame.transform.scale(fast1_img_orig, button_scaling)
change_view = pygame.transform.scale(change_view_img_orig, button_scaling)
change_view1 = pygame.transform.scale(change_view1_img_orig, button_scaling)
success = pygame.transform.scale(success_img_orig, (int((3/4)*display_width),int(((3/4)*display_width)*(13/45))))
next_level = pygame.transform.scale(nextlvl_img_orig, (int((3/4)*display_width),int(((3/4)*display_width)*(13/45))))
pygame.font.init()
player_spawnpoint = (0,0)
while player_spawnpoint[0] % 2 != 0 :
    player_spawnpoint[0] = np.random.randint(0, size[0])
while player_spawnpoint[1] % 2 != 0:
    player_spawnpoint[1] = np.random.randint(0, size[1])


def multi_grid(array):
    # arrays mirror the grid layout, must be of matrix form
    array_size = np.shape(array)
    global grid_size
    grid_size = array_size[1]
    global multi_block_size
    multi_block_size = display_height / array_size[1]
    global data_list
    data_list = []
    # image scaling
    scale_factor = (int(multi_block_size), int(multi_block_size))
    dirt_path_img = pygame.transform.scale(dirt_path_img_orig, scale_factor)
    stone_path_img = pygame.transform.scale(path_img_orig, scale_factor)
    lava_img = pygame.transform.scale(lava_img_orig, scale_factor)
    portal1_img = pygame.transform.scale(portal_1_img_orig, scale_factor)
    portal2_img = pygame.transform.scale(portal_2_img_orig, scale_factor)
    goal_img = pygame.transform.scale(goal_img_orig, scale_factor)
    '''
    Indexes for block types:
    dirt path = 0
    stone path = 1
    lava = 2
    portal_1 = 3
    portal_2 = 4
    goal = 5
    If adding a new block type add the resources above this comment
    update the chain of ifs below
    make sure to add into the grid algorithm
    '''
    for index_with_value in np.ndenumerate(array):
        data_list.append(index_with_value)
    i = 0
    for pos_and_type in data_list:
        block_pos = (int(pos_and_type[0][0] * multi_block_size), int(pos_and_type[0][1] * multi_block_size))
        data_list[i] = (block_pos, pos_and_type[1])
        i += 1
    for pixel_position_and_type in data_list:
        blit_position = pixel_position_and_type[0]
        block_type = pixel_position_and_type[1]
        # add in block types here
        if block_type == 0:
            gameDisplay.blit(dirt_path_img, blit_position)
        if block_type == 1:
            gameDisplay.blit(stone_path_img, blit_position)
        if block_type == 2:
            gameDisplay.blit(lava_img, blit_position)
        if block_type == 3:
            gameDisplay.blit(portal1_img, blit_position)
        if block_type == 4:
            gameDisplay.blit(portal2_img, blit_position)
        if block_type == 5:
            gameDisplay.blit(goal_img, blit_position)


def display_player(vector, dir):

    ts = down_pic
    if dir == "up":
        ts = up_pic
    elif dir == "down":
        ts = down_pic
    elif dir == "left":
        ts = left_pic
    elif dir == "right":
        ts = right_pic

    gameDisplay.blit(ts, (int(vector[0] * multi_block_size + (multi_block_size - player_size/2) / 2), int(vector[1] * multi_block_size + (multi_block_size - player_size) / 2)))



def find_block(type, world):
    return np.where(world == type)


def quit_game():
    pygame.quit()
    quit()

def player_view(location):

    blit_loc = (int((location[0] * multi_block_size) + multi_block_size / 2),int((location[1] * multi_block_size)) + multi_block_size / 2)
    radius = 0.85 * multi_block_size
    view = pygame.Surface((display_width,display_height))
    view.fill(black)
    pygame.draw.circle(view, white, blit_loc, radius)
    gameDisplay.blit(view, (0,0), special_flags=3)


def flash_screen(string):
    if string == "death":
        pygame.draw.rect(gameDisplay, black, ((0,0), (display_width, display_height)))
        gameDisplay.blit(skull, ((display_width/2) - (skull_scaling[0]/2), 0))
        pygame.display.update()
        time.sleep(0.3)
    elif string == "success":
        pygame.draw.rect(gameDisplay, (0,251,176), ((0,0), (display_width, display_height)))
        pygame.display.update()
        time.sleep(0.3)
        gameDisplay.blit(success, ((display_width/2)-(end_screen_scaling[0]/2), display_height*1/8))
        pygame.display.update()
        time.sleep(0.3)
        gameDisplay.blit(next_level, ((display_width/2)-(end_screen_scaling[0]/2), (display_height*7/8 - end_screen_scaling[1])))
        pygame.display.update()
        time.sleep(0.5)



# declaring the AI
agent_v2 = AI_v2.agent(0.01,size, 2, 5)
# AI @ ai.py


def game_loop(**kwargs): # args1 = AI_ACTIVE, args2 = FAST_ACTIVE, args4 = RESET_ARRAY
    player_location = player_spawnpoint
    global random_array
    global seed
    direction = "down"
    loc1 = ()
    loc2 = ()
    hasMoved = True
    #below is the button variables
    AI_ACTIVE = False
    if "ai_key" in kwargs:
        AI_ACTIVE = kwargs['ai_key']
    FAST_ACTIVE = False
    if "fast_key" in kwargs:
        FAST_ACTIVE = kwargs["fast_key"]
    PLAYER_VIEW_ACTIVE = False
    if "player_view_key" in kwargs:
        PLAYER_VIEW_ACTIVE = kwargs["player_view_key"]
    if "reset_array" in kwargs:
        if kwargs["reset_array"] == True:
            seed = np.random.randint(low=0, high=1000)
            random_array = maze_algorithm(size, seed)

    while not game_end:
        # the helper tool to display the grid
        multi_grid(random_array)

        # the button coordinates
        button_coors = pygame.rect.Rect((display_width * 9 / 10, display_height / 20),(display_width / 8, display_height / 10))
        fast_coors = pygame.rect.Rect((display_width * 9 / 10, (display_height / 20)+50),(display_width / 8, display_height / 10))
        change_view_coors = pygame.rect.Rect((display_width * 9 / 10, (display_height / 20)+100),(display_width / 8, display_height / 10))

        if not FAST_ACTIVE:
            speed = 0.2
            fps = 30
        elif FAST_ACTIVE:
            speed = 0
            fps = 240

        # the movement of the AI, coding under assumption that the map resets after every loss
        # new game if its a loss
        ai_play = True
        simplfied_tiles = []
        if AI_ACTIVE and ai_play:
                reward = 0
                if int(random_array[player_location]) == 0 or 1 or 3 or 4:
                    reward = -0.01
                if int(random_array[player_location]) == 2:
                    reward = -5
                if int(random_array[player_location]) == 5:
                    reward = 5
                simplfied_tiles = [int(random_array[x]) for x in adj_tiles(player_location,size)]
                for index, x in enumerate(simplfied_tiles):
                    if x == 0:
                        simplfied_tiles[index] = 1
                    if x == 4:
                        simplfied_tiles[index] = 3
                action = agent_v2.play(reward, [int(random_array[player_location]), player_location], simplfied_tiles)
                # move
                if action == 1:
                    time.sleep(speed)
                    player_location = (player_location[0], player_location[1] - 1)
                    direction = "up"
                elif action == 2:
                    time.sleep(speed)
                    player_location = (player_location[0], player_location[1] + 1)
                    direction = "down"
                elif action == 3:
                    time.sleep(speed)
                    player_location = (player_location[0] - 1, player_location[1])
                    direction = "left"
                elif action == 4:
                    time.sleep(speed)
                    player_location = (player_location[0] + 1, player_location[1])
                    direction = "right"
                # if dead, break
                ai_play = False



        # block controls for the portal, lava and goal
        if int(random_array[player_location]) == 3:
            if AI_ACTIVE:
                agent_v2.updateValues(-0.01, [3, player_location], simplfied_tiles)
            player_location = find_block(4, random_array)
            random_array[player_location] = 0
            random_array[find_block(3, random_array)] = 0
        if int(random_array[player_location]) == 4:
            if AI_ACTIVE:
                agent_v2.updateValues(-0.01, [3, player_location], simplfied_tiles)
            player_location = find_block(3, random_array)
            random_array[player_location] = 0
            random_array[find_block(4, random_array)] = 0
        if int(random_array[player_location]) in [2, 5]:
            if AI_ACTIVE:
                reward = 0
                if int(random_array[player_location]) == 2:
                    reward = -5
                if int(random_array[player_location]) == 5:
                    reward = 5
                agent_v2.updateValues(reward, [int(random_array[player_location]), player_location], simplfied_tiles)
            if int(random_array[player_location]) == 2:
                flash_screen("death")
                game_loop(ai_key=AI_ACTIVE, fast_key=FAST_ACTIVE, player_view_key=PLAYER_VIEW_ACTIVE, reset_array=False)
            if int(random_array[player_location]) == 5:
                agent_v2.game_over()
                flash_screen("success")
                game_loop(ai_key=AI_ACTIVE, fast_key=FAST_ACTIVE, player_view_key=PLAYER_VIEW_ACTIVE, reset_array=True)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            # keypress inputs
            keys_pressed = pygame.key.get_pressed()
            # up down left right
            if keys_pressed[pygame.K_DOWN] and player_location[1] != grid_size - 1 and not (
                    keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_RIGHT]):
                player_location = (player_location[0], player_location[1] + 1)
                direction = "down"
            if keys_pressed[pygame.K_LEFT] and player_location[0] != 0 and not (
                    keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_RIGHT]):
                player_location = (player_location[0] - 1, player_location[1])
                direction = "left"
            if keys_pressed[pygame.K_RIGHT] and player_location[0] != grid_size * 4 / 3 - 1 and not (
                    keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_DOWN]):
                player_location = (player_location[0] + 1, player_location[1])
                direction = "right"
            if keys_pressed[pygame.K_UP] and player_location[1] != 0 and not (
                    keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_RIGHT]):
                player_location = (player_location[0], player_location[1] - 1)
                direction = "up"


            # buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_coors.collidepoint(mouse_pos):
                    AI_ACTIVE = not AI_ACTIVE
                if fast_coors.collidepoint(mouse_pos):
                    FAST_ACTIVE = not FAST_ACTIVE
                if change_view_coors.collidepoint(mouse_pos):
                    PLAYER_VIEW_ACTIVE = not PLAYER_VIEW_ACTIVE

        # button textures for player view button
        if not PLAYER_VIEW_ACTIVE:
            gameDisplay.blit(change_view, change_view_coors)
        elif PLAYER_VIEW_ACTIVE:
            player_view(player_location) # stuffed in the view code as well
            gameDisplay.blit(change_view1, change_view_coors)
        # button textures for AI button
        if not AI_ACTIVE:
            gameDisplay.blit(button, button_coors)
        elif AI_ACTIVE:
            gameDisplay.blit(button1, button_coors)

        # button textures for fast learn button and the speed and fps settings.
        if not FAST_ACTIVE:
            gameDisplay.blit(fast, fast_coors)

        elif FAST_ACTIVE:
            gameDisplay.blit(fast1, fast_coors)
        display_player(player_location, direction)
        pygame.display.update()
        clock.tick(fps)

game_loop(reset_array = True, player_view_key=True)
