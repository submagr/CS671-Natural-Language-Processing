import os
from sklearn.datasets import load_svmlight_file 
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfTransformer
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

model = Word2Vec(sentences, size=10, window=5, min_count=5, workers=4)
model.init_sims(replace=True)
 
##TODO: Dump and reuse trained vectors

X_train = []
y_train = []
X_test = []
y_test = []
vocabFileName = "aclImdb/imdb.vocab"
trainBowFileName = "aclImdb/train/labeledBow.feat"
testBowFileName = "aclImdb/test/labeledBow.feat"

freq_train, y_train = load_svmlight_file(trainBowFileName)
freq_test, y_test = load_svmlight_file(testBowFileName, freq_train.shape[1])

vocab = [word.strip() for word in open("aclImdb/imdb.vocab").readlines()]

X_train = []
X_test = []
for row in freq_train:
    vector = []
    for index, col in enumerate(row):
        word = vocab[index]
        try:
            vector += [x*col[0,index] for x in list(model[word])]
        except: 
            pass
    X_train.append(vector)

for row in freq_test:
    vector = []
    for index, col in enumerate(row):
        word = vocab[index]
        try:
            vector += [x*col[0,index] for x in list(model[word])]
        except: 
            pass
    X_test.append(vector)


def convertTagsToBinary(y):
    for i in range(len(y)):
        if y[i] <=5:
            y[i] = -1
        else:
            y[i] = 1
    return y

y_train = convertTagsToBinary(y_train)
y_test  = convertTagsToBinary(y_test)
print "Test Train data loaded"


clf = SVC()
clf.fit(X_train, y_train) 
meanAccuracy = clf.score(X_test, y_test)
print "Accuracy = ", meanAccuracy

