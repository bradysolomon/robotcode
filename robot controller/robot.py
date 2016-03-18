import threading
import time
import socket
import json
import Adafruit_BBIO.PWM as PWM

SERVER_PORT = 57373
BUFFER_SIZE = 1024

class NonAutonomousRobotWorker():
	def __init__(self):
		self.robot_commands = None

		self.running_thread = None
		self.is_thread_running = False

	def update_commands(self, robot_commands):
		self.robot_commands = robot_commands

	def start(self):
		self._robot_initialization()
		self.is_thread_running = True
		self.running_thread = threading.Thread(target=self.robot_loop, args=())
		self.running_thread.start()

	def stop(self):
		self._robot_termination()
		self.is_thread_running = False

	def get_queued_data(self):
		return "Sensor data"

	####################################################
	#### MAKE SURE TO NOT TOUCH ANYTHING ABOVE THIS ####
	####################################################

	# self.robot_commands is a dictionary of keys and values #
	# {u'down_key': False, u'up_key': False, u'left_key': False, u'speed': 1.0, u'right_key': False} #
	# Speed should be between 0.0-1.0 (0 stopped 1 fast)

	# DUTY CYCLE RANGE = 6.5-7.5-8.5
	def _robot_initialization(self):
		self._leftdrive = "P9_14"
		self._rightdrive = "P9_16"

		PWM.start(self._leftdrive)
		pwm.start(self._rightdrive)

	def _robot_termination(self):
		PWM.close(self._leftdrive)
		PWM.close(self._rightdrive)

	def robot_loop(self):
		while self.is_thread_running:
			PWM.set_frequency(self._leftdrive, 50)
			PWM.set_frequency(self._rightdrive, 50)

			# Speed is a value between 0 and 1
			speed = self.robot_commands["speed"]

			if self.robot_commands["up_key"]:
				if self.robot_commands["left_key"]:
					#move robot left and forward
					PWM.set_duty_cycle(self._rightdrive, 7.5 + speed)
				elif self.robot_commands["right_key"]:
					#move robot right and forward
					PWM.set_duty_cycle(self._leftdrive, 7.5 + speed)
				else:
					#move robot purely forwad
					PWM.set_duty_cycle(self._leftdrive, 7.5 + speed)
					PWM.set_duty_cycle(self._rightdrive, 7.5 + speed)
			elif self.robot_commands["down_key"]:
				if self.robot_commands["left_key"]:
					#move robot left and backwards
					PWM.set_duty_cycle(self._rightdrive, 7.5 - speed)
				elif self.robot_commands["right_key"]:
					#move robot right and backwards
					PWM.set_duty_cycle(self._leftdrive, 7.5 - speed)
				else:
					#move robot purely backwards
					PWM.set_duty_cycle(self._leftdrive, 7.5 - speed)
					PWM.set_duty_cycle(self._rightdrive, 7.5 - speed)
			elif self.robot_commands["right_key"]:
				#spin robot right
				PWM.set_duty_cycle(self._rightdrive, 7.5 - speed)
				PWM.set_duty_cycle(self._leftdrive, 7.5 + speed)
			elif self.robot_commands["left_key"]:
				#spin robot left
				PWM.set_duty_cycle(self._rightdrive, 7.5 + speed)
				PWM.set_duty_cycle(self._leftdrive, 7.5 - speed)
			
def recvtill(socket, marker):
    # Receive until marker is found, return received message with trailing marker removed 
    buflist = []
    while True:
        buf = socket.recv(BUFFER_SIZE, socket.MSG_PEEK)
        if not buf:
            raise IOError("Expected more bytes, invalid protocol.")
        index = buf.find(marker)
        if index == -1:
            socket.recv(len(buf))
            buflist.append(buf)
        else:
            socket.recv(index + len(marker))
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