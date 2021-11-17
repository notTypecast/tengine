import os, sys
import time
from random import randint
#go to parent directory
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import tengine as TE


def draw(drawer, eventQueue):
	#get display and place spaceship at bottom, middle
	display = drawer.getDisplay()
	rows, columns = display.getSize()
	spaceship_x = columns // 2
	spaceship_y = rows - 3
	bullets = []
	rocks = []
	total_rocks = 1

	while True:

		while len(rocks) < total_rocks:
			rocks.append([randint(1, columns - 1), 1])

		spaceship_speed = 0

		action = eventQueue.get()

		if action:
			if action == "left":
				spaceship_speed = -1
			elif action == "right":
				spaceship_speed = 1
			elif action == "shoot":
				bullets.append([spaceship_x, spaceship_y])
			elif action == "EXIT":
				break


		#clear screen
		display.clear()

		if spaceship_speed > 0 and spaceship_x < columns - 3:
			spaceship_x += spaceship_speed
		elif spaceship_speed < 0 and spaceship_x > 1:
			spaceship_x += spaceship_speed

		#draw spaceship
		display[spaceship_y][spaceship_x] = chr(9632)
		display[spaceship_y + 1][spaceship_x] = chr(9632)
		display[spaceship_y + 1][spaceship_x - 1] = chr(9632)
		display[spaceship_y + 1][spaceship_x + 1] = chr(9632)

		updated_bullets = []
		for bullet in bullets:
			bullet[1] -= 1
			if bullet[1] >= 0:
				updated_bullets.append(bullet)

		bullets = updated_bullets

		updated_rocks = []
		for rock in rocks:
			rock[1] += .6
			if round(rock[1]) < rows:
				updated_rocks.append(rock)

			'''			
			if rock[0] < spaceship_x:
				rock[0] += 1
			elif rock[0] > spaceship_x:
				rock[0] -= 1
			'''
		if len(rocks) != len(updated_rocks):
			total_rocks += 1
		rocks = updated_rocks

		for bullet in bullets:
			display[bullet[1]][bullet[0]] = chr(8607)

			for rock in rocks:
				if round(rock[0]) in range(bullet[0] - 1, bullet[0] + 2) and bullet[1] == round(rock[1]):
					rocks.remove(rock)
					bullets.remove(bullet)
					break
		
		for rock in rocks:
			display[rock[1]][rock[0]] = chr(11054)

			if round(rock[0]) in range(spaceship_x - 1, spaceship_x + 2) and round(rock[1]) in range(spaceship_y, spaceship_y + 2):
				print("You lose!")
				exit(0)		

		#draw the edited display
		drawer.drawDisplay()



if __name__ == "__main__":
	#create queue for listener and handler to communicate
	eventQueue = TE.KeyQueue()

	#create listener and add necessary keys
	listener = TE.KeyListener(eventQueue)
	listener.addKey(TE.CONST.K_SPACEBAR, "shoot")
	listener.addKey(TE.CONST.K_LARROW, "left")
	listener.addKey(TE.CONST.K_RARROW, "right")
	listener.addKey(TE.CONST.K_ESC, "EXIT")

	#create drawer
	drawer = TE.Drawer()
	drawer.setFPS(30)

	#start drawer and listener
	drawer.startThread(draw, (drawer, eventQueue))
	listener.handleIn()



