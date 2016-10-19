from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Input, merge, TimeDistributed, Activation
import numpy as np
from collections import defaultdict
from nltk.corpus import brown

# PseudoCode for preprocessing
# tagset: is created after ignoring all tags which are present less than 50 times + 'NA' tag
# vocab: trim all sentences to 50 length
# input feature vector : length 50: word_index in vocab
# output feature vector : length 50: each a vector of size total tags (one hot representation)

count_tags = {}   
for word, tag in brown.tagged_words():
    count_tags[tag] = count_tags.setdefault(tag, 0) + 1
tags = {}
index = 0
for tag, count in count_tags.items():
    if count >50: 
        tags[tag] = index
        index+=1
tags['NA'] = -1

vocab = {}
index = 0
for sentence in brown.tagged_sents():
    for length, tagged_word in enumerate(sentence):
        word = tagged_word[0].lower()
        if length<50 and word not in vocab:
            vocab[word] = index
            index+=1

X_train = [] 
y_train = []
for sentence in brown.tagged_sents():
    #TODO: Check why accuracy decreased drastically when -1 was used in both
    inp_vector = [0]*50
    out_vector = [[0]*len(tags)]*50
    for length, tagged_word in enumerate(sentence):
        if length>=50:
            break
        word = tagged_word[0].lower()
        tag = tagged_word[1]

        inp_vector[length] = vocab[word]

        one_hot_tag_vector = [0]*len(tags)
        if tag in tags:
            one_hot_tag_vector[tags[tag]] = 1
        else:
            one_hot_tag_vector[tags['NA']] = 1
        out_vector[length] = one_hot_tag_vector
    X_train.append(inp_vector)
    y_train.append(out_vector)

print "Data preprocessing .."

max_features = 50000
batch_size = 16

print('Build model...')
model = Sequential()
model.add(Embedding(max_features, 128, input_length=50))

model.add(LSTM(128,return_sequences=True))  
model.add(Dropout(0.5))
model.add(TimeDistributed(Dense(len(tags))))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',metrics=['accuracy'], optimizer='adam', class_mode="binary")
print(model.summary())

print("Training..")

model.fit(X_train[0:(int)(len(X_train)*0.80)], y_train[0:(int)(len(y_train)*0.80)], batch_size=batch_size, nb_epoch=3, validation_split=0.2, show_accuracy=True, shuffle=True)
score, acc = model.evaluate(X_train[(int)(len(X_train)*0.80): len(X_train)], y_train[(int)(len(y_train)*0.80): len(y_train)], batch_size=batch_size, show_accuracy=True)
print('Test score:', score)
print('Test accuracy:', acc)
