from gensim.models import Word2Vec
from nltk.corpus import brown
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

model = Word2Vec(brown.sents()[1:10])

def getGoogleVec(word):
    #TODO: Return real google vector here
    return model[word]

cosineSim = []
for word in model.vocab:
    googleVec = getGoogleVec(word)
    cosineSim.append(cosine_similarity(googleVec, model[word])[0][0])

plt.hist(cosineSim, bins = [x*0.1 for x in range(0,11)])
plt.show()
