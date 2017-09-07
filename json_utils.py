import json
# from jsonschema import validate
from file_utils import *

def writeJSONToFile(argJsonString, argFileName):
	fileContents = json.dumps(argJsonString)
	writeToFile(fileContents, argFileName)

def readJSONFromFile(argFileName):
	fileContents = readFromFile(argFileName)
	return json.loads(fileContents)

# def validateJSON(argJsonString, argJsonSchema):
# 	return jsonschema.validate(argJsonString, argJsonSchema)


def main():
	ourDict = { "a" : "b" }
	writeJSONToFile(ourDict, "boys")

if __name__ == "__main__":
	main()