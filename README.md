# Cavescapes
A game that uses a Monte-Calro based learning algorithm to traverse a procedurally generated world.

## Running the Game
Run MAIN.py using python 3 or above. Requires Numpy and PyGame installed.

## Overview
As said in the heading, the Agent uses a monte-carlo based learning model. 
The world (maze) is created through the use of a modified reverse backtracking algorithm. 
Playable by a human or the AI. 
- Use arrow keys to move and 
- Turn on/off the AI by clicking the button on the top
- Speed up the learning process by clicking "fast learn". This increases the framerate and removes delay between frame updates
- The "change view" button allows you to toggle between seeing the whole board and just what the AI sees (It is able to see adjacent tiles only)
- The complexity/size of the grid can be changed by editing the ```grid_size``` variable in ```game_config.py```
- For more advanced users, properties of the AI can be adjusted in ```game_config.py```

## Notable Behaviours and Quirks
- The AI seems to refuse to step on portal tiles, likely due to a high level of positive reinforcement towards regular path tiles that discourage the exploration of portals or new branches.
- The AI oftern retraces its paths to earn "slow and steady" rewards since a small positive reward is generally allocated to path tiles by the end of training.

## Future Changes
Likely no major future changes.

-sonic597
