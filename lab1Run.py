
from lab1Support import *
import sys

def runlab1Bakery(dataSet, minSup, minConf, supportData):


   # Read in dataSet
   bakeryData = pd.read_csv(dataSet,sep = '\n', header = None)
   bakeryData = bakeryData.iloc[:,0].values
   bakeryData = [list(map(int, x.split(','))) for x in bakeryData]
   for x in bakeryData:
      del x[0]
 
   # Read in goods and make dictionary
   goods = pd.read_csv('goods.csv')
   goodsVal = goods['Flavor'].astype(str)  + goods['Food'].astype(str)

   goodsDict = dict(zip(goods['Id'], goodsVal))

   # Print results
   findRules(bakeryData, minSup, minConf, goodsDict)

def runlab1Bingo(dataSet, minSup, minConf, supportData):


   # Read in dataSet
   bingoData = pd.read_csv(dataSet,sep = '\n', header = None)
   bingoData = bingoData.iloc[:,0].values
   bingoData = [list(map(int, x.split(','))) for x in bingoData]
   for x in bingoData:
      del x[0]
   for x in bingoData:
      for i, val in enumerate(x):
         if val == 1:
            del x[i]
 
   # Read in goods and make dictionary
   authors = pd.read_csv(supportData,sep = '|', header = None)
   authorsDict = dict(zip(list(authors[0]), list(authors[1])))

   # Print results
   findRules(bingoData, minSup, minConf, authorsDict)

def runlab1Transcription(dataSet, minSup, minConf, supportData):


   # Read in dataSet
   basketFactors = pd.read_csv(dataSet,sep = '\n', header = None)
   baskets = basketFactors.iloc[1:,0].values
   baskets = [list(map(int, x.split(','))) for x in baskets]
   for x in baskets:
      del x[0]

   # Format data for function
   newBaskets = []
   for x in baskets:
      pairs = x[::2]
      newBaskets.append(pairs)

   # Get counts of each transcription
   allElements = [item for basket in newBaskets for item in basket]
   count = {}
   for c in allElements:
      if c not in count:
         count[c] = 1
      else:
         count[c] += 1

   # Get items that occur in all or almost in all baskets and others
   highOccuring = []
   for key, value in count.items():
      if value >= 40:
         highOccuring.append(key)
   # Remove items from market baskets that are in high occuring
   fullbaskets = []
   for i, basket in enumerate(newBaskets):
      tmpBasket = []
      for j, tran in enumerate(basket):
         if tran not in highOccuring:
            tmpBasket.append(tran)
      fullbaskets.append(tmpBasket)
 
   # Read in goods and make dictionary
   factors = pd.read_csv(supportData)
   factorsDict = dict(zip(list(factors['tf_id']), list(factors['transfac'])))

   # Print results
   findRulesGene(fullbaskets, minSup, minConf, factorsDict)

   # Get support of all of the ones we excluded and print
   supportNon = [(factorsDict[x], support(x, newBaskets)) for x in highOccuring]
   print("")
   print("")
   print("Transcription factors occuring in almost every market basket >= 40/47")
   print("->These transcription factors were removed from the market baskets<-")
   print("------------------------------------------------------------")
   for i, itemSet in enumerate(supportNon):
      print('HighSet #', str(i+1) + ") Factor ->", itemSet[0], "    Support: ", itemSet[1])


# Get values and run program
def runCode():
   # Get arguments
   dataSet = sys.argv[1]
   minSup = float(sys.argv[2])
   minConf = float(sys.argv[3])
   supportData = sys.argv[4]
   whichData = sys.argv[5]

   # Check which datatype and run accordingly

   if whichData == 'Bakery':
      runlab1Bakery(dataSet, minSup, minConf, supportData)
   elif whichData == 'Bingo':
      runlab1Bingo(dataSet, minSup, minConf, supportData)
   else:
      runlab1Transcription(dataSet, minSup, minConf, supportData)


runCode()









