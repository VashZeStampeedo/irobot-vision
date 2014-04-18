import create
import time
robot = create.Create("/dev/ttyUSB0")
robot.go(10,0)
moving = 1
while moving == 1:
	sensors = robot.sensors([create.LEFT_BUMP, create.RIGHT_BUMP])
	if sensors[create.LEFT_BUMP] == 1 or sensors[create.RIGHT_BUMP] == 1:
		print "HIT A WALL"
		robot.stop()
		moving = -1
