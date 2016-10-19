from gensim.models import Word2Vec
from nltk.corpus import brown
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

googleModel = Word2Vec.load_word2vec_format('models/GoogleNews-vectors-negative300.bin', binary=True)  
print "Google model loaded"

# Caps => Small
sentences = [[word.lower() for word in sentence] for sentence in brown.sents()]
model = Word2Vec(brown.sents(), size = 300)
print "Skip gram trained on Brown words"

cosineSim = []
print "Computing Cosine Similarities"
for word in model.vocab:
    if word in googleModel:
        cosineSim.append(cosine_similarity(googleModel[word], model[word])[0][0])

plt.hist(cosineSim, bins = [x*0.1 for x in range(-10,11)])
plt.show()
