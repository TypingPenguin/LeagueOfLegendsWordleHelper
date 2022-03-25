from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import certifi
import ssl


def main(length):
	champCorrectLength = []
	champList = getChampions('https://championmastery.gg/summoner?summoner=a+penguin&region=EUW')
	if champList == None:
		print("Title could not be found")
	else:
		i = 0
		for name in champList:
			if len(name.get_text()) == 6:
				champCorrectLength.append(name.get_text())

	for name in champCorrectLength:
		print(name)
	return champCorrectLength

def getTitle(url):
	try:
		html = urlopen(url)
	except HTTPError as e:
		print(e)
		return None
		#return null, break, or do some other "Plan B"
	except URLError as e:
		print('The server can not be found!')
		return None
	try:
		bs = BeautifulSoup(html.read(), 'lxml')
		title = bs.body.h1
	except AttributeError as e:
		return None
	return title

def getChampions(url):
	try:
		html = urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
	except HTTPError as e:
		print(e)
		return None
		#return null, break, or do some other "Plan B"
	except URLError as e:
		print('The server can not be found!')
		return None
	try:
		bs = BeautifulSoup(html.read(), 'lxml')
		text = bs.find_all('a')
	except AttributeError as e:
		return None
	return text

def information():
	x = int(input("amount of characters:"))
	return x

def filter(champs): #filter on the random placed letters
	letters = input("letters that are correct:").split()
	#print (letters)
	for letter in letters:
			champs = [name for name in champs if name.find(letter) >= 0] #returns position of letters from 0...n
	print(champs)


	return letters



length = information()
newChampList = main(length)
filter(newChampList)

#Implement system with correctly placed letters
#Implement system that manages best first try etc..
#Make code cleaner