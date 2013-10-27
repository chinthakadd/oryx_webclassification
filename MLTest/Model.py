import Orange, cPickle

data = Orange.data.Table("dataset.csv")
bayes = Orange.classification.bayes.NaiveLearner()
classifier = bayes(data)
cPickle.dump(classifier, open("oryx1.pck", "wb"))



