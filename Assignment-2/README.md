#Assignment 2: Tagging, Word and document vectors, sentiment analysis

##Language models using brown corpus
Brown corpus contains 1161192 tagged words. We'll use this to create our own word tagger using different methods. Using 80:20 as train:test division, following results are obtained: 

- Naive Approach: Give the most frequent tag to the word in the dataset.
	Accuracy = 0.8566083069954099
- Using nltk tagger: 0.602649006623 :0
- Viterbi Parser:
	- About Viterbi Algorithm: Viterbi algorithm is used in nlp for tagging sequence problem (Given a sentence, you have to produce tags). 

##Viterbi Algorithm

##TF-IDF
- numerical statistic that is intended to reflact how important a word is to a document
- tf-idf value increases proportionally to the number of times a word appear in document but is offset by the frequency of the word in the corpus, which helps to adjust for the fact that some words appear more frequently in general. 

##Document Models: 
- 3a: Accuracy = 0.73284
- 3b: Accuracy = 0.63416
- 3c: Accuracy =  0.63068
- 3d: 0.51004
- 3e: 0.50172
