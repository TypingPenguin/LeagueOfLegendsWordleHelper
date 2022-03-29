
#reads file and outputs array of elements

def readText(textFile):
	f = open(textFile,'r')
	elements = f.read().split(',')
	f.close()
	return elements	