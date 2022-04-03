from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from readDoc import *
import certifi
import ssl
import time
from tkinter import Tk

#discord stuff
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks # Importing tasks here





## Raspbi/Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
chrome_options = Options()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--disable-gpu')
#chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options, executable_path='C:\gecko\chromedriver.exe')
#browser = None
#browser.close()


##Firefox
#from selenium import webdriver
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
#from selenium.webdriver.common.by import By
#browser = webdriver.Firefox(executable_path='C:\gecko\geckodriver.exe')


#discord Stuff
load_dotenv()

client = discord.Client()





wordleURL = 'https://yordle.pages.dev/'
champURL = 'https://championmastery.gg/summoner?summoner=a+penguin&region=EUW'


#Some global variables
blackLetters = []
orangeLetters = []
greenLetters = []
global countGlobal
countGlobal = 0



def sortLength(rawChampList	, length, category):
	champCorrectLength = []
	sortChampList = []
	champList = []
	champListName = []
	champListDoubleArray = []
	champCorrectLengthLower = []

	if rawChampList == None: #error management
		print("empty object in sort length")
	#Get name of Champs from data into champListName

	if category	== 'online': 
		for name in rawChampList:
			champListName.append(name.get_text())
			#print(champListName)
	else:
		champListName = rawChampList

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
	for name in champCorrectLength:
		champCorrectLengthLower.append(name.lower())
	return champCorrectLengthLower


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

def filter(champs, greenLetters, orangeLetters, blackLetters): #filter on the random placed letters
	#letters = input("letters that are correct:").split()
	#print (letters)
	x = 0 #counter for position in name attempt
	for letter in greenLetters:
		champs = [name for name in champs if name[x] == letter or letter == ' '] #check if empty slot or same letter in same place
		x += 1
	for letter in orangeLetters:
		champs = [name for name in champs if name.find(letter) >= 0] #returns position of letters from 0...n
	for letter in blackLetters:
		champs = [name for name in champs if name.find(letter) == -1]
	print("---------------- Possible champs with current letters --------------------")
	print(champs)


	return champs

def findCharacters(url):
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
		webdriver.ActionChains(browser).send_keys(i).perform()
		time.sleep(0.1)
	webdriver.ActionChains(browser).send_keys(Keys.RETURN).perform()


def startSession(url):
	browser.get(url)
#-----------Remove line if not in incognito anymore ---------
	time.sleep(5)
	#	closePopup = browser.find_element_by_class_name('absolute right-4 top-4')
	closePopup = browser.find_element(By.ID, "headlessui-dialog-overlay-4")
	
	action = webdriver.common.action_chains.ActionChains(browser)
	action.move_to_element_with_offset(closePopup, 5, 5)
	action.click()
	action.perform()
	time.sleep(1)
	return


#def bestOption(champs):




def main(category):
	blackLetters = []
	orangeLetters = []
	greenLetters = []		

	#find length of the attempts
	length = findCharacters(wordleURL)

	#initialyse the array of correct Letters
	for i in range(length):
			greenLetters.append(' ')

	#Uncomment for manual input of character length
	#length = information()


	#-------- depending on URL based or TXTbased documents
	if category == 'online':
		rawChampList = getChampions(champURL) #only supported for champs currently
	else:
		print('igothere')
		rawChampList = readText(category)
		time.sleep(3)
	print(rawChampList)
	

	newChampList = sortLength(rawChampList, length, category) #filter on amount of characters array of possible candidates
	print(newChampList)

	#make filter to choose one of the champs
	sortedChampList = findVowelsConsonants(newChampList)
	print(sortedChampList)

	#try first attempt
	lastElement = len(sortedChampList) - 1
	attempt = sortedChampList[lastElement][0]
	print (attempt)

	#attempt = 'leona'

	for i in range(6):
		x = 0
		print(i)
		#make choice here
		if i > 0:
			newChampList = filter(newChampList, greenLetters, orangeLetters, blackLetters)
			attempt = newChampList[0] #TODO don't make it first element of the list
		time.sleep(2)
		enterAttempt(attempt)
		newChampList.remove(attempt)
		time.sleep(5)
		allChrHTML = browser.find_element(By.CLASS_NAME, value= 'pb-20')
		rowChrHTML = allChrHTML.find_elements(By.CLASS_NAME, value ='mb-1')


		chrContainerHTML = rowChrHTML[i].find_elements(By.CLASS_NAME, 'w-14')
		for y in chrContainerHTML: #for every container in the row
			skip = 0
			chrInContainer = y.find_element(By.XPATH, './/*').text
			print(y.get_attribute("class"))

			if y.get_attribute("class").find('dark:bg-transparent') >= 0:
				#print("faulty")
				#print (chrInContainer)
				for letter in greenLetters:
					if letter.find(chrInContainer.lower()) >= 0:
						skip = 1
				for letter in orangeLetters: 
					if letter.find(chrInContainer.lower()) >= 0:
						skip = 1
				if skip == 0:
					blackLetters.append(str(chrInContainer).lower())
					print('black: ')
					print(blackLetters)
			if y.get_attribute("class").find('dark:border-green-700') >= 0:
				#print("green")
				#print(chrInContainer)
				greenLetters[x] = (str(chrInContainer).lower())
				print('green: ')
				print(greenLetters)
			if y.get_attribute("class").find('dark:border-amber-700') >= 0:
				#print("orange")
				#print(chrInContainer)
				orangeLetters.append(str(chrInContainer).lower())
				print('orange: ')
				print(orangeLetters)
			x += 1
		win = len(greenLetters)
		correctChrs = 0
		for greenLetter in greenLetters:
			win = len(greenLetters)
			if greenLetter != ' ':
				correctChrs +=1
			if correctChrs == win:
				print("YOU FOUND THE CORRECT ANSWER")
				print("---------------------------------------FINAL ANSWER---------------------------------------")
				print("--------				"+attempt+"				-------------")
				print("---------------------------------------FINAL ANSWER---------------------------------------")
				return
				browser.quit()
				exit("fuck yeah")



	#Implement system with correctly placed letters
	#Seperate champs space names
	#remove ` from names
	#Implement system that manages best first try etc..
	#Make code cleaner
@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$wordle'):
		await message.channel.send("'You can't beat me' -Kayle" )
		await message.channel.send("I'm currently solving the worlde" )
		startSession(wordleURL)
		main("champions.txt")
		time.sleep(5)
		browser.find_element(By.CLASS_NAME,'px-9').click()

		await message.channel.send("Found the champ, now onto the abilities" )
		main("abilities.txt")
		time.sleep(5)
		browser.find_element(By.CLASS_NAME,'hover\:bg-indigo-700').click()
		time.sleep(5)
		share = Tk().clipboard_get()
		await message.channel.send("GOTTEM!" )
		##TODO make discord bot that shares "share"

		print(share)
		browser.execute_script("window.localStorage.clear();")
		browser.get('https://www.google.com/')
		#browser.refresh()
		#exit("Congrats")

		await message.channel.send(share)
		return


client.run(os.getenv('TOKEN'))
