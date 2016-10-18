import nltk
from nltk.corpus import wordnet as wn

nouns = list(wn.all_synsets(wn.NOUN))
verbs = list(wn.all_synsets(wn.VERB))

updatedNoun = []
updatedVerb = []
for i in nouns:
	updatedNoun.append(i.name().split('.')[0])

for i in verbs:
	updatedVerb.append(i.name().split('.')[0])



file = open('lex.txt', 'w')

file.write("Multichar_Symbols +N +V +PastPart +Past +PresPart +3P +Sg +Pl\nLEXICON Root\nNoun ;\nVerb ;")
file.write("\nLEXICON Noun\n")

for i in updatedNoun:
	file.write("%s Ninf;\n" % i)

file.write("\nLEXICON Verb\n")	

for i in updatedVerb:
	file.write("%s Vinf;\n" % i)


file.write("LEXICON Ninf\n+N+Sg:0   #;\n+N+Pl:^s  #;\nLEXICON Vinf\n+V:0             #;\n+V+3P+Sg:^s      #;\n+V+Past:^ed      #;\n+V+PastPart:^ed  #;\n+V+PresPart:^ing #;")