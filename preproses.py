
__author__ ='maulisye'
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer



#inp = open('dataTA/STSint.testinput.headlines.sent2.txt').read()
dataRoot = [line.rstrip('\n') for line in open('dataTA/penting/rootwords.txt')]
def removeNoChunk(token):
    # menghapus semua tanda
    token = re.sub(r'([A-Z])\w+', '', str(token))
    token = re.sub(r'[,"(-)$-\']', '', str(token))  # menghapus tanda hubung , ' . ;
    token = re.sub(r'[-\']', '', str(token))  # menghapus ]
    token = re.sub('\n', '', str(token))
    return token
def tokenWord(data):
    #tokenisasi berdasarkan kata
    return  data.split(' ')

def tokenFrase(data):
    #tokenisasi berdasarkan frase
    return data.split(']')

def tokenChunk(data):
    return data.split(']')

def Removal(token):
    #menghapus semua tanda {,(,[ :
     token = re.sub(r'[>[)}:{",?.(<]', '', str(token))
     token = re.sub(r']','',str(token)) #menghapus ]
     token = re.sub(r'[.,;"-$-\']', '', str(token)) # menghapus tanda hubung , ' . ;
     token = re.sub('\n', '', str(token))
     return token

dataStopword ='dataTA/penting/stopwords.txt'
file = open(dataStopword)
stopwords = file.read().splitlines()

def Hapus_stopword(token):
    if token.lower() in stopwords :
        token=''
    return token

def lematisasi (token):
    #lem= WordNetLemmatizer()
    token= WordNetLemmatizer().lemmatize(token)
    return token

def stemming(token):
    #porter_stemmer = PorterStemmer()
    token = PorterStemmer().stem_word(token)
    return  token

def prosesStemdanLem (input):
    # if input in dataRoot :

        token = stemming(input)
        token = lematisasi(token)
        return token


# inp = " only"
# print "lema =",lematisasi(inp)
# print "stem =", stemming(inp)
# print "dua2nya = ",prosesStemdanLem(inp)
def chunking(input):
    return input