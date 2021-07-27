import tweepy
import re
import csv
from textblob import TextBlob
import nltk
import io
import base64
import urllib.parse
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

def createTestData(testData):
    test = []
    wo = []
    with open(testData,'r') as t:
        lineReader = csv.reader(t, delimiter=',')
        for row in lineReader:
            if row:
                test.append({"text":row[0]})
                tweets = row[0].split(" ")
                wo.append(tweets)
    return (test,wo)
testData="D:/SKRIPSI/corpus/detokenize_test.csv"
test, wo = createTestData(testData)
print(test[:10])
eng = TextBlob(test)
try:
    eng = eng.translate(to='en')
except Exception as e:
    pass
print(eng[:10])