import numpy as np

# use the size as a tuple, width, height
# set seed to none for random seed

def adj_tiles(location, grid_size):
    adj_list = []
    adj_up = (location[0], location[1] - 1)
    if not (adj_up[0]<0 or adj_up[1]<0 or adj_up[0]>grid_size[0]-1 or adj_up[1]>grid_size[1]-1):
        adj_list.append(adj_up)
    adj_down = (location[0], location[1] + 1)
    if not (adj_down[0]<0 or adj_down[1]<0 or adj_down[0]>grid_size[0]-1 or adj_down[1]>grid_size[1]-1):
        adj_list.append(adj_down)
    adj_left = (location[0] - 1, location[1])
    if not (adj_left[0]<0 or adj_left[1]<0 or adj_left[0]>grid_size[0]-1 or adj_left[1]>grid_size[1]-1):
        adj_list.append(adj_left)
    adj_right = (location[0] + 1, location[1])
    if not (adj_right[0]<0 or adj_right[1]<0 or adj_right[0]>grid_size[0]-1 or adj_right[1]>grid_size[1]-1):
        adj_list.append(adj_right)
    return adj_list

def maze_algorithm(size, seed):
    gridworld = 2 * np.ones(size)
    path_blocks = []
    for index, tile in np.ndenumerate(gridworld): # every 2 tiles will be a path
        if index[0] % 2 == 0 and index[1] % 2 == 0:
            gridworld[index] = 0
            path_blocks.append(index)
    global pointer
    pointer = path_blocks[np.random.randint(0, len(path_blocks))] # the current place being evaluated
    tracked_tiles = [pointer]

    def directions(location):
        directions = []
        adj_up = (location[0], location[1] - 2)
        if not (adj_up[0]<0 or adj_up[1]<0 or adj_up[0]>size[0]-1 or adj_up[1]>size[1]-1):
            if adj_up not in tracked_tiles:
                directions.append("up")


        adj_down = (location[0], location[1] + 2)
        if not (adj_down[0]<0 or adj_down[1]<0 or adj_down[0]>size[0]-1 or adj_down[1]>size[1]-1):
            if adj_down not in tracked_tiles:
                directions.append("down")

        adj_left = (location[0] - 2, location[1])
        if not (adj_left[0]<0 or adj_left[1]<0 or adj_left[0]>size[0]-1 or adj_left[1]>size[1]-1):
            if adj_left not in tracked_tiles:
                directions.append("left")


        adj_right = (location[0] + 2, location[1])
        if not (adj_right[0]<0 or adj_right[1]<0 or adj_right[0]>size[0]-1 or adj_right[1]>size[1]-1):
            if adj_right not in tracked_tiles:
                directions.append("right")
        return directions

    end = False # checks if recursion is finished
    while end == False:
        # finding the tiles that are valid
        actions = directions(pointer)

        if len(actions) > 0:
            move = np.random.choice(actions)
            # changing pointer and updating gridworld
            if move == "up":
                pointer = (pointer[0], pointer[1]-1)
                gridworld[pointer] = 0
                pointer = (pointer[0], pointer[1]-1)

            elif move == "down":
                pointer = (pointer[0], pointer[1]+1)
                gridworld[pointer] = 0
                pointer = (pointer[0], pointer[1]+1)

            elif move == "left":
                pointer = (pointer[0]-1, pointer[1])
                gridworld[pointer] = 0
                pointer = (pointer[0]-1, pointer[1])

            elif move == "right":
                pointer = (pointer[0]+1, pointer[1])
                gridworld[pointer] = 0
                pointer = (pointer[0]+1, pointer[1])
            tracked_tiles.append(pointer)
        else:
            index = tracked_tiles.index(pointer)
            while len(directions(pointer)) == 0: # the backtracking
                if index == -1:
                    end = True # the end signal
                    break
                pointer = tracked_tiles[index]
                index -= 1

    portal1 = path_blocks[np.random.randint(0, len(path_blocks))]
    portal2 = path_blocks[np.random.randint(0, len(path_blocks))]
    while portal2 == portal1:
        portal2 = path_blocks[np.random.randint(0, len(path_blocks))]
    goal = path_blocks[np.random.randint(0, len(path_blocks))]
    while goal == portal1 or goal == portal2:
        goal = path_blocks[np.random.randint(0, len(path_blocks))]
    gridworld[goal] = 5
    gridworld[portal1] =  3
    gridworld[portal2] = 4

    return gridworld
