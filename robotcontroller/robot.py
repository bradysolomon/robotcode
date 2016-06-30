import threading
import time
import socket
import json
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO

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

	# Speed should be 0-100
	# Forward should be true/false
  def _drive_motor_move(self, drive_pin, forward, speed):

    speed_percent = 0

    if speed > 0:
      speed_percent = speed * 3

    if not forward:
      speed_percent *= -1.0

    PWM.set_duty_cycle(drive_pin, 50 + speed_percent)

  def _wrist(self, up, off = False)
    if off:
      GPIO.output(WRIST1, 0)
      GPIO.output(WRIST2, 0)
    elif up:
      GPIO.output(WRIST1, 0)
      GPIO.output(WRIST2, 1)
    else
      GPIO.output(WRIST1, 1)
      GPIO.output(WRIST2, 0)

  def robot_loop(self):
    LEFT_DRIVE = "P9_16"
    RIGHT_DRIVE = "P9_22"
    WRIST1 = "P9_23"
    WRIST2 = "P9_25"
    SPEED = 0

    PWM.start(LEFT_DRIVE, 50, 333, 0)
    PWM.start(RIGHT_DRIVE, 50, 333, 0)
    GPIO.setup(WRIST1, GPIO.OUT)
    GPIO.setup(WRIST2, GPIO.OUT)

    while self.is_thread_running:
      if self.robot_commands is None:
        continue

      if self.robot_commands["set_speed"] > 0:
        SPEED = self.robot_commands["set_speed"]

      if self.robot_commands["k_key"]:
        self._wrist(True) 
      elif self.robot_commands["j_key"]:
        self._wrist(False)
      else
        self._wrist(True, True)

      if self.robot_commands["up_key"]:
        if self.robot_commands["left_key"]:
          #move robot left and forward
          self._drive_motor_move(LEFT_DRIVE, True, SPEED)
          self._drive_motor_move(RIGHT_DRIVE, True, 0)
        elif self.robot_commands["right_key"]:
          #move robot right and forward
          self._drive_motor_move(RIGHT_DRIVE, True, SPEED)
          self._drive_motor_move(LEFT_DRIVE, True, 0)
        else:
          #move robot purely forwad
          self._drive_motor_move(RIGHT_DRIVE, True, SPEED)
          self._drive_motor_move(LEFT_DRIVE, True, SPEED)
      elif self.robot_commands["down_key"]:
        if self.robot_commands["left_key"]:
          #move robot left and backwards
          self._drive_motor_move(RIGHT_DRIVE, False, 0)
          self._drive_motor_move(LEFT_DRIVE, False, SPEED)
        elif self.robot_commands["right_key"]:
          #move robot right and backwards
          self._drive_motor_move(RIGHT_DRIVE, False, SPEED)
          self._drive_motor_move(LEFT_DRIVE, False, 0)
        else:
          #move robot purely backwards
          self._drive_motor_move(LEFT_DRIVE, False, SPEED)
          self._drive_motor_move(RIGHT_DRIVE, False, SPEED)
      elif self.robot_commands["right_key"]:
        #move robot right
        self._drive_motor_move(RIGHT_DRIVE, False, SPEED)
        self._drive_motor_move(LEFT_DRIVE, True, SPEED)
      elif self.robot_commands["left_key"]:
        #move robot left
        self._drive_motor_move(RIGHT_DRIVE, True, SPEED)
        self._drive_motor_move(LEFT_DRIVE, False, SPEED)
      else:
        self._drive_motor_move(RIGHT_DRIVE, True, 0)
        self._drive_motor_move(LEFT_DRIVE, False, 0)

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
