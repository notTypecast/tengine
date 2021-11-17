import os, sys
import queue
from random import randint
from time import sleep
#go to parent directory
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import tengine


fps = 1

eventQueue = tengine.KeyQueue()
handler = tengine.KeyListener(eventQueue)
#TODO: there are issues with pausing
handler.addKey(tengine.CONST.K_p, "pause")
handler.addKey(tengine.CONST.K_UARROW, "speedup")
handler.addKey(tengine.CONST.K_DARROW, "slowdown")
drawer = tengine.Drawer()
drawer.setFPS(fps)

def drawFunc(drawer, q, fps):

	paused = False

	while True:
		res = q.get()
		if res == "pause":
			paused = False if paused else True
		elif res == "speedup":
			fps += 1
			drawer.setFPS(fps)
		elif res == "slowdown":
			if fps > 1:
				fps -= 1
				drawer.setFPS(fps)

		if not paused:
			display = drawer.getDisplay()
			displaySize = display.getSize()

			for row in range(displaySize[0]):
				for column in range(displaySize[1]):
					display[row][column] = randint(0, 1)

			drawer.drawDisplay()
		else:
			sleep(.01)


drawer.startThread(drawFunc, (drawer, eventQueue, fps))

handler.handleIn()