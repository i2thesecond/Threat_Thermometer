import nltk
import csv


documents = []
sentences = ''
allWords = []

with open('/root/Documents/NLP/Threat_Thermometer/practice/spam/Spams Detection/smsspamcollection/SMSSpamCollection') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        documents.append((nltk.word_tokenize(row[1]), row[0]))
        sentences = sentences + row[1] + ' '
        #d[row[1]] = row[0]
        #sentences.append(row[1])
allWords = nltk.word_tokenize(sentences)
print(allWords)
# define feature extractor
allWords = nltk.FreqDist(allWords)
print(allWords)
word_features = list(allWords)

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

featuresets = [(document_features(d),c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))


