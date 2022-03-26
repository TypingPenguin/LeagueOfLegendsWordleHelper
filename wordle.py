from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import certifi
import ssl
import time
import pyautogui

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

browser = webdriver.Firefox(executable_path='C:\gecko\geckodriver.exe')

wordleURL = 'https://yordle.pages.dev/'


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
	print("---------------- All Champs with " + str(length) + " characters--------------------")
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
	print("---------------- Possible champs with current letters --------------------")
	print(champs)


	return letters

def findCharacters(url):
	browser.get(url)
#-----------Remove line if not in incognito anymore ---------
	time.sleep(2)
	#	closePopup = browser.find_element_by_class_name('absolute right-4 top-4')
	closePopup = browser.find_element_by_id("headlessui-dialog-overlay-4")
	
	action = webdriver.common.action_chains.ActionChains(browser)
	action.move_to_element_with_offset(closePopup, 5, 5)
	action.click()
	action.perform()
	time.sleep(2)

	boxes = browser.find_elements_by_class_name("letter-container")
	characters = int((len(boxes)) / 6)
	print (characters)

	return characters

##selenium




length = findCharacters(wordleURL)

pyautogui.write('Hell')



#Uncomment for manual input
#length = information()
newChampList = main('https://championmastery.gg/summoner?summoner=a+penguin&region=EUW', length)
filter(newChampList)





#Implement system with correctly placed letters
#Seperate champs space names
#remove ` from names
#Implement system that manages best first try etc..
#Make code cleaner
