import threading
import time
import socket
import json

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

	def robot_loop(self):
		while self.is_thread_running:
			print self.robot_commands
			time.sleep(2.5)

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