import numpy as np
import random

'''
This is the second AI. It follows a monte-carlo learning method and is made from scratch. This is coded specifically for the game. Major changes from version 1 are listed below:
 - States are now only the type of block and are used as a "tag" for certain deterministic in-game states (the tiles you can land on)
 - It is adaptable to use deterministic movements such as the movement to lava and path tiles but also allows for changing averages for portal tiles.
 - no more action-specific values, this only follows the v(s) (values for states exclusively), with more tiles gradually being "revealed"
 - actions are now direct mappings to tiles, which map to the average rewards. The v(s) denometed here does not take into account the future state, instead, this is computed directly in the decision function
 - added a lookup table which is basically a mapping of all the seen tiles, used as weighting for pathfinding (below).
 - to encourage following new paths, the more times a specific block is visted, the greater the penality, and tiles that have not been stepped on are seen as more desirable.
 - instead of thinking of each tile as inherently different, we tell it that a tile of the same types have the same function (ie: a lava tile - despite it's location - will still affect you the same way as any other lava tiles). This is the key improvement of this version of the AI

Dev notes:
state given is a list: [type_of_block, (location)]
adj_tiles = [up,down,left,right] TYPE OF BLOCK, skip tile out-of-bounds


actions:
1 - up
2 - down
3 - left
4 - right
'''

class agent:
    def __init__(self, elipson, grid_size, unseen_weighting, unk_weighting):
        # initalising
        self.states = [] # just a refrence list for the number of states (used to convert state to the index used in the rest of the code)
        self.values = [] # can change to a random selection (check which is best performing)
        self.steps = [] # used for computing the running average
        self.loc_steps = np.zeros(grid_size) # used to track the amount of steps in a location and to discourage visiting the same states
        self.lookup = np.full(grid_size, None) #this is the lookup grid
        self.unseen_weighting = unseen_weighting # the weighting (usually x>1) to unseen tiles to encourage (or discourage) new pathfinding
        self.elipson = elipson # explore vs. exploit used as the confidencelevel parameter in UCB
        self.tmp = True # to provoke random action on first move
        self.grid_size = grid_size # to find valid actions
        self.unk_weighting = unk_weighting # the bonus added to value for an unseen state/block

    def game_over(self): # this seems stupid but it declutters the main code and is less memory intensive than other solutions. This function should be called at the end of a game(episode) and erases the memory of the lookup array to avoid confusion for a new game.
        self.lookup = np.full(self.grid_size, None)
        self.loc_steps = np.zeros(self.grid_size)

    def play(self, reward, state, adj_tiles):
        block_type = state[0]
        location = state[1]
        self.lookup[location] = block_type # adding entry to the lookup grid
        self.loc_steps[location]+=1

        for tile in adj_tiles: #adding the adj_tiles to states
            if tile not in self.states:
                self.states.append(tile)

        if len(self.states) > len(self.values): # if the value length is not state length or if the value length is state length but the value is not documented
            if block_type not in self.states:
                self.states.append(block_type) #adding the block type to the state
            state_index = self.states.index(block_type)   # match index of values to the index in states
            while len(self.values) < len(self.states):# matching the length of values to the states
                self.values.append("NO_VALUE")
            while len(self.steps) < len(self.states):# matching the length of steps to the states
                self.steps.append(0)
            self.values[state_index] = reward
            self.steps[state_index] += 1


        elif block_type not in self.states or self.values[self.states.index(block_type)] == "NO_VALUE": # to avoid doing an invalid check and crashing
            if block_type not in self.states:
                self.states.append(block_type) #adding the block type to the state
            state_index = self.states.index(block_type)   # match index of values to the index in states
            while len(self.values) < len(self.states):# matching the length of values to the states
                self.values.append("NO_VALUE")
            while len(self.steps) < len(self.states):# matching the length of steps to the states
                self.steps.append(0)
            self.values[state_index] = reward
            self.steps[state_index] += 1


        valid_actions = [] #calculating the valid actions
        adj_up = (location[0], location[1] - 1)
        if not (adj_up[0]<0 or adj_up[1]<0 or adj_up[0]>self.grid_size[0]-1 or adj_up[1]>self.grid_size[1]-1):
            valid_actions.append("up")
        else:
            valid_actions.append("invalid")
        adj_down = (location[0], location[1] + 1)
        if not (adj_down[0]<0 or adj_down[1]<0 or adj_down[0]>self.grid_size[0]-1 or adj_down[1]>self.grid_size[1]-1):
            valid_actions.append("down")
        else:
            valid_actions.append("invalid")
        adj_left = (location[0] - 1, location[1])
        if not (adj_left[0]<0 or adj_left[1]<0 or adj_left[0]>self.grid_size[0]-1 or adj_left[1]>self.grid_size[1]-1):
            valid_actions.append("left")
        else:
            valid_actions.append("invalid")
        adj_right = (location[0] + 1, location[1])
        if not (adj_right[0]<0 or adj_right[1]<0 or adj_right[0]>self.grid_size[0]-1 or adj_right[1]>self.grid_size[1]-1):
            valid_actions.append("right")
        else:
            valid_actions.append("invalid")

        action_list =[] # order : [up, down, left, right]
        tmp = 0
        backup_list = []
        for index, value in enumerate(self.values):# backup list that removes the NO_VALUES from the value list, preventing the passing of a list with a string into the random function
            if value != "NO_VALUE":
                backup_list.append(value)

        for unk in valid_actions: # appending the value of the type of block to the respective action
            if unk != "invalid":
                tile_index = self.states.index(adj_tiles[tmp]) # do this
                tile = () #the actual tile, not the action
                if unk == "up":
                    tile = adj_up
                elif unk == "down":
                    tile = adj_down
                elif unk == "left":
                    tile = adj_left
                elif unk == "right":
                    tile = adj_right

                # discourage seeing a new tile
                subtract = self.loc_steps[tile]*0.2

                multiplier = 1
                if self.lookup[tile] == None:# the increase for an unseen tile
                    multiplier = self.unseen_weighting

                if self.values[tile_index] != "NO_VALUE": # if tile in values
                    action_list.append(self.values[tile_index] + multiplier - subtract)
                else:
                    action_list.append(np.mean(backup_list)+multiplier + self.unk_weighting - subtract)
                tmp+=1
            else:
                action_list.append("skip")


        # above was just setup (mostly) below is adaptable to the type of decison used
        action_dict = {}
        for ind, x in enumerate(action_list):# a dictionary backup of action_list to prevent passing a list with strings into the max/random.choice function
            if type(x) != str:
                action_dict[ind+1] = x # ind+1 because the actions start at index 1


        int_ran = np.random.rand()
        if int_ran >= self.elipson:
            action = max(list(action_dict.values())) # using action dict to get the proper value
            # the loop below is used in order to find if there are multiple max values in order to prevent the AI from going into a loop as the max function only picks the first maximum value. (biased towards the earlier values in [up,down,left,right]
            max_list = []
            for x in action_dict.keys(): # no builitn value-key search method
                if action_dict[x] == action: # loop through the keys in the action list and append ones that corelate to maximum values
                    max_list.append(x)
            action = np.random.choice(max_list)

        else:
            action = np.random.choice(list(action_dict.keys())) # slightly more cleaner code using random.choices, saves operation time as a key can be picked directly from a dictionary rather than picking a value, then corelating a key to it.
        return action






    def updateValues(self, reward, state, adj_tiles): # if in a terminal state before reciving the reward.
        block_type = state[0]
        location = state[1]
        self.lookup[location] = block_type # adding entry to the lookup grid
        self.loc_steps[location] += 1
        for tile in adj_tiles: #adding the adj_tiles to states
            if tile not in self.states:
                self.states.append(tile)
        if len(self.states) > len(self.values): # if the value length is not state length or if the value length is state length but the value is not documented
            if block_type not in self.states:
                self.states.append(block_type) #adding the block type to the state
            state_index = self.states.index(block_type)   # match index of values to the index in states
            while len(self.values) < len(self.states):# matching the length of values to the states
                self.values.append("NO_VALUE")
            while len(self.steps) < len(self.states):# matching the length of steps to the states
                self.steps.append(0)
            self.values[state_index] = reward
            self.steps[state_index] += 1
        elif self.values[self.states.index(block_type)] == "NO_VALUE":
            if block_type not in self.states:
                self.states.append(block_type) #adding the block type to the state
            state_index = self.states.index(block_type)   # match index of values to the index in states
            while len(self.values) < len(self.states):# matching the length of values to the states
                self.values.append("NO_VALUE")
            while len(self.steps) < len(self.states):# matching the length of steps to the states
                self.steps.append(0)
            self.values[state_index] = reward
            self.steps[state_index] += 1

        else:
            state_index = self.states.index(block_type)
            self.steps[state_index]+=1
            # below keeps a running average to values
            self.values[state_index] = (self.values[state_index] * (self.steps[state_index]-1) + reward)/self.steps[state_index]
