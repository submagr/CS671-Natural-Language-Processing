from nltk.corpus import brown 
from multiprocessing import Pool
import string
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re

# Get brown data
rawData = brown.tagged_sents()

# Lower case, stopword removal, trim sentences
def preprocess(rawSentence):
    sentence = [] 
    index = 0
    for word, tag in rawSentence:
        if index >= 20:
            break
        index+=1
        word = word.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(word)
        filtered_words = [w for w in tokens if not w in stopwords.words('english')]
        if (''.join(filtered_words)) != '':
            sentence.append((''.join(filtered_words), tag))
    return sentence

data = [] 
for rawSentence in rawData: 
    sentence = preprocess(rawSentence)
    if len(sentence) > 2:
        data.append(preprocess(rawSentence))

# Create tag set
count_tags = {}   
for sent in data:
    for word, tag in sent:
        count_tags[tag] = count_tags.setdefault(tag, 0) + 1

tags = set() 
for tag, count in count_tags.items():
    if count >500: 
        tags.add(tag)
tags.add('NA')

# Change tags with less numbers to NA
totalWords = 0
for sent in data:
    for i, (word, tag) in enumerate(sent):
        totalWords+=1
        if tag not in tags:
            sent[i] = (word, 'NA')
 
trainData = data[0: int(0.80*len(data))]
testData = data[int(0.80*len(data)): len(data)]
print "data ready after preprocessing"
print "Train set size (#sentences): ", len(trainData), " Test set size: ", len(testData)
#Viterbi Algorithm

##Get counts for calculation of probabilities from train data.

counts = {}
# We need 3 counts: 
# - count of (word, tag)
# - count of (tag1)
# - count of (tag1, tag2)
# - count of (tag1, tag2, tag3)
for sent in trainData:
    sent = [('', 'START'),('', 'START')] + sent + [('', 'STOP')]
    for index, tagged_word in enumerate(sent): 
        counts[tagged_word] = counts.setdefault(tagged_word, 0) + 1
        counts[tagged_word[1]] = counts.setdefault(tagged_word[1], 0) + 1
        try : 
            if index - 1 >= 0:
                prev = sent[index - 1]
                counts[(prev[1], sent[index][1])] = counts.setdefault((prev[1], sent[index][1]), 0) + 1
                try:
                    if index-2 >= 0: 
                        prevPrev = sent[index - 2]
                        counts[(prevPrev[1], prev[1], sent[index][1])] = counts.setdefault((prevPrev[1], prev[1], sent[index][1]), 0) + 1
                except: 
                    pass
        except: 
            pass
print "training done: calculated counts on train set"

def getProb(v, z, u=None):
    #print "in getProb: {0}, {1}, {2} ".format(v, z, u)
    alpha1, alpha2, alpha3 = 0.5, 0.3, 0.2
    assert(alpha1 + alpha2 + alpha3 == 1)
    if u==None:
        assert(counts[z]!=0)
        return (counts.setdefault((v,z), 1)*1.0)/counts[z]
    else:
        den1 = counts.setdefault((z,u), 0)
        if den1 == 0:
            p1 = 0
        else: 
            p1 = (counts.setdefault((z,u,v),0)*1.0)/den1
        p2 = (counts.setdefault((u,v), 0)*1.0)/counts[u]
        p3 = (counts[v]*1.0)/totalWords
        return alpha1*p1 + alpha2*p2 + alpha3*p3

def multiRunWrapper(args):
    return calcPi(*args)

def calcPi(k, u, v, tagged_word):
    lst = []
    Y[k-2] = getTagSet(k-2)
    for z in Y[k-2]: 
        lst.append(((k,u,v), z, prevPi[(k-1, z, u)]*getProb(v, z, u)*getProb(tagged_word[0], v)))
    return max(lst, key = lambda item:item[2])

def getTagSet(k):
    if k<1:
        return ['START'] 
    else:
        return tags

numWords = 0 
totalCorrects = 0 
for sent in testData: 
    pi = {(0,'START', 'START'):1}
    bPtr = {}
    for k, tagged_word in enumerate(sent):
        prevPi = pi
        pi = {}
        k += 1

        print '>>>>>>>>', k, tagged_word
        Y = {}
        Y[k-1] = getTagSet(k-1)
        Y[k] = getTagSet(k)
        # Multiprocess code
        #p = Pool(4)
        #res = p.map(multiRunWrapper, [(k,u,v,tagged_word) for u in Y[k-1] for v in Y[k]])
        #for item in res:
        #    bPtr[item[0]] = item[1] 
        #    pi[item[0]] = item[2]
        # Simple code
        for u in Y[k-1]:
            for v in Y[k]:
                temp = calcPi(k, u, v, tagged_word)
                bPtr[(k,u,v)] = temp[1]
                pi[(k,u,v)] = temp[2]
    predTags = []
    lst = []
    for u in Y[k-1]:
        for v in Y[k]:
            lst.append(((u,v),pi[(k,u,v)]*getProb('STOP', u, v))) 
    temp = max(lst, key=lambda item:item[1])[0]
    predTags = [temp[0], temp[1]]
    for k in range(k-2, 0, -1) :
        predTags = [bPtr[(k+2, predTags[0], predTags[1])]] + predTags
    correct = 0 
    for index, tagged_word in enumerate(sent):
        if tagged_word[1] == predTags[index]:
            correct+=1
    print predTags
    print "accuracy = ", correct*1.0/len(sent)
    numWords+=len(sent)
    totalCorrects+=correct
    print "Overall accuracy uptill now= ", totalCorrects*1.0/numWords

#sent = [(u'doubt', u'NN')        ,
#        (u'mrs', u'NP')          ,
#        (u'meeker', u'NP')       ,
#        (u'snubbed', u'VBN')     ,
#        (u'many', 'NA')          ,
#        (u'time', u'NN')         ,
#        (u'felt', u'VBD')        ,
#        (u'grief', u'NN')        ,
#        (u'passing', u'NN')      
#        ]
#
#pi = {(0,'START', 'START'):1}
#bPtr = {}
#tempPi = []
#for k, tagged_word in enumerate(sent):
#    tempPi.append(pi)
#    prevPi = pi
#    pi = {}
#    k += 1
#
#    print '>>>>>>>>', k, tagged_word
#    Y = {}
#    Y[k-1] = getTagSet(k-1)
#    Y[k] = getTagSet(k)
#    # Multiprocess code
#    #p = Pool(4)
#    #res = p.map(multiRunWrapper, [(k,u,v,tagged_word) for u in Y[k-1] for v in Y[k]])
#    #for item in res:
#    #    bPtr[item[0]] = item[1] 
#    #    pi[item[0]] = item[2]
#    # Simple code
#    for u in Y[k-1]:
#        for v in Y[k]:
#            temp = calcPi(k, u, v, tagged_word)
#            bPtr[(k,u,v)] = temp[1]
#            pi[(k,u,v)] = temp[2]
#predTags = []
#lst = []
#for u in Y[k-1]:
#    for v in Y[k]:
#        lst.append(((u,v),pi[(k,u,v)]*getProb('STOP', u, v))) 
#temp = max(lst, key=lambda item:item[1])[0]
#predTags = [temp[0], temp[1]]
#for k in range(k-2, 0, -1) :
#    predTags = [bPtr[(k+2, predTags[0], predTags[1])]] + predTags
#correct = 0 
#for index, tagged_word in enumerate(sent):
#    if tagged_word[1] == predTags[index]:
#        correct+=1
#print predTags
#print "accuracy = ", correct*1.0/len(sent)
#numWords+=len(sent)
#totalCorrects+=correct
#print "Overall accuracy uptill now= ", totalCorrects*1.0/numWords
