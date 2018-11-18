#login, update msgs

import threading
import time
import sys
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)


messages = []
messages.append({'user': 'Moshe', 'content': 'ff'})


@app.route('/')
def homepage():
	return '''
	<html>
		<head> </head>
		<body style="background-color: blue">
			%s
		</body>
	</html>
	''' % (
		'<h1 style="text-align: center; font-size:200px; color:green; background-color: red">DOR HAMOR</h1>' * 10000)

	
@app.route('/messages', methods=['GET'])
def get_messages():
	return jsonify(messages)
	
@app.route('/static/<path:filename>', methods=['GET'])
def get_static():
	return send_from_directory('static', filename)


@app.route('/message', methods=['POST'])
def post_message():
	msg = request.json

	messages.append(msg)
	
	return 200

	
if __name__ == '__main__':
	if len(sys.argv) > 1:
		port = sys.argv[1]
	else:
		port = 5000

	app.run(host= '0.0.0.0', port=port)