import threading
import time
import socket
import json
import Adafruit_BBIO.PWM

SERVER_PORT = 57373
BUFFER_SIZE = 1024

#H-Bridge constants 
H11 = "P9_23
H12 = "P9_25"
H21 = "P9_27"
H22 = "P9_41"
H31 = "P9_12"
H32 = "P9_30"

#Servo Constants
Servo_Right = "P9_14"
Servo_Left = "P9_21"
Servo_Claw = "P9_42"
Servo_Claw_OC = #????
Servo_Gim = #???

class NonAutonomousRobotWorker():
	def __init__(self):
		self.robot_commands = None

		self.running_thread = None
		self.is_thread_running = False

	def update_commands(self, robot_commands):
		self.robot_commands = robot_commands

	def start(self):
		self.is_thread_running = True
		self.running_thread = threading.Thread(target=self.robot_loop, args=())
		self.running_thread.start()

	def stop(self):
		self.is_thread_running = False

	def get_queued_data(self):
		return "shit"

	####################################################
	#### MAKE SURE TO NOT TOUCH ANYTHING ABOVE THIS ####
	####################################################

	# self.robot_commands is a dictionary of keys and values #
	# {u'down_key': False, u'up_key': False, u'left_key': False, u'speed': 50.0, u'right_key': False} #

	# Speed should be 0-100
	# Forward should be true/false
	def _left_motor_move(self, drive_pin, forward, speed):

		speed_percent = 0

		if speed > 0:
			speed_percent = speed * 3

		if not forward:
			speed_percent *= -1.0

		Adafruit_BBIO.PWM.set_duty_cycle(drive_pin, 50 + speed_percent)

	# Speed should be 0-100
	# Forward should be true/false
	def _right_motor_move(self, drive_pin, forward, speed):
		speed_percent = 0

		if speed > 0:
			speed_percent = speed / 100.0

		if forward:
			speed_percent *= -1.0

		Adafruit_BBIO.PWM.set_duty_cycle(drive_pin, 7.5 + speed_percent)

	def robot_loop(self):
		#H_bridge
		if SH11 = 1:
			Adafruit_BBIO.GPIO(H11, 1)
			Adafruit_BBIO.GPIO(H12, 0)
		if SH12 = 1:
			Adafruit_BBIO.GPIO(H11, 0)
			Adafruit_BBIO.GPIO(H12, 1)
		else:
			Adafruit_BBIO.GPIO(H11,0)
			Adafruit_BBIO.GPIO(H12,0)
		if SH21 = 1:
			Adafruit_BBIO.GPIO(H21,1)
			Adafruit_BBIO.GPIO(H22,0)
		if SH22 = 1:
			Adafruit_BBIO.GPIO(H21,0)
			Adafruit_BBIO.GPIO(H22,1)
		else:
			Adafruit_BBIO.GPIO(H21,0)
			Adafruit_BBIO.GPIO(H22,0)
		if SH31 = 1:
			Adafruit_BBIO.GPIO(H31,1)
			Adafruit_BBIO.GPIO(H32,0)
		if SH32 = 1:
			Adafruit_BBIO.GPIO(H31,0)
			Adafruit_BBIO.GPIO(H32,1)
		else:
			Adafruit_BBIO.GPIO(H31,0)
			Adafruit_BBIO.GPIO(H32,0)
			
		#servo loop
		if Servo_LL = 1:
			Adafruit_BBIO.PWM.set_duty_cycle(Servo_Left, 9)
		if Servo_LR = 1:
			Adafruit_BBIO.PWM.set_duty_cycle(Servo_Left, 6)
		if Servo_RL = 1:
			Adafruit_BBIO.PWM.set_duty_cycle(Servo_Right, 9)
		if Servo_RR = 1:
			Adafruit_BBIO.PWM.set_duty_cycle(Servo_Right, 6)
		if Servo_CL = 1:
			Adafruit_BBIO.PWM.set_duty_cycle(Servo_Claw, 9)
		if Servo CR = 1:
			Adafruit_BBIO.PWM.set_duty_cycle(Servo_Claw, 6)
		if Servo CC = 1:
			Adafruit_BBIO.PWM.set_duty_cycle(Servo_Claw_OC, 6)
		if Servo CO = 1:
			Adafruit_BBIO.PWM.set_duty_cycle(Servo_Claw_OC, 9)
		#Gimbal 
		if Servo GL = 1:
			Adafruit_BBIO.PWM.set_duty_cycle(Servo_Gim, 9)
		if Servo GR = 1:
			Adafruit_BBIO.PWM.set_duty_cycle(Servo_Gim, 6)
		
		LEFT_DRIVE = "P9_16"
		RIGHT_DRIVE = "P9_22"
    SPEED = 0

		Adafruit_BBIO.PWM.start(LEFT_DRIVE, 50, 333, 0)
		Adafruit_BBIO.PWM.start(RIGHT_DRIVE, 50, 333, 0)

		while self.is_thread_running:
			if self.robot_commands is None:
				continue

      if self.robot_commands["set_speed"]:
        SPEED = self.robot_commands["set_speed"]

			if self.robot_commands["up_key"]:
				if self.robot_commands["left_key"]:
					#move robot left and forward
					self._left_motor_move(LEFT_DRIVE, True, SPEED)
					self._right_motor_move(RIGHT_DRIVE, True, 0)
				elif self.robot_commands["right_key"]:
					#move robot right and forward
					self._right_motor_move(RIGHT_DRIVE, True, SPEED)
					self._left_motor_move(LEFT_DRIVE, True, 0)
				else:
					#move robot purely forwad
					self._right_motor_move(RIGHT_DRIVE, True, SPEED)
					self._left_motor_move(LEFT_DRIVE, True, SPEED)
			elif self.robot_commands["down_key"]:
				if self.robot_commands["left_key"]:
					#move robot left and backwards
					self._right_motor_move(RIGHT_DRIVE, False, 0)
					self._left_motor_move(LEFT_DRIVE, False, SPEED)
				elif self.robot_commands["right_key"]:
					#move robot right and backwards
					self._right_motor_move(RIGHT_DRIVE, False, SPEED)
					self._left_motor_move(LEFT_DRIVE, False, 0)
				else:
					#move robot purely backwards
					self._left_motor_move(LEFT_DRIVE, False, SPEED)
					self._right_motor_move(RIGHT_DRIVE, False, SPEED)
			elif self.robot_commands["right_key"]:
				#move robot right
				self._right_motor_move(RIGHT_DRIVE, False, SPEED)
				self._left_motor_move(LEFT_DRIVE, True, SPEED)
			elif self.robot_commands["left_key"]:
				#move robot left
				self._right_motor_move(RIGHT_DRIVE, True, SPEED)
				self._left_motor_move(LEFT_DRIVE, False, SPEED)
			else:
				self._right_motor_move(RIGHT_DRIVE, True, 0)
				self._left_motor_move(LEFT_DRIVE, False, 0)

def recvtill(sock, marker):
    # Receive until marker is found, return received message with trailing marker removed 
    buflist = []
    while True:
        buf = sock.recv(BUFFER_SIZE, socket.MSG_PEEK)
        if not buf:
            raise IOError("Expected more bytes, invalid protocol.")
        index = buf.find(marker)
        if index == -1:
            sock.recv(len(buf))
            buflist.append(buf)
        else:
            sock.recv(index + len(marker))
            buflist.append(buf[:index])
            return ''.join(buflist)

if __name__ == "__main__":
	robot = NonAutonomousRobotWorker()
	robot.start()

	# THE CLIENT-SERVER/SERVER-CLIENT PROTOCL SHOULD BE AS SEEN BELOW #
	# IT IS OKAY TO MAKE THE ASSUMPTION THAT ALL COMMUNICATIONS FOLLOW THAT PROTOCOL AS WE ARE ONLY ACCEPTING CONNECTIONS FROM LOCALHOST #

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(("0.0.0.0", SERVER_PORT))
	sock.listen(1)

	while True:
		conn, address = sock.accept()

		data = recvtill(conn, "\n\n")
		
		if data == "REQUEST_DATA":
			response = robot.get_queued_data()
			conn.sendall(response)
		elif data == "SEND_DATA":
			data = recvtill(conn, "\n\n")

			json_parsed_data = None

			try:
				json_parsed_data = json.loads(data)
			except Exception as e:
				print e

			robot.update_commands(json_parsed_data)
		elif data == "PING":
			conn.sendall("PONG")

		conn.close()
