from time import sleep, time
from operator import iadd, isub
from sys import argv
from random import randint
import termios, fcntl, sys, os
import threading
import queue
from subprocess import call


class CONST:
	K_ESC = "\x1b"
	K_F1 = "\x1bOP"
	K_F2 = "\x1bOQ"
	K_F3 = "\x1bOR"
	K_F4 = "\x1bOS"
	K_F5 = "\x1b[15~"
	K_F6 = "\x1b[17~"
	K_F7 = "\x1b[18~"
	K_F8 = "\x1b[19~"
	K_F9 = "\x1b[20~"
	K_F10 = "\x1b[21~"
	K_F11 = "\x1b[23~"
	K_F12 = "\x1b[24~"
	K_GRAVE_ACCENT = "`"
	K_1 = "1"
	K_2 = "2"
	K_3 = "3"
	K_4 = "4"
	K_5 = "5"
	K_6 = "6"
	K_7 = "7"
	K_8 = "8"
	K_9 = "9"
	K_0 = "0"
	K_TILDE = "~"
	K_EXCLAMATION_MARK = "!"
	K_AT_SIGN = "@"
	K_HASH = "#"
	K_DOLLAR_SIGN = "$"
	K_PERCENTAGE_SIGN = "%"
	K_CIRCUMFLEX = "^"
	K_AMPERSAND = "&"
	K_ASTERISK = "*"
	K_OPARENTHESIS = "("
	K_CPARENTHESIS = ")"
	K_DASH = "-"
	K_UNDERSCORE = "_"
	K_EQ_SIGN = "="
	K_PLUS_SIGN = "+"
	K_BACKSPACE = "\x7f"
	K_TAB = "\t"
	K_Q = "Q"
	K_q = "q"
	K_W = "W"
	K_w = "w"
	K_E = "E"
	K_e = "e"
	K_R = "R"
	K_r = "r"
	K_T = "T"
	K_t = "t"
	K_Y = "Y"
	K_y = "y"
	K_U = "U"
	K_u = "u"
	K_I = "I"
	K_i = "i"
	K_O = "O"
	K_o = "o"
	K_P = "P"
	K_p = "p"
	K_OBRACKET = "["
	K_OBRACE = "{"
	K_CBRACKET = "]"
	K_CBRACE = "}"
	K_BAR = "|"
	K_BACKSLASH = "\\"
	K_A = "A"
	K_a = "a"
	K_S = "S"
	K_s = "s"
	K_D = "D"
	K_d = "d"
	K_F = "F"
	K_f = "f"
	K_G = "G"
	K_g = "g"
	K_H = "H"
	K_h = "h"
	K_J = "J"
	K_j = "j"
	K_K = "K"
	K_k = "k"
	K_L = "L"
	K_l = "l"
	K_SEMICOLON = ";"
	K_COLON = ":"
	K_QUOTE = "'"
	K_DQUOTE = "\""
	K_RETURN = "\n"
	K_Z = "Z"
	K_z = "z"
	K_X = "X"
	K_x = "x"
	K_C = "C"
	K_c = "c"
	K_V = "V"
	K_v = "v"
	K_B = "B"
	K_b = "b"
	K_N = "N"
	K_n = "n"
	K_M = "M"
	K_m = "m"
	K_COMMA = ","
	K_LT_SIGN = "<"
	K_DOT = "."
	K_GT_SIGN = ">"
	K_SLASH = "/"
	K_QUESTION_MARK = "?"
	K_SPACEBAR = " "
	K_INSERT = "\x1b[2~"
	K_HOME = "\x1b[H"
	K_PGUP = "\x1b[5~"
	K_DEL = "\x1b[3~"
	K_END = "\x1b[F"
	K_PGDN = "\x1b[6~"
	K_UARROW = "\x1b[A"
	K_LARROW = "\x1b[D"
	K_DARROW = "\x1b[B"
	K_RARROW = "\x1b[C"




class KeyListener:
	'''
	KeyListener object handles keyboard events
	Requires a KeyQueue object on initialization, into which the chosen values for given keys will be placed
	Usage:
		listener = KeyListener(q)
		listener.addKey(CONST.K_UARROW, "up arrow")
		listener.handleIn()

	Above listener will wait for any input; when it detects a key press, if that key is the up arrow, it will place
	the string "up arrow" into the given queue
	the handleIn method must be run on the main program, not a thread
	On exit, the handler will put 0 in the queue
	'''

	def __init__(self, q):

		if type(q) is not KeyQueue:
			raise TypeError("KeyListener: expected KeyQueue object")

		self.fd = sys.stdin.fileno()

		self.oldterm = termios.tcgetattr(self.fd)
		newattr = termios.tcgetattr(self.fd)
		newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
		termios.tcsetattr(self.fd, termios.TCSANOW, newattr)

		self.oldflags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
		fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

		self.eQueue = q
		self.rec_keycodes = {}

	def __del__(self):
		termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
		fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)
		self.eQueue._put(0)


	def handleIn(self):
		try:
			while True:
				sleep(.01)
				try:
					c = sys.stdin.read(5)

					last_press = self.eQueue._getLastPressTime()

					if c:
						for keycode in self.rec_keycodes:
							if c == keycode:
								self.eQueue._put(self.rec_keycodes[c])
								if self.rec_keycodes[c] == "EXIT":
									exit(0)
								break

					elif last_press and time() - last_press > .05:
						self.eQueue._clear()

				except IOError:
					pass
				except ValueError:
					self.__del__()
					exit(0)


		except KeyboardInterrupt:
			termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
			fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)
			self.eQueue._put("EXIT")

		

	def addKey(self, key, value):
		self.rec_keycodes[key] = value



class Drawer:

	'''
	Drawer object handles drawing to the terminal screen
	The drawer must be run in a seperate thread
	For this reason, all the game code must be placed inside a function
	and then drawer.startThread(function, arguments) must be run, where function
	is the game function and arguments are the arguments for that function, as a tuple
	Usage:
		drawer = Drawer()
		display = drawer.getDisplay()

		#display is now a Display object
		#its rows/columns are equal to the terminal's rows/columns
		#whatever is contained in each cell of the array will be printed at the position it is at
		#therefore code editing the array to change the game frames should be included here

		drawer.drawDisplay(display)

	TODO: Make Drawer automatically update the display object size whenever the terminal window is resized
	'''

	def __init__(self):
		self.last_draw = 0
		self.update_delay = 0
		self.displayObj = Display()

	def drawDisplay(self):

		display = self.displayObj._displayArray
		rows, columns = self.displayObj.getSize()

		while time() - self.last_draw <= self.update_delay:
			sleep(.01)


		call("clear", shell = True)
		for row in range(rows):
			for column in range(columns):
				sys.stdout.write(str(display[row][column]))

			
		sys.stdout.flush()
		self.last_draw = time()

	def getDisplay(self):
		return self.displayObj

	def setFPS(self, value):
		if type(value) is not int:
			raise TypeError("setFPS: FPS value must be integer")
		elif value <= 0:
			raise ValueError("setFPS: FPS value must be positive")

		self.update_delay = 1 / value

	def startThread(self, drawFunc, arguments):

		if not callable(drawFunc):
			raise TypeError("startThread: drawFunc must be function")
		elif type(arguments) is not tuple:
			raise TypeError("startThread: function arguments must be tuple")

		drawThread = threading.Thread(target = drawFunc, args = arguments)
		drawThread.setDaemon(True)
		drawThread.start()


class Display:

	def __init__(self):
		self.clear()

	def _updateSize(self):
		self._rows, self._columns = os.popen('stty size', 'r').read().split()
		self._rows, self._columns = int(self._rows), int(self._columns)

	def getSize(self):
		self._updateSize()
		return (self._rows, self._columns)

	def clear(self):
		self._updateSize()
		self._displayArray = []
		for row in range(self._rows):
			self._displayArray.append([" " for column in range(self._columns)])

	def __getitem__(self, index):
		return self._displayArray[round(index)]



class KeyQueue:

	def __init__(self):
		self.keyPress = queue.Queue()
		self.lpt = None

	def get(self):
		try:
			return self.keyPress.get_nowait()
		except queue.Empty:
			return None

	def _getLastPressTime(self):
		return self.lpt

	def _put(self, val):
		self.keyPress.put(val)
		self.lpt = time()

	def _clear(self):
		with self.keyPress.mutex:
			self.keyPress.queue.clear()
