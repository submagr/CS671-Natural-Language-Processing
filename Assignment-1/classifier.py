import re
from sklearn.datasets import fetch_20newsgroups
import nltk
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
import sys


reload(sys)
sys.setdefaultencoding("utf-8")

#fetch dataset
newsgroups_train = fetch_20newsgroups(subset='train')
#newsgroups_train.data = newsgroups_train.data[:100]
newsgroups_test = fetch_20newsgroups(subset='test')
#newsgroups_test.data = newsgroups_test.data[:20]
vec = DictVectorizer()

sentenceTok = re.compile("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s")
senTermiIndexTrain = []
senTermiIndexTest = []

features = []
window_dicts = []
training_labels = []
testing_labels = []

classifier = LinearSVC()

for article in newsgroups_train.data:
    temp = []
    for m in sentenceTok.finditer(article):
        temp.append(m.start()-1)
    senTermiIndexTrain.append(temp)

for article in newsgroups_test.data:
    temp = []
    for m in sentenceTok.finditer(article):
        temp.append(m.start()-1)
    senTermiIndexTest.append(temp)

k = 0
#training data

for j in range(0,len(newsgroups_train.data)): 
    position = 0;
    newsgroups_train.data[j] = "START " + "START " + newsgroups_train.data[j].rstrip() + " STOP " + "STOP"  
    t = nltk.word_tokenize(newsgroups_train.data[j].encode('utf-8'))  
    tags = nltk.pos_tag(t)                                            
    tags = dict(tags)

    for i in range(2,len(t)-3): 
        position+= len(t[i])
        k += 1
        window = {
            "word-2": t[i-2], 
            "tag-2": tags[t[i-2]], 
            "word-1": t[i-1], 
            "tag-1": tags[t[i-1]], 
            "word+1": t[i+1], 
            "tag+1": tags[t[i+1]], 
            "word+2": t[i+2], 
            "tag+2": tags[t[i+2]]
        }
        window_dicts.append(window)
        if t[i] == '.' and position in senTermiIndexTrain[j]:
            training_labels.append(1)
        else:
            training_labels.append(0)

l = 0
for j in range(0,len(newsgroups_test.data)): 
    position = 0
    newsgroups_test.data[j] = "start " + "start " + newsgroups_train.data[j].rstrip() + " stop " + "stop"
    t = nltk.word_tokenize(newsgroups_test.data[j].encode('utf-8'))
    tags = nltk.pos_tag(t)
    tags = dict(tags)
    for i in range(2,len(t)-3):
        position += len(t[i])
        l += 1
        window = {
            "word-2": t[i-2], 
            "tag-2": tags[t[i-2]], 
            "word-1": t[i-1], 
            "tag-1": tags[t[i-1]], 
            "word+1": t[i+1], 
            "tag+1": tags[t[i+1]], 
            "word+2": t[i+2], 
            "tag+2": tags[t[i+2]] 
        }
        window_dicts.append(window)
        if t[i] == '.' and position in senTermiIndexTest[j]:
            testing_labels.append(1)
        else:
            testing_labels.append(0)

features = vec.fit_transform(window_dicts)

transformer = TfidfTransformer()
transformed = transformer.fit_transform(features)

train = transformed[:k,:]
test = transformed[k:,:]

print "Training on ", len(newsgroups_train.data), " files"
classifier.fit(train, training_labels)

print "Testing on ", len(newsgroups_test.data), " files"
prediction = classifier.predict(test)

correct = 0
for i in range(0,len(testing_labels)):
    if prediction[i] == testing_labels[i]:
        correct += 1
accuracy = correct*1.0/len(testing_labels)
print "Final Accuracy: ", accuracy 
