# python-snake-game
Python Snake game based on the tutorial by baraltech found here:
https://www.youtube.com/watch?v=ebVV-6QMUIU

With several changes including:

## CORE CHANGES
- Removed dependency of font file.
- Avoid the need for resetting the screen and redrawing the grid each frame, Modify the Snake.update method to correctly move the snake by adding a new head and removing the last segment.
- 

## BUGFIXES
- The snake's direction cannot reverse directly to avoid self-collision by instantaneous 180-degree turns.
- Added a place_apple method that ensures the apple spawns outside the snake's body. The method uses a while loop to keep generating a new position until it finds one that does not collide with any part of the snake.

## UPGRADES
- Wait for the user input before moving
- New dedicated are for the score, doesn't interfere with gameplay.
- Added HI-Score feature
- Added Game Over screen, with option to retry ot close the game.
