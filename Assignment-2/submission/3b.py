from sklearn.datasets import load_svmlight_file 
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfTransformer

vocabFileName = "aclImdb/imdb.vocab"
trainBowFileName = "aclImdb/train/labeledBow.feat"
testBowFileName = "aclImdb/test/labeledBow.feat"

X_train, y_train = load_svmlight_file(trainBowFileName)
X_test, y_test = load_svmlight_file(testBowFileName, X_train.shape[1])

def convertTagsToBinary(y):
    for i in range(len(y)):
        if y[i] <=5:
            y[i] = -1
        else:
            y[i] = 1
    return y

y_train = convertTagsToBinary(y_train)
y_test  = convertTagsToBinary(y_test)
print "Test Train data loaded"

tfIdf = TfidfTransformer()
X_train = tfIdf.fit_transform(X_train)
X_test  = tfIdf.fit_transform(X_test)

clf = SVC()
clf.fit(X_train, y_train) 
meanAccuracy = clf.score(X_test, y_test)
print "Accuracy = ", meanAccuracy
