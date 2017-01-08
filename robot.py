import RPi.GPIO as GPIO
import sys
import time
import sys,tty,termios
from _thread import start_new_thread

import numpy as np


GPIO.setmode (GPIO.BOARD)
GPIO.setwarnings (False)

pin1=15
pin2=16
pin3=18
pin4=22

global moving
moving = False

global ultrasonicValues
ultrasonicValues = []

TRIG = 12
ECHO = 11

timesleep = 0.1

# Motor Control Setup
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)
GPIO.output(pin1, True)
GPIO.output(pin2, True)
GPIO.output(pin3, True)
GPIO.output(pin4, True)

# Ultrasonic Setup
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)

def get_distance():

	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)
	pulse_start = time.time()
	pulse_end = time.time()

	while GPIO.input(ECHO)==0:
		pulse_start = time.time()

	while GPIO.input(ECHO)==1:
		pulse_end = time.time()     

	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150
	distance = round(distance, 0)
	#print (distance)
	return distance


def drive(input):
	print ("Setting GPIO")
	print (input)
    	
	if input[0] == "1":
		GPIO.output(pin1, False)
	else:
		GPIO.output(pin1, True)
    	
	time.sleep (timesleep) 
	if input[1] == "1":
		GPIO.output(pin2, False)
	else:
		GPIO.output(pin2, True)
   
	time.sleep (timesleep) 
	if input[2] == "1":
		GPIO.output(pin3, False)
	else:
		GPIO.output(pin3, True)

	time.sleep (timesleep) 
	if input[3] == "1":
		GPIO.output(pin4, False)
	else:
		GPIO.output(pin4, True)
	return

def prevent_crash():
	global moving
	ultrasonicValues
	while True:
		distance = get_distance()
		if len(ultrasonicValues) > 10:
			ultrasonicValues.pop(0)
		ultrasonicValues.append(int(distance))
		#print ("Distance: " + str(ultrasonicValues))
		my_arr = np.array(ultrasonicValues)
		time.sleep (0.1)
		if distance < 30 and moving and my_arr.std() < 20:
			drive ('1010')
			time.sleep(1)
			drive ('0100')
			# time.sleep(random())
			time.sleep(1)
			drive ('0101')
			# moving = False
			# print ("Std: " + str(round(my_arr.std(),0)))
	return


print ("Robot initializing...")
print ("Waiting For Ultrasonic sensor to settle")
time.sleep(2)
print ("Ready!")

start_new_thread (prevent_crash, ())

class _Getch:       
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
	global moving
	inkey = _Getch()
	while(1):
		k=inkey()
		print (k)
		if k!='':break
	
	if k==(chr(27)+chr(91)+chr(65)):
		if moving:
			print ("Stop")
			drive('0000')
			moving = False
		else:
			print ("Forward")
			drive('0101')
			moving = True
	elif k==(chr(27)+chr(91)+chr(66)):
		if moving:
			print ("Stop")
			drive('0000')
			moving = False
		else:
			print ("Backward")
			drive('1010')
			moving = True
	elif k=='\x1b[C':
		print ("Right")
		drive('0100')
		moving = True
	elif k=='\x1b[D':
		print ("Left")
		drive('0001')
		moving = True
	else:
                print ("not an arrow key!", ord(k))


def main():
    while True:
        get()

if __name__=='__main__':
    main()


