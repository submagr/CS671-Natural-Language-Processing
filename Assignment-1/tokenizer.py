import re
import sklearn  
from sklearn.datasets import fetch_20newsgroups
import nltk

ngData = fetch_20newsgroups(subset='all')

## Word Tokenizer
wordTok = re.compile("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+")

## Sentence Tokenizer
sentenceTok = re.compile("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s")

sentenceSegmented = []
wordsSegmented = []
for article in ngData.data[:30]:
    tempSen = []
    tempWords = []
    tempWords.append(wordTok.findall(article))
    tempSen.append(sentenceTok.findall(article))
    sentenceSegmented.append(tempSen)
    wordsSegmented.append(tempWords)

## Morphological Analyzer

morphologicalTokens = []
for article in ngData.data[:30]:
    text = nltk.word_tokenize(article)
    morphologicalTokens.append(nltk.pos_tag(text))
