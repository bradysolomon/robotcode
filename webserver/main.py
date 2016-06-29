import flask
import random
import json
import socket

app = flask.Flask(__name__)
robot_sock = None

ROBOT_SERVER_PORT = 57373
ROBOT_BUFFER_SIZE = 1024

@app.route("/")
def control_panel():
	return flask.render_template("test.html", rand_numb=random.randint(0, 100))

@app.route("/control_robot", methods=["POST"])
def control_robot():
  mutable_form = flask.request.form.copy()

  if "keys_pressed" in mutable_form and "speed" in mutable_form:
    speed = float(mutable_form.pop("speed"))
    keys_pressed = json.loads(mutable_form.pop("keys_pressed"))

    true_keys_ctr = 0
    for value in keys_pressed.values():
      if value: true_keys_ctr += 1

    if true_keys_ctr > 2 or (keys_pressed["left_key"] and keys_pressed["right_key"]) or (keys_pressed["up_key"] and keys_pressed["down_key"]):
      return "Failed to move robot."

    send_data_to_robot(json.dumps(control_data))
    return "Successfully moved robot."

  return "Failed to move robot."	

def send_data_to_robot(data):
	robot_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	robot_sock.connect(("0.0.0.0", ROBOT_SERVER_PORT))

	try:
		robot_sock.sendall("SEND_DATA\n\n")
		robot_sock.sendall(data + "\n\n")
		robot_sock.close()
	except Exception as e:
		print e	

'''
# speed can be any value between 0 and 100
# keys_pressed should be a dictionary with 4 keys (up_key, left_key, right_key, down_key) and values (true, false)
	# only a maximum of two values in the dictionary should be true at once 
	# both right_key and left_key cannot be true at once; both up_key and down_key cannot be true at once
def move_robot(keys_pressed, speed):
	if keys_pressed["up_key"]:
		if keys_pressed["left_key"]:
			#move robot left and forward
			return "Moving robot forward left."
		elif keys_pressed["right_key"]:
			#move robot right and forward
			return "Moving robot forward right."
		else:
			#move robot purely forwad
			return "Moving robot forward."
	elif keys_pressed["down_key"]:
		if keys_pressed["left_key"]:
			#move robot left and backwards
			return "Moving robot backwards left."
		elif keys_pressed["right_key"]:
			#move robot right and backwards
			return "Moving robot backwards right."
		else:
			#move robot purely forwad
			return "Moving robot backwards."
	elif keys_pressed["right_key"]:
		#move robot right
		return "Turning robot right."
	elif keys_pressed["left_key"]:
		#move robot left
		return "Turning robot left."

	return "Error moving robot."
'''

if __name__ == "__main__":
	app.run(debug=True, threaded=True, host="0.0.0.0")
