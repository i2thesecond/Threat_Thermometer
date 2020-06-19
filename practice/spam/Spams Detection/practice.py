import nltk
import csv


d = []
sentences = ''
allWords = []

with open('/root/Documents/NLP/Threat_Thermometer/practice/spam/Spams Detection/smsspamcollection/SMSSpamCollection') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        d.append((nltk.word_tokenize(row[1]), row[0]))
        sentences = sentences + row[1] + ' '
        #d[row[1]] = row[0]
        #sentences.append(row[1])
print(d[1])
print(sentences)
allWords = nltk.word_tokenize(sentences)
print(allWords)
# define feature extractor
allWords = nltk.FreqDist(allWords)
wordFeatures = list(allWords.keys())
