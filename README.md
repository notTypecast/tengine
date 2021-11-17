# tengine

TEngine is a simply game engine for command line games, written in Python.
Making a game with TEngine is simple. The general template is presented in the steps below:

1. Import the file.
	`import tengine`
2. Make a `KeyQueue` object.
	`q = tengine.KeyQueue()`
3. Make a `KeyListener` object, passing the previously constructed `KeyQueue` object to it.
	`listener = tengine.KeyListener(q)`
4. Using the `addKey` method, set up the keys that the player can use. The first parameter of the method should be one of the key constants, predefined in `tengine.CONST`.The second parameter of the method should be a value, which will be placed inside the `KeyQueue` object whenever the player presses said key. Keep in mind that only a single key can be read at a time.
	`listener.addKey(tengine.CONST.K_UARROW, "up")
	listener.addKey(tengine.CONST.K_DARROW, "down")
	listener.addKey(tengine.CONST.K_ESC, "exit")`
5. Make a `Drawer` object. That object will automatically construct a display, matching the size of the terminal window. Use the `setFPS` method to set the refresh rate of the terminal window when the game is run. Note that a higher framerate speeds up the game, unless measures are taken to prevent this by the game's code.
	`drawer = Drawer()
	drawer.setFPS(30)`

6. Create a function containing the actual game loop. That function should take at least two parameters, the previously created `Drawer` and `KeyQueue` objects. The game loop should run indefinitely (or until some condition is met, like the ESC key is pressed). 
Initially, the game loop should access the `KeyQueue` object and check for any data that might have been placed in it by the listener. After that, the game's logic should follow (including handling any potential key presses).
A `Display` object will act as a 2D array, representing each character on the screen. Each iteration of the game loop, the `clear` method of the `Display` object returned by the `Drawer` object's `getDisplay` method should be called. This will clear the array by filling each cell with an empty space character. After this, each cell of the array can be edited by the game's code to be a different character. Finally, `drawer.drawDisplay()` should be called. It is important to ensure that each string, representing a cell of the display, does not contain any more (or less) than a single character.

7. Start the `Drawer` object's thread using the `startThread` method, passing the game loop function as well as its arguments to it.
	`drawer.startThread(draw, (drawer, q)) #here, draw is the game loop function`

8. Start the key listener.
	`listener.handleIn()`

### Documentation

`class KeyQueue`
method|parameters|returns|description
-|-|-|-
Constructor||`KeyQueue`|Creates a new `KeyQueue` object.
`get`||Value contained in queue, or `None` if queue is empty|Used to get values corresponding to specific key presses in the game loop.

`class KeyListener`
method|parameters|returns|description|raises
-|-|-|-|-
Constructor|`q`|`KeyListener`|Creates a new `KeyListener` object.|`TypeError`: if `q` is not of type `KeyQueue`
`addKey`|`key`: one of the constants from the `CONST` class, `value`: the value to be placed in the queue if `key` is pressed|`None`|Used to bind keys to values, so the game loop function can read and handle them.|
`handleIn`||`None`|Run after the drawer thread has started to begin handling input.|

`class Drawer`
method|parameters|returns|description|raises
-|-|-|-|-
Constructor||`Drawer`|Creates a new `Drawer` object, with a corresponding `Display` object.
`setFPS`|`value`: the FPS value|`None`|Sets the refresh rate to the passed value.|`TypeError`: if `value` is not of type `int`, `ValueError`: if `value` is non-positive
`getDisplay`||`Display`|Returns the `Display` object corresponding to this object.|
`drawDisplay`||`None`|Shows the display array on the screen. Will block according to the given FPS value.|
`startThread`|`drawFunc`: the game loop function, `arguments`: the arguments for `drawFunc`|`None`|Starts a new thread, which executes the code of `drawFunc`.|`TypeError`: if `drawFunc` is not callable or if `arguments` is not a tuple

`class Display`
method|parameters|returns|description
-|-|-|-
Constructor||`Display`|Creates a new `Display` object; is automatically called by the constructor of `Drawer`.
`getSize`||`tuple`|Returns a tuple, representing the rows and columns of the terminal window respectively.
`clear`||`None`|Clears the internal 2D array representing each cell of the screen.
