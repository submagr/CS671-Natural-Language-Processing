from nltk.corpus import brown 

##Create Train-Test sets
data = brown.tagged_words()
print "Total number of tagged words in brown corpus = ", len(data)
train_data = data[0:(int)(0.80*len(data))]
test_data = data[(int)(0.80*len(data))+1: len(data)]
print "Size of train data = ", len(train_data)
print "Size of test data = ", len(test_data)

##Create a dictionary that contains word - count
counts = {}
for tagged_word in train_data:
    counts[tagged_word[0]] = counts.setdefault(tagged_word[0], (tagged_word[1], 1)) 
    counts[tagged_word[0]]=(counts[tagged_word[0]][0], counts[tagged_word[0]][1] - 1);
    if counts[tagged_word[0]][1] < 0 :
        counts[tagged_word[0]] = (tagged_word[1], 0)

## Get accuracy on test set

correct = 0;
for tagged_word in test_data:
    if tagged_word[0] in counts and counts[tagged_word[0]][0] == tagged_word[1]:
        correct+=1;

print "Accuracy is ", correct*1.0/len(test_data)
## Accuracy comes around 0.8566083069954099


