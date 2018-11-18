import requests
from bs4 import BeautifulSoup


#archives chosen 4chan board.

HEADERS = {
    'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


pageNum = 1

#get page
mainPage = requests.get('http://boards.4chan.org/pol/')
soup = BeautifulSoup(mainPage.text, 'lxml')

board = soup.find('div', {'class': 'board'})
thread_ids = []
				
def getPage(urls):
	for i in range(0, len(urls)):
		link = 'http://boards.4chan.org/%s/%s' %(FORUM_NAME, urls[i])
		page = requests.get(link)
		thread = page.content
		print('Archiving page ' + str(pageNum) + ' thread ' + str(i+1)) 
		fWrite = open('page ' + str(pageNum) + ' thread ' + str(i+1) + '.html', 'wb')
		fWrite.write(thread)
		fWrite.close()

FORUM_NAME = 'pol'

for pageNum in range(1, 11):
	mainPageLink = 'http://boards.4chan.org/%s/' %(FORUM_NAME)
	if pageNum > 1:
		mainPageLink += str(pageNum)
	 
	mainPage = requests.get(mainPageLink)
	soup = BeautifulSoup(mainPage.text, 'lxml')
	board = soup.find('div', {'class': 'board'})
	urls = []
	thread_ids = []
	for a in board.find_all('a', {'class': 'replylink'}):
		if 'thread' in a['href']:
			thread_id = a['href'].split('/')[1]
			if thread_id not in thread_ids:
				print (thread_id, a['href'])
				urls.append(a['href'])
				thread_ids.append(thread_id)
				
	getPage(urls)
	pageNum = pageNum + 1