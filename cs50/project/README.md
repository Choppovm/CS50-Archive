# Agar.io-Styled Game
### Video Demo:
https://www.youtube.com/watch?v=0a97VudCT8k
### Description:
Most things about this game, from the objective, to the controls, to the graphics are relatively simple.
You are a blue square. You use the WASD keys to move up, left, down, and right respectively.
Your objective is to get the green circles, and to avoid the red circles (which chase after you).

Your score is tracked at the bottom.
It increases if you get a green circle (how much it increases depends on the radius of the circle)
It decreases if you get hit by a red circle (how much it decreases depends on the radius of the circle)
Upon reaching zero, you lose, and the game closes itself.

Lines 1-12 consist of a comment on how to play and the imports required for the program to run.
If you don't have any of the imports installed (such as pyglet), you will need to install them (i.e. with pip)

Lines 14-47 consist of constants used throughout the program.
These majorly affect the program, so feel free to copy the code and modify them to see what it does.
Comments have been added to make sure you know what you're editing.

Lines 49-51 initialize the window that's used to project the graphics of the game.
It's therefore advised you don't modify these lines at all.
Lines 53-64 create the score label. The variable names should be self-explanatory.
Feel free to modify these lines to see what they do.

Lines 66-90 create the square you play as, as well as makes sure it can't break the game.
Unless you know what you're doing, don't modify this part.

Lines 92-116 create the circle sprite and checks whether the square has collided with it or not.
Similar to lines 66-90, don't touch this part unless you know what you're doing.

In lines 118-135, line 127 allows you to modify how much the score is increased when touching a green circle.
Feel free to change that, otherwise, again, no touching unless you know what you're doing.

Lines 137-178 are responsible for the particles created when a circle is touched.
To modify these, change the constants at the start of the program.

Lines 183-215 are temporary variables and arrays that stores what's going on in the game.
These shouldn't be modified at all.

Lines 217-242 involve checking whether or not to remove the particles, as well as the controls.
You shouldn't modify this too much, but feel free to change the controls if you know how to do it.

Lines 244-278 check how to update the score, and manages the regenerating of the circles.
If you want to modify this such as changing the delay of generation, edit the constants at the start.

Lines 280-291 draws the particles. Nothing else here.

Lines 293-295 generate the green circles. Increase the "10" to spawn more green circles.
Lines 297-299 determine how many red circles spawn at the start of the match. Increase the "1" to change it.

Lines 301-308 generate the gui that you play on, and let you interact with it. Do not touch these.

That's it for this project.
Thank you, CS50!
