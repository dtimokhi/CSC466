
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import itertools

# In[5]:

def support(item, baskets):
    top = sum([1 if item in basket else 0 for basket in baskets])
    bottom = len(baskets)
    return top*1.0/bottom


# In[6]:

def getPairs(F, k):
    outList = []
    for first in F:
        for second in F:
            if len(first) == len(second) == k:
                outList.append([first, second, tuple(set(first) | set(second))])
    return outList 


# In[7]:

def getSubsets(tmpTuple):
    size = len(tmpTuple) - 1
    return set(itertools.combinations(list(tmpTuple), size))


# In[8]:

def candidate(F,k):
    C = set()
    for pair in getPairs(F,k):
        if len(pair[2]) == len(pair[0]) + 1:
            c = pair[2]
            flag = True
            for s in getSubsets(c):
                if s not in F:
                    flag = False
            if flag == True:
                if c not in C:
                    C.add(tuple(c))
    return C


# In[9]:

def apriori(T, minSup):
    FullSupport = []
    I =  list(set(x for l in T for x in l))
    Fk = []; Fk.append(None);
    firstIter = set(tuple([x]) for x in filter(lambda a: a != -1, [x if support(x, T) >= minSup else -1 for x in I]))
    Fk.append(firstIter)
    k = 2
    while len(Fk[k-1]) != 0:
        Ck = candidate(Fk[k-1], k-1)
        count = {}
        for c in Ck:
            count[c] = 0
        for t in T:
            for c in Ck:
                if set(c) <= set(tuple(t)):
                    count[c] += 1
        tmpFk = []
        for c in Ck:
            if count[c]*1.0/len(T) >= minSup:
                tmpFk.append(c)
        Fk.append(set(tmpFk))
        newSet = set(x for x in Fk[k-1])
        for newTerm in Fk[k]:
            for oldTerm in Fk[k-1]:
                if set(oldTerm).issubset(newTerm) == True:
                    if oldTerm in newSet:
                        newSet.remove(oldTerm)
                        #print("After: ", newSet)
        Fk[k-1] = set(tuple(sorted(x)) for x in newSet)
        k += 1
    Fk = Fk[1:-1]
    return Fk
                    

# In[10]:

def getCorrect():
    t = np.linspace(.05, .01, 20)
    for minS in t:
        ap = addNamesFreq(apriori(bakery1000M, minS),goodsDict)
        print("---- Apriori: ", minS, " ----")
        print("NumRules: ", len(genRules(bakery1000M, ap, .85)))
        for i, val in enumerate(ap):
            print(i+1, ": ", len(val))
            


# In[11]:

def genRules(data, freqItemSet, minConf):
    allRules = []
    freqItemSet = freqItemSet[1:]
    freqItemSet = [item for sublist in freqItemSet for item in sublist]
    for itemSet in freqItemSet:
        for item in itemSet:
            noItem=set(itemSet)-(set([item]))
            item = set([item])
            conf = confidence(data,noItem,item)
            sup = supportOut(data,noItem,item)
            confItem = [noItem, item, conf, sup]
            if conf >= minConf:
                allRules.append(confItem)
                
            
    return allRules
                    


# In[12]:

def confidence(T,set1,set2): #Dataset,leftSideList,rightSideList
    top = sum([1 if (set1|set2) <= set(basket) else 0 for basket in T])
    bottom = sum([1 if (set1) <= set(basket) else 0 for basket in T])
    if(bottom == 0 | top == 0):
        return 0
    return top*1.0/bottom


# In[13]:

def supportOut(T, set1,set2):
    return sum([1 if (set1|set2) <= set(basket) else 0 for basket in T])/len(T)


# In[15]:

def getSupportFreq(T, output):
    allFreq = []
    for groupSize in output:
        for term in groupSize:
            termSup = supportOut(T, set(term), set([]))
            termOut = [term,termSup]
            allFreq.append(termOut)
    return allFreq
            
    


# In[16]:

def addNamesFreq(output, goods):
    groupList=[]
    for i, basket in enumerate(output):
        basketList = []
        for value in list(basket[0]):
            basketList.append(goods[value])
        groupList.append([basketList, basket[1]])
    return groupList


# In[77]:

def addNames(output, goods):
    ruleList = []
    for i, rule in enumerate(output):
        termList = []
        for j, terms in enumerate(rule[:-2]):
            setList = []
            for k, objectId in enumerate(list(terms)):
                setList.append(goods[objectId])
            termList.append(setList)
        termList.append(rule[2])
        termList.append(rule[3])
        ruleList.append(termList)
    return ruleList  


# In[73]:

def printCorrectly(output):
    for i, rule in enumerate(output):
        print("Rule: ", str(i), '   ', ','.join(rule[0]), " --> ", 
                rule[1][0]) 
        print("              Support: ", str(rule[3]))
        print("              Confidence: ", str(rule[2]))
        


# In[76]:

def findRules(T, minSup, minConf, goodsDictTmp, needsNames = True):
    aprioriOutput = apriori(T, minSup)
    aprioriNames = None
    if(needsNames == True):
        aprioriNames = addNamesFreq(getSupportFreq(T, aprioriOutput), goodsDictTmp)
        for i, itemSet in enumerate(aprioriNames):
            print('Set # ', i+1, " ", itemSet)
    genRulesOutput = genRules(T, aprioriOutput, minConf)
    if(needsNames == True):
        genRulesOutput = addNames(genRulesOutput, goodsDictTmp)
    print("**********************************************")
    printCorrectly(genRulesOutput)
    


# In[103]:

def findRulesGene(T, minSup, minConf, goodsDictTmp, needsNames = True):
    aprioriOutput = apriori(T, minSup)
    aprioriNames = None
    if(needsNames == True):
        aprioriNames = addNamesFreq1(getSupportFreq(T, aprioriOutput), goodsDictTmp)
        for i, itemSet in enumerate(aprioriNames):
            print('Set # ', i+1, " ", itemSet)
    genRulesOutput = genRules(T, aprioriOutput, minConf)
    if(needsNames == True):
        genRulesOutput = addNames1(genRulesOutput, goodsDictTmp)
    print("**********************************************")
    printCorrectly1(genRulesOutput)
    #return genRulesOutput


# In[94]:

def addNamesFreq1(output, goods):
    groupList=[]
    for i, basket in enumerate(output):
        basketList = []
        for value in list(basket[0]):
            basketList.append(tuple([goods[value[0]],value[1]]))
        groupList.append([basketList, basket[1]])
    return groupList


# In[118]:

def addNames1(output, goods):
    ruleList = []
    for i, rule in enumerate(output):
        termList = []
        for j, terms in enumerate(rule[:-2]):
            setList = []
            for k, objectId in enumerate(list(terms)):
                setList.append(str(str(goods[objectId[0]]) + "," + str(objectId[1])))
            termList.append(setList)
        termList.append(rule[2])
        termList.append(rule[3])
        ruleList.append(termList)
    return ruleList


# In[130]:

def printCorrectly1(output):
    for i, rule in enumerate(output):
        print("Rule: ", str(i), '   ', ' & '.join(rule[0]), " --> ", 
                rule[1][0]) 
        print("              Support: ", str(rule[3]))
        print("              Confidence: ", str(rule[2]))
        

# In[21]:

def findMinSupport(dataSet,goodsDict):
    t = np.linspace(.05, .01, 5)
    for minSup in t:
        print("******* ",minSup," *******")
        findRules(dataSet, minSup, .8, goodsDict, bakery=True)
    






