from sklearn.svm import SVC
import os
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec
import numpy as np

train_pos = [os.path.join("aclImdb/train/pos", z) for z in os.listdir("aclImdb/train/pos")][1:10]
train_neg = [os.path.join("aclImdb/train/neg", z) for z in os.listdir("aclImdb/train/neg")][1:10]
test_pos  =   [os.path.join("aclImdb/test/pos", z) for z in os.listdir("aclImdb/test/pos")][1:10]
test_neg  =   [os.path.join("aclImdb/test/neg", z) for z in os.listdir("aclImdb/test/neg")][1:10]

def read_dir(lst):
    sentences = []
    for fileName in lst:
        sentences+=[word_tokenize(sentence) for sentence in sent_tokenize(open(fileName).read().decode("ascii","ignore").encode("ascii"))]
    return sentences

sentences = read_dir(train_pos+train_neg+test_pos + test_neg)

model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
model.init_sims(replace=True)
 
##TODO: Dump and reuse trained vectors


X_train = []
y_train = []
X_test = []
y_test = []

def getVector(document):
    count = 0
    vector = np.ndarray
    for word in document:
        if word in model.vocab:
            if count == 0: 
                vector = model[word]
            else: 
                vector = (vector*count + model[word])/(count+1)
            count+=1
    return vector


for fileName in train_pos: 
    document = word_tokenize(open(fileName).read().decode("ascii","ignore").encode("ascii"))
    X_train.append(getVector(document))
    y_train.append(1)

for fileName in train_neg: 
    document = word_tokenize(open(fileName).read().decode("ascii","ignore").encode("ascii"))
    X_train.append(getVector(document))
    y_train.append(-1)

for fileName in test_pos: 
    document = word_tokenize(open(fileName).read().decode("ascii","ignore").encode("ascii"))
    X_test.append(getVector(document))
    y_test.append(1)

for fileName in test_neg: 
    document = word_tokenize(open(fileName).read().decode("ascii","ignore").encode("ascii"))
    X_test.append(getVector(document))
    y_test.append(-1)

clf = SVC()
clf.fit(X_train, y_train) 
meanAccuracy = clf.score(X_test, y_test)
print "Accuracy = ", meanAccuracy

a = '''spd-say "Boss! Accuracy came out to be {0}" '''.format(meanAccuracy)
os.system(a)
