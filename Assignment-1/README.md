#Assignment-1: Morphological Analyzer, Word Tokenizer, Sentence Termination Identification
This assignment deals with the most common tasks of natural language and processing course: 
- Word tokenizer: Given a sentence, find out individual word tokens 
- Sentence termination identification: Given a document, find out sentence boundaries 
- Morphological Analyzer: Given a word, identify root word \+ word forms and vice-versa

## Word and Sentence Tokenizer:
For tokenizing word and sentences, I've used regular expressions
- Word tokenizer's regex:
```python 
	[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+
```
Explaination from [link](http://stackoverflow.com/a/6203000):
	- [A-Z]{2,}(?![a-z]) matches words with all letters capital
	- [A-Z][a-z]+(?=[A-Z]) matches words with a first captitel letter. The lookahead (?=[A-Z]) stops the match before the next capital letter
	- [\'\w\-]+ matches all the rest, i.e. words which may contain ' and -. 

- Sentence tokenizer's regex:
```python 
	(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s
```
Reference: [link](http://stackoverflow.com/a/25736082):

## Morphological Analyzer
For morphological analysis, I've used [foma](https://code.google.com/archive/p/foma/). Very nice tutorial is uploaded [here](Resources/Foma-tutorial/) in this repository.
- Nouns and Verbs from nltk.corpus.wordnet are used as lexicon
- Nouns are appended with 
	+N+Sg:0			 #;
	+N+Pl:^s		 #;
- Verbs are appended with 
	+V:0             #;
	+V+3P+Sg:^s      #;
	+V+Past:^ed      #;
	+V+PastPart:^ed  #;
	+V+PresPart:^ing #;
	# above means end of generation process. ^ means end of morpheme
- The technique used is first verb/noun + possible forms(plural, singular, past etc.) is generated using lexicon. Then, various filter rules are applied to handle edge cases. The rules are: 
	- ConsonantDoubling g -> g g || _ "^" [i n g | e d ];
	- EDeletion e -> 0 || _ "^" [ i n g | e d ] ;
	- EInsertion [..] -> e || s | z | x | c h | s h _ "^" s ;
	- YReplacement y -> i e || _ "^" s    ,, 
	- KInsertion [..] -> k || V c _ "^" [e d | i n g];
	- Cleanup "^" -> 0;

## Sentence Terminator Classifier:
- Dataset used: *20-newsgroup* dataset, contains 18000 news documents tagged in 20 categories  
- Extracted sentence termination index using regex are treated as Ground truth for training and testing
- Feature Vector: For every word in sentence: used surrounding words and tags within window size = 2. For example: In sentence S = "Hello! How do you do?" Feature of word "do" will be 
```python
{
	"Hello", pos\_tag("Hello"),
	"How", pos\_tag("How"),
	"you", pos\_tag("you"),
	"do", pos\_tag("do")
}
```
and it's label will be -1 since it is not end of sentence
- Linear SVC modeled is trained using sentences from 11,314 documents and tested on 7532 documents from newsgroup dataset
- Accuracy came out to be 99.98%
