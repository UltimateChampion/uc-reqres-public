def readFromFile(argFileName):
	with open(argFileName, 'r') as theFile:
		return theFile.read()

def writeToFile(argString, argFileName):
	with open(argFileName, 'w') as theFile:
		theFile.write(argString)
		theFile.close()
