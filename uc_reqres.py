import math

from json_utils import *
from datetime import *

class UCReqRes:

	class Hasher:
		hashFunction = hash

	class UCReqResException(Exception):
		pass

	def __init__(self, **kwargs):
		self.metaData = kwargs.get("reqResMetaData", None)
		self.metaDataHash = self.Hasher.hashFunction(self.metaData)
		self.data = kwargs.get("reqResData", None)
		self.chunkInfo = kwargs.get("chunkInfo", [1, 1])

	def __str__(self):
		return "REQ_RES: {}\nHASH: {}\nDATA: {}\nCHUNK: {}/{}\n\n".format(self.metaData, self.metaDataHash, self.data, self.chunkInfo[0], self.chunkInfo[1])

	def makeMetaData(self, metaData):
		self.metaData = metaData
		self.metaDataHash = self.Hasher.hashFunction(self.metaData)

	def makeData(self, data):
		self.data = data

	def stringify(self):
		return json.dumps({ "reqResMetaData" : self.metaData , "reqResData" : self.data })

	def chunkData(self, chunkSize):
		chunkedReqResList = []

		dataLength = len(self.data)
		dataLengthFloat = float(dataLength)
		totalChunksCeil = math.ceil(dataLengthFloat/chunkSize)
		totalChunks = int(totalChunksCeil)

		chunkNum = 1

		for i in range(0, totalChunks):
			start = i * chunkSize
			end = min(dataLength , start + chunkSize)

			currentChunk = self.data[start:end]
			currentReqRes = UCReqRes(reqResMetaData = self.metaData, reqResData = currentChunk, chunkInfo = [chunkNum, totalChunks])
			chunkedReqResList.append(currentReqRes)

			chunkNum += 1
			
		return chunkedReqResList

	def aggregateChunks(self, chunks):

		def validateMetaDataHashes(chunks):
			currentMetaDataHash = None
			for chunk in chunks:
				if currentMetaDataHash is None:
					currentMetaDataHash = chunk.metaDataHash
				elif currentMetaDataHash != chunk.metaDataHash:
					raise UCReqResException("Error Validating Chunking Aggregation: Metadata Hash Mismatch in Chunks! Mismatch ")

		def validateOrdering(chunks):
			prevIdx = 0
			totalNum = None
			for chunk in chunks:
				if totalNum is None:
					totalNum = chunk.chunkInfo[1]
				elif totalNum != chunk.chunkInfo[1]:
					raise self.UCReqResException("Error Validating Chunking Aggregation: Mismatch of Number of Chunks!")

				if prevIdx != chunk.chunkInfo[0] - 1:
					raise self.UCReqResException("Error Validating Chunking Aggregation: Ordering Fail!")
				prevIdx = chunk.chunkInfo[0]

			numChunks = len(chunks)
			if numChunks != totalNum:
				raise self.UCReqResException("Error Validating Chunking Aggregation: Mismatch of Number of Chunks With List of Chunks!")


		validateMetaDataHashes(chunks)
		validateOrdering(chunks)

		aggregatedData = ""
		metaData = None

		for chunk in chunks:
			print chunk
			metaData = chunk.metaData
			aggregatedData += chunk.data

		self.makeData(aggregatedData)
		self.makeMetaData(metaData)

def main():
	print "Hello World"
	ucrr = UCReqRes(reqResMetaData="metadata here!", reqResData = "This is a test string to try to chunk stuff!")
	print ucrr
	ucrrChunks = ucrr.chunkData(10)

	ucrr2 = UCReqRes()
	ucrr2.aggregateChunks(ucrrChunks)
	print ucrr2


if __name__ == "__main__":
	main()

