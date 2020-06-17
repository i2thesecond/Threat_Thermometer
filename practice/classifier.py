#! /usr/local/bin/python3

from nltk.corpus import names
import nltk
import random

names = ([(name, 'male') for name in names.words('male.txt')] + [(name,'female.txt') for name in names.words('female.txt')])

random.shuffle(names)

def gender_features(word):
    return {'last_letter': word[-1]}

featuresets = [(gender_features(n), g) for (n,g) in names]
train_set, test_set = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)

def classify_name(name):
    print(name + ' classify as ' + classifier.classify(gender_features(name)))

classify_name('Ashley')

classifier.show_most_informative_features(5)

def gender_features2(name):
    features = {}
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
        features["has({})".format(letter)] = (letter in name.lower())
    return features

print(gender_features2('Ashley'))
