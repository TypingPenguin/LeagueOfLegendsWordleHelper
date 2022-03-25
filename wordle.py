from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import certifi
import ssl

extraNames = ['renata','nunu','willump','twisted','fate','master','yi', 'tahm', 'kench', 'jarvan','miss',]

def main(url, length):
	champCorrectLength = []
	sortChampList = []
	champList = []
	champListName = []
	champListDoubleArray = []
	unsplitChampList = getChampions(url)

	if champList == None:
		print("Title could not be found")

	#Get name of Champs from data into champListName
	for name in unsplitChampList:
		champListName.append(name.get_text())
	#print(champListName)

	#Split names if they contain a space, downside: it created a second layer in the array
	for name in champListName:
		#if statement cleaning up webscrape. --TODO: make this cleaner
		if name.find('player') == -1 and name.find('FAQ') == -1 and name.find('scores') == -1 and name.find('info') == -1 and name.find('champions') == -1 and name.find('me') == -1 and name.find('League') == -1 and name.find('u.gg') == -1 and name.find('Git') == -1 and name.find('op.gg') == -1:
			champListDoubleArray.append(name.split())
	#pint(champListDoubleArray)

	#create one array with all the elements by looping twice
	for name in champListDoubleArray:
		for i in name:
			champList.append(i)

	for name in champList:
		sortChampList.append(name)
		if len(name) == length:
			champCorrectLength.append(name)

	#print(sorted(sortChampList))
	print("---------------- Divider Correct Array --------------------")
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
newChampList = main('https://championmastery.gg/summoner?summoner=a+penguin&region=EUW', length)
filter(newChampList)

#Implement system with correctly placed letters
#Seperate champs space names
#remove ` from names
#Implement system that manages best first try etc..
#Make code cleaner
