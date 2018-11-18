import os
import requests
import threading
import time

SERVER_URL = 'http://localhost:5000'

arr = []
last_index = 0
username = None

def get_messages():
	return requests.get(SERVER_URL + '/messages').json()


def print_messages(messages):
	for message in messages:
		print_message(message)
		
def print_message(message):
	global username
	if message['user'] == username:
		return
	print('%s: %s' % (message['user'], message['content']))

def main():	
	global last_index
	global username
	username = input('Welcome!\nChoose your username: ')
	update_chat(get_messages())

	t = threading.Thread(target=update_chat_loop, args=tuple())
	t.start()

	while True:
		msg = input('')
		requests.post(SERVER_URL + '/message', json={
			'user': username,
			'content': msg})
	
def update_chat_loop():
	while True:
		update_chat(get_messages())
		time.sleep(5)
	

def update_chat(messages):
	global last_index
	if len(messages) == 0:
		return 

	for message in messages[last_index:]:
		print_message(message)
		
	last_index = len(messages)
	
if __name__ == '__main__':
	main()