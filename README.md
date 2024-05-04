# PEG SOLITAIRE
#### Author: Toke Henrik Olesen
#### Video Demo: https://youtu.be/IX6GxPzVLLQ
### General description:

Peg Solitaire is a simple puzzle game based on the popular single-player board game of the same name. Written in Python
using the Pygame framework, it mimics the graphical style and look of DOS games of the early 90s and is rendered at an
era-appropriate internal resolution of 320x240 pixels, which is scaled up before displaying.

The game lets the player test themselves against five different board configurations (including the popular English
and French layouts), supports undo functionality and is localized in two languages: English and Polish.

### Main menu overview:

When the game starts, the player is greeted by the main menu.

- "Play": Takes the player to a new menu where they can choose the board layout that they wish to play. Choosing a
layout starts the actual game.
- "Settings": Takes the player to a screen where they can choose whether they want sounds to be played, valid moves
to be highlighted on the board and the games' language. The choices are saved to a file.
- "Quit": Stops the game.

### Gameplay overview:

Upon choosing a layout, the player will be taken to the main game screen. A game board will be displayed, showing a
number of pegs and one free tile. A peg can be moved to a free tile two tiles away, horizontally or vertically, provided
that the tile between the peg and the chosen destination is occupied by another peg. After moving, the peg that has been
jumped over is removed from the board. The goal of the game is to remove all pegs but one.

Pegs are moved by dragging and dropping them with the mouse. By default, the tiles that the lifted peg can legally be
moved to will be highlighted; that can be disabled in settings.

At any time, the player can go back any number of steps by clicking the "Undo" button. The "Restart" button resets the
board and all the pegs; "Exit" takes the player back to the main menu.

### Design overview:

The game's design follows the OOP principles, and as such, the game's elements are self-contained, independent and
reusable.

When the code first runs, an object of the Game class is instantiated. At initialization, it instantiates objects of the
game's other classes as its properties, most notably an object of the Board class (board_class.py) which contains the
actual gameplay logic, as well as UI elements such as buttons, labels and switches. Game states are defined and methods
of the Game class are assigned to them. When the game loop runs, the appropriate method is called on each cycle
depending on the game's current state.

The actual gameplay logic is handled by an object of the Board class, which is drawn on its own Pygame surface. This
allows the Board class to be easily reused in any other project. Indeed, it would be possible to have several boards on
the screen at the same time, or embed them inside a window. This makes it possible to include Peg Solitaire as a
minigame in a bigger project, without the need to alter the Board class' code.

Since the game is rendered at a resolution of 320x240, it needs to be scaled up before displaying on a modern screen.
This is achieved by blitting all game's graphics - the background, the board, the UI elements - to a "display" Pygame
surface, which is scaled up before blitting on a "screen" surface, which is what actually gets displayed on the user's
screen. The scaling factor defaults to 3, but can be set to any value in the 1-10 range with the command line argument
-s or --scale (for example, "python main.py --scale 5").

Rendering the game at a scaled resolution made it necessary to correct mouse input values. Since Pygame's
mouse.get_pos() function returns the cursor coordinates relative to "screen" (scaled) and not "display" (unscaled), it
is necessary to divide the coordinates by the scaling factor to get values that can be used in the context of "display".

Since the game is 100% mouse-driven, standard GUI elements such as buttons and switches were necessary. These have been
implemented from scratch and care has been taken to make them independent and reusable; as such, they can be readily
used in other projects. While the most attention has been given to the Button class (button_class.py), toggle switches,
radio buttons and dialog windows have also been implemented to a degree sufficient for the game's needs; a full Pygame
GUI suite is a possible future project.

### Module overview:

In addition to using the Pygame framework as well as some modules from Python's standard library, such as Pickle and
Enum, the game's code spans multiple files. Where possible, care has been taken to implement them as modules with
reusability in mind.

#### Main.py

Describes the Game class, which defines all the game states, their associated methods and implements the game loop.
During initialization, loads user settings from a file, instantiates an object of the Board class (which contains the
actual game), assigns methods to buttons, loads graphics and sound and initalizes all GUI elements.

The .game_loop() method runs until the game is terminated; each cycle, it calls the method assigned to the current game
state and redraws the screen.

#### Board_class.py

Describes the game board, where the actual gameplay takes place, and all the game logic. It defines its own surface that
it is drawn on, which is later blitted on the target surface that will be displayed on the screen.

The board is composed of a set of tiles (defined in board_tiles_class.py), arranged in a square of, by default, 9 by 9
tiles. A tile can be smooth or contain a hole with room for a peg; when the game starts, all tiles with holes, but one,
will be occupied by pegs. The board layout is described in layout.py, as a tuple of tuples (essentially a 2d array), and
passed to the Board class' constructor as an argument at initialization.

The various methods define the game's rules, check the player moves' validity, implement the undo functionality, check
the board's current state against the victory/defeat conditions etc. Some of the most important are:

- ._move_is_legal(): returns True if the player's current move is valid according to the game rules. Uses the Peg
object's properties .grid_coords (the peg's current position) and .old_grid_coords to determine whether the move can be
performed using helper functions ._tile_is_occupied(), ._destination_is_valid() and ._is_jumping_over().
- .undo(): Goes back one step. The .undo_stack property contains a list of all moves; .undo() gets the data of the last
moves, deletes it, and puts the pegs back on the board.
- ._check_for_victory_and_defeat(): compared the board's current state against the victory and defeat conditions, and
sets ._game_is_won and ._game_is_lost to True or False accordingly. If the user undoes their last move on a won or lost
game, those flags are cleared.
- .process_input(): The actual game logic. Checks for mouse input and lets the user drag and drop pegs; highlights valid
destinations for the dragged peg; updates peg positions upon a valid move; deletes "jumped over" pegs; keeps track of
the move count.

#### Board_tiles_class.py

Describes the Tile object used by the Board. The base Tile class describes a generic tile and is used to instantiate
plain tiles, tiles with holes, and highlights (a special case of a tile, overlaid on other tiles to highlight valid
moves when a peg is lifted).

The Peg class is a child class of Tile and implements additional functionality. Since it's the only kind of Tile that
can be moved, it has properties describing it's current position (.grid_pos), the position where it was before it was
lifted by the player (.old_grid_pos), as well as ._mouse_offset (describes the relative position of the peg to the mouse
cursor at the beginning of a drag&drop operation - each frame, until dropped, the peg will be drawn at a position
relative to the cursor's position, effectively following it).

The Peg class implements some animations to make the game more visually pleasing, such as a "fading out" animation when
the peg has been set to be deleted, and "snapping back" animation if the peg was released without finding a new valid
position. "Fading out" is achieved by lowering the peg's alpha value each frame until it reaches 0; "snapping back"
describes the pegs current and target positions as 2d vectors, and then updates its position every frame by a velocity
vector, which is a normalized direction vector multiplied by the speed, defined at initialization.

#### Graphics.py

Describes the Graphics class which, upon initialization, loads graphical files and generates other graphical assets.
It also describes the game's graphical constants, such as, among other, the resolution and target framerate.

All graphical assets used by the game are properties of an object of the Graphics class, which in the Game class is
instantiated as .gfx, as a property of that class. That object is passed to other objects' constructors as an argument,
as necessary.

#### Sounds.py

Same as graphics.py, but for audio assets.

#### Button_class.py

Describes the Button, which is the most commonly used GUI element in the game. It is customizable and relatively fully
featured, and can be readily reused in other Pygame projects.

All arguments passed to the class' constructor must be keyword arguments.

A function name must be passed to the button as an argument at initialization; when the button is clicked, that function
will be called. The button requires a Surface object to use for it's graphics. Two surface objects can be provided, one
for the unclicked and one for the clicked state. If no "clicked" graphic is provided, the "unclicked" version will be
used, rotated 180 degrees, to simulate a 3D-esque convex/concave effect.

Text can be displayed on the button using the chosen font, and while it will by default be displayed in the middle, it
can be shifted by passing the text_x_offset and text_y_offset arguments.

The button can be made inactive when a value, optionally defined as active_condition, is False. An inactive button is
"greyed out" and cannot be clicked. If an active_condition has been defined, the button's active state will follow
the active_condition's value.

#### Dialog_window_class.py

Describes a dialog window. Requires a surface to be passed for graphics, and the text to be displayed. The buttons,
yes/no or otherwise, must be defined separately. Making the dialog class more fleshed-out is a possible future
consideration.

The dialog window will be displayed at the defined position on the screen, awaiting the user's input. In the game, it is
used to get the player's confirmation when they want to restart or quit the game.

#### Toggle_class.py

Describes a simple switch that can be either on and off and can be flipped with a mouse click. Like the Button class,
requires a Pygame surface to be passed for graphics. Has an .is_on property that describes it's current status.

Optionally, the switch can call a function when flipped, if the name of one was provided.

That can be used to simulate a "radio button" functionality using a set of switches. To that end, if the ._is_radio
property has been defined and if it is set to True, the switch can only be flipped when it is off. If a function is
passed to set the other radio buttons to False when it is clicked, the switches will behave like radio buttons.

This is a temporary hack; implementing a fully fleshed out radio button functionality is a possible future
consideration.

#### Ui_elements.py

This module contains a few helper classes designed to help generate buttons, dialog windows and switches. All those GUI
elements require a large amount of arguments at initialization; these helper classes keep track of the data for each
GUI element and help generate dictionaries that can be passed to the constructor of GUI objects as keyword arguments.
This approach helps keep all the GUI related data in one place and, because defaults are defined separately, removes the
need for keyword argument default values in the GUI classes themselves, making them independent from the rest of the
code and, as a result, more portable.

- InitializeButtons class: instantiates all buttons objects in the game and stores them in lists, depending on which
game state they belong to. Contains the data for all the buttons, and default data to fall back on if no specific data
was provided.
- InitializeDialogWindows: instantiates Dialog Window objects as properties of an object of this class.
- InitializeToggles: instantiates Toggle objects as properties of an object of this class.

#### Options.py

Describes an object that stores the game's settings. It is instantiated (or loaded from a file) when the game starts and
gets passed to other objects as necessary.

#### Layouts.py

Contains the data for the board layouts as one variable, "layouts", which is a tuple of dictionaries. Each dictionary
has a "layout" key and a "start" key; "layout" is a tuple of tuples (essentially a 2d array) where 0 means a smooth
tile and 1 means a tile with hole. "start" contains the coordinates of the start hole, that is, the only hole tile that
does not contain a peg at the start of the game.

#### Languages.py

Contains all of the labels, text messages etc. that appear in the game in both supported languages: English and Polish.
Each entry is a dictionary with "en" and "pl" as keys. This design would make it trivial to add more languages, if that
was ever desired.

#### Create_surface.py

A helper function that draws a pygame surface object that looks like a flat 3d GUI element. Can be used for buttons,
dialog windows, switches etc. It is used throughout the game. Not really considered part of the game code itself, but
in the absence of better graphics assets, makes it possible to quickly create something that is useful and looks
passable.