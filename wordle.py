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
from selenium.webdriver.common.by import By

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


	return champs

def findCharacters(url):
	browser.get(url)
#-----------Remove line if not in incognito anymore ---------
	time.sleep(1)
	#	closePopup = browser.find_element_by_class_name('absolute right-4 top-4')
	closePopup = browser.find_element_by_id("headlessui-dialog-overlay-4")
	
	action = webdriver.common.action_chains.ActionChains(browser)
	action.move_to_element_with_offset(closePopup, 5, 5)
	action.click()
	action.perform()
	time.sleep(1)

	boxes = browser.find_elements_by_class_name("letter-container")
	characters = int((len(boxes)) / 6)
	print (characters)

	return characters


def isVowel(ch):
     
    # To handle lower case
    ch = ch.upper()
 
    return (ch == 'A' or ch == 'E' or
            ch == 'I' or ch == 'O' or
            ch == 'U') and ord(ch) >= 65 and ord(ch) <= 90

def isConsonnant(ch):
     
    # To handle lower case
    ch = ch.upper()
 
    return not (ch == 'A' or ch == 'E' or
            ch == 'I' or ch == 'O' or
            ch == 'U') and ord(ch) >= 65 and ord(ch) <= 90
 
def totalVowels(string):
    vowels = ''
    count = 0
     
    for i in range(len(string)):
 
        # To check is character is Consonant
        if (isVowel(string[i])):
        	if vowels.find(string[i].lower())<0:
        		vowels += string[i].lower()

        	#print(string[i].lower())
             
    return vowels

def totalConsonants(string):
    consonants = ''
    count = 0
     
    for i in range(len(string)):
 
        # To check is character is Consonant
        if (isConsonnant(string[i])):
        	if consonants.find(string[i].lower())<0:
        		consonants += string[i].lower()

        	#print(string[i].lower())
             
    return consonants

#def findVowelsConsonants(champs):
#	for x in champs:
#		champArray = []
#		vowels = totalVowels(x)
#		info = x
#		info = {
#		"name" : x,
#		"consonants":"",
#		"vowels": vowels,
#		}
#		print(x)
#		champArray.append(info)
#	print (champArray)

def findVowelsConsonants(champs):
	#could use dictionaries, but takes more work
	champArray = []
	for x in champs:
		print(x)
		#Creates array for every champ, [0] champ name, [1]different Vowels, [2]different Consonants
		champArray.append([x,totalVowels(x),totalConsonants(x)])
#TODO: improve sorting by also sorting on consonants (more different the more info you get)

	champArray.sort(key = lambda x:len(x[1]) )
	return (champArray)

def enterAttempt(string):
	for i in string:
		pyautogui.write(i)
		time.sleep(0.1)
	pyautogui.keyDown('enter')
	pyautogui.keyUp('enter')

#def bestOption(champs):




##selenium




length = findCharacters(wordleURL)

#pyautogui.write('Hell')



#Uncomment for manual input of character length
#length = information()

newChampList = main('https://championmastery.gg/summoner?summoner=a+penguin&region=EUW', length) #filter on amount of characters array of possible candidates

#make filter to choose one of the champs
sortedChampList = findVowelsConsonants(newChampList)
print(sortedChampList)

#try first attempt
lastElement = len(sortedChampList) - 1
firstAttempt = sortedChampList[lastElement][0]
print (firstAttempt)
enterAttempt(firstAttempt)

#what letters where correct?
time.sleep(0.5)

correctLetter = browser.find_elements(By.CLASS_NAME, value='text-amber-100')
print(correctLetter.getText())




champs = filter(newChampList) #filter on specific leters












#Implement system with correctly placed letters
#Seperate champs space names
#remove ` from names
#Implement system that manages best first try etc..
#Make code cleaner
