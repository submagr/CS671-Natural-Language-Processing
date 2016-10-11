import nltk
from nltk.corpus import brown 

##Create Train-Test sets
data = brown.tagged_words()
print "Total number of tagged words in brown corpus = ", len(data)
train_data = data[0:(int)(0.80*len(data))]
test_data = data[(int)(0.80*len(data))+1: len(data)]
print "Size of train data = ", len(train_data)
print "Size of test data = ", len(test_data)

predicted = nltk.pos_tag([x[0] for x in test_data])
## Get accuracy on test set

correct = 0
index = 0
for word, tag in predicted:
    assert(word == test_data[index][0])
    if test_data[index][1] == tag:
        correct+=1
    index+=1

print "Accuracy is ", correct*1.0/len(test_data)
## Accuracy comes around 0.602649006623
#TODO: This is done by without seeing context. There must be some context based package in nltk
