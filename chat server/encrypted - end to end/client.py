import os
import requests
import threading
import time

SERVER_URL = 'http://localhost:5000'


letters = ['.', '`', '%', '!', '@', '#', '$', '^', '&', '*', '(', ')', ',', '-', ' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
encryptedLetters = ['k', '!', '1', 'j', 'p', '7', 'a', 't', '%', 'n', ')', 'z', '3', '.', 'x', '&', 'o', 'y', '`', '$', 'u', '#', 'v', 'w', '2', '*', '8', ',', 'r', 'i', '-', '6', 'b', '^', 'm', '0', 's', '(', ' ', 'l', '4', '5', '9', 'c', 'e', 'g', 'f', 'h', 'q', 'd', '@']

cypher = dict(zip(letters, encryptedLetters))
decypher = dict(zip(encryptedLetters, letters))
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
	print('%s: %s' % (message['user'], decryptString(message['content'])))

def main():	
	global last_index
	global username
	username = input('Welcome!\nChoose your username: ')
	update_chat(get_messages())

	t = threading.Thread(target=update_chat_loop, args=tuple())
	t.start()

	while True:
		rawMsg = input('')
		msg = encryptString(rawMsg.lower())
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
	
def encryptString(str):
    resultString = ''
    for letter in str:
        resultString += cypher[letter]
    return resultString
    
def decryptString(str):
    resultString = ''
    for letter in str:
        resultString += decypher[letter]
    return resultString
	
if __name__ == '__main__':
	main()