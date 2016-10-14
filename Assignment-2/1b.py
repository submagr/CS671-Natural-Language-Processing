from nltk.corpus import brown 
from multiprocessing import Pool

#Create Train-Test sets
data = brown.tagged_sents()
print "Total number of tagged words in brown corpus = ", len(data)
train_data = data[0:(int)(0.80*len(data))]
test_data = data[(int)(0.80*len(data))+1: len(data)]
print "Size of train data = ", len(train_data)
print "Size of test data = ", len(test_data)

#Viterbi Algorithm
##Get counts for calculation of probabilities from train data.
counts = {}
vocabulary = set() 
tags = set()
for sent in train_data:
    sent = [('', 'START'),('', 'START')] + sent + [('', 'STOP')]
    for index, tagged_word in enumerate(sent): 
        tags.add(tagged_word[1])
        vocabulary.add(tagged_word[0])
        counts[tagged_word] = counts.setdefault(tagged_word, 0) + 1
        counts[tagged_word[1]] = counts.setdefault(tagged_word[1], 0) + 1
        try : 
            prev = sent[index - 1]
            counts[(prev[1], sent[1])] = counts.setdefault((prev[1], sent[1]), 0) + 1
            try:
                prevPrev = sent[index - 2]
                counts[(prevPrev[1], prev[1], sent[1])] = counts.setdefault((prevPrev[1], prev[1], sent[1]), 0) + 1
            except: 
                pass
        except: 
            pass

def getProb(v, z, u=None):
    if u==None:
        assert(counts[z] != 0)
        assert(counts.setdefault((v,z), 0) <= counts[z])
        return (counts.setdefault((v,z), 0) + 1)*1.0/ counts[z]
    else:
        den = counts.setdefault((z,u), 0)
        if den == 0:
            return 0
        else: 
            return (counts.setdefault((z,u,v),0)+1)*1.0/den

def multiRunWrapper(args):
    return calcPi(*args)

def calcPi(k, u, v):
    lst = []
    for z in Y[k-2]: 
        #print pi[(k-1, z, u)], getProb(v, z, u), getProb(tagged_word[0], v)
        lst.append(((k,u,v), z, pi[(k-1, z, u)]*getProb(v, z, u)*getProb(tagged_word[0], v)))
    return max(lst, key = lambda item:item[1])

def getTagSet(k):
    if k<=1:
        return ['START'] 
    else:
        return tags

numWords = 0 
totalCorrects = 0 
for sent in test_data: 
    pi = {(0,'START', 'START'):1}
    bPtr = {}
    sent = [('', 'START'),('', 'START')] + sent 
    for k, tagged_word in enumerate(sent):
        print '>>>>>>>>', k, tagged_word
        k += 1
        Y = {}
        Y[k-2] = getTagSet(k-2)
        Y[k-1] = getTagSet(k-1)
        Y[k] = getTagSet(k)
        p = Pool(4)
        res = p.map(multiRunWrapper, [(k,u,v) for u in Y[k-1] for v in Y[k]])
        for item in res:
            bPtr[item[0]] = item[1] 
            pi[item[0]] = item[2]
    predTags = []
    lst = []
    for u in Y[k-1]:
        for v in Y[k]:
            assert(pi[(k,u,v)])
            lst.append(((u,v),pi[(k,u,v)*getProb('STOP', u, v)])) 
    temp = max(lst, key=lambda item:item[1])[0]
    predTags = [temp[0], temp[1]] + predTags
    for k in range(k-2, 0, -1) :
        predTags = [bPtr[(k, predTags[0], predTags[1])]] + predTags
    correct = 0 
    for index, tagged_word in enumerate(sent):
        if tagged_word[1] == predTags[index]:
            correct+=1
    print "accuracy = ", correct*1.0/len(sent)
    break
    numWords+=len(sent)
    totalCorrects+=correct
print "Overall accuracy = ", totalCorrects*1.0/numWords
