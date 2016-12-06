__author__ ='maulisye'

import difflib
from preproses import prosesStemdanLem
from nltk.corpus import stopwords
from nltk.corpus import wordnet

ppdbDict={}
ppdbSim =0.81

nesim=0.81
neDict={}

#Mengidentifikasi kata identik
def Kata_Identik(word1,word2):
    if word1 ==word2:
        return 1
    else:
        return 0


def alignmentChunk(W1,W2):
    true=1
    nilai=0
    synonyms = []
    antonyms = []
    if (Kata_Identik(W1,W2)== true) :
        nilai=nilai+5
        print nilai
    for syn in wordnet.synsets(W1):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    if (synonyms==W2) :
        print synonyms,"=",W2
    # print(set(synonyms))
    # print(set(antonyms))



def alignIdenticalWord(jmlline,aligned1,aligned2,W1,W2):
    word1= []
    word2= []
    align_identic=0
    for y in range(0,jmlline):
        for i in range(0,len(W1[y])):
            for j in range(0,len(W2[y])):
                align_identic = align_identic + Kata_Identik((W1[y][i]).lower(),(W2[y][j]).lower())
            if align_identic >= 1 :
                word1.append(W1[y][i])
                align_identic = 0
        aligned1.append(word1)
        word1= []
        for x in range(0,len(W2[y])):
            for z in range(0,len(W1[y])):
                align_identic = align_identic + Kata_Identik((W2[y][x]).lower(),(W1[y][z]).lower())
            if align_identic >= 1 :
                word2.append(W2[y][x])
            align_identic = 0
        aligned2.append(word2)
        word2= []
################################################################################
#Paraphrase
#def loadPPDB(ppdbNamaFile='dataTA/penting/ppdb-1.0-xxxl-lexical.extended.synonyms.uniquepairs'):

def loadPPDB(ppdbNamaFile='dataTA/penting/ppdb-2.0-xxxl-lexical'):
    global ppdbSim
    global ppdbDict

    count = 0

    Fileppdb = open(ppdbNamaFile, 'r')
    for line in Fileppdb:
        if line == '\n':
            continue
        tokens = line.split()
        tokens[1] = tokens[1].strip()
        ppdbDict[(tokens[0], tokens[1])] = ppdbSim
        count += 1


################################################################################


################################################################################
def presentInPPDB(word1, word2):
    global ppdbDict

    if (word1.lower(), word2.lower()) in ppdbDict:
        return True
    if (word2.lower(), word1.lower()) in ppdbDict:
        return True



def align_ppdb(jml_line,aligned_word1PPDB,aligned_word2PPDB,W1,W2):

    word1PFA = []
    word2PFA = []
    for y in range(jml_line):
        for i in range(len(W1[y])):
            for j in range(len(W2[y])):
                if presentInPPDB((W1[y][i]), (W2[y][j])):
                    word1PFA.append(W1[y][i])
        aligned_word1PPDB.append(word1PFA)
        word1PFA = []

        for x in range(len(W2[y])):
            for z in range(len(W1[y])):
                if presentInPPDB(((W2[y][x]).lower()), ((W1[y][z]).lower())):
                    word2PFA.append(W2[y][x])
        aligned_word2PPDB.append(word2PFA)
        word2PFA = []
################################################################################
#NE / named entity

def LoadNE(neNamaFile='dataTA/penting/ne.txt'):
    global nesim
    global neDict

    count=0
    FileNe =open(neNamaFile,'r')
    for line in FileNe:
        if line == '\n':
            continue
        tokens = line.split('\t')
        tokens[1]= tokens[1].strip()
        neDict[(tokens[0].lower(), tokens[1].lower())] = nesim
        count+=1


def presentInNE(word1, word2):

    global neDict

    if (word1.lower(), word2.lower()) in neDict:
        return True
    if (word2.lower(), word1.lower()) in neDict:
        return True

def align_NE (jml_lines,aligned_word1NE,aligned_word2NE,W1,W2):
    word1NE =[]
    word2NE =[]
    for y in range(jml_lines):
        for i in range(len(W1[y])):
            for j in range(len(W2[y])):
                if presentInNE((W1[y][i]),(W2[y][j])):
                    word1NE.append(W1[y][i])
        aligned_word1NE.append(word1NE)
        word1NE=[]

        for x in range(len(W2[y])):
            for z in range(len(W1[y])):
                if presentInNE(((W2[y][x]).lower()),((W1[y][z]).lower())):
                    word2NE.append(W2[y][x])
        aligned_word2NE.append(word2NE)
        word2NE= []

        for k in range(len(W1[y])-1):
            for l in range(len(W2[y])-1):
                if presentInNE(((W1[y][k])+" "+(W1[y][k+1])),((W2[y][l])+" "+(W2[y][l+1]))):
                    word1NE.append(W1[y][k])
                    word1NE.append(W1[y][k+1])
        aligned_word1NE.append(word1NE)
        word1NE=[]

        for p in range(len(W2[y])-1):
            for q in range(len(W1[y])-1):
                if presentInNE(((W2[y][p])+" "+(W2[y][p+1])),((W1[y][q])+" "+(W1[y][q+1]))):
                    word2NE.append(W1[y][p])
                    word2NE.append(W1[y][p+1])
        aligned_word2NE.append(word2NE)
        word2NE= []


#matching

def match(W1,W2):
    matchers = difflib.SequenceMatcher(a=W1,b= W2) #lib difflib digunakan untuk membndingkan sequence
    for block in matchers.get_matching_blocks():
        if block.size <2 :
            continue
        yield  ' '.join(W1[block.a:block.a+block.size])

def WordSequenceAlignment(sequenceList,W1,W2,jmlline):
    temp =[]
    for y in range(jmlline):
        temp.append(list(match(W1[y],W2[y])))
    for z in range(jmlline) :
        if (len(temp[z])>0):
            for a in range(len(temp[z])):
                temp[z][a]=temp[z][a].split(' ')
        sequenceList.append(temp[z])

#konteks teks

def KonteksTeks(sentence1,sentence2,stopwords):
    s1index=[]
    s2index=[]
    c1=[]
    c2=[]
    konteks=[]
    for ortu in range(len(sentence1)):
        s1index.append([sentence1[ortu,ortu]])

    for tmn in range(len(sentence2)):
        s2index.append([sentence2[tmn,tmn]])

    for a in range(len(s1index)):
        for b in range(1,3):
            k=a-b
            l=a+b
            if k and l !=a :
                if k or l == s1index[a][1]:
                    if s1index[a][0] not in stopwords:
                        if s1index[a] not in c1:
                            c1.append(s1index[a])

    for b in range(len(s2index)):
        for c in range(1,3):
            m=b-c
            y=b+c
            if m and y != b:
                if m or y ==s2index[b][1]:
                    if s2index[b][0] not  in stopwords:
                        if s2index[b] not in c2:
                            c2.append(s2index[b])

    for w in range(len(c1)):
        for m in range(len(c2)):
            konteks.append([c1[w],c2[m]])
    return konteks


def alignSurroundingWord(konteks):
    skor=0
    for i in range(len(konteks)):
        skor=Kata_Identik(konteks[i][0][0],konteks[i][1][0])
    print (skor)


##############################################################################################################################
def wordRelatedness(word1, pos1, word2, pos2):
    global stemmer
    global ppdbSim
    global punctuations

    if len(word1) > 1:
        canonicalWord1 = word1.replace('.', '')
        canonicalWord1 = canonicalWord1.replace('-', '')
        canonicalWord1 = canonicalWord1.replace(',', '')
    else:
        canonicalWord1 = word1

    if len(word2) > 1:
        canonicalWord2 = word2.replace('.', '')
        canonicalWord2 = canonicalWord2.replace('-', '')
        canonicalWord2 = canonicalWord2.replace(',', '')
    else:
        canonicalWord2 = word2

    if canonicalWord1.lower() == canonicalWord2.lower():
        return 1

    if stemmer.stem(word1).lower() == stemmer.stem(word2).lower():
        return 1

    if canonicalWord1.isdigit() and canonicalWord2.isdigit() and canonicalWord1 <> canonicalWord2:
        return 0

    if pos1.lower() == 'cd' and pos2.lower() == 'cd' and (
        not canonicalWord1.isdigit() and not canonicalWord2.isdigit()) and canonicalWord1 <> canonicalWord2:
        return 0

    # stopwords can be similar to only stopwords
    if (word1.lower() in stopwords and word2.lower() not in stopwords) or (
            word1.lower() not in stopwords and word2.lower() in stopwords):
        return 0

    # punctuations can only be either identical or totally dissimilar
    if word1 in punctuations or word2 in punctuations:
        return 0

    if presentInPPDB(word1.lower(), word2.lower()):
        return ppdbSim
    else:
        return 0


##############################################################################################################################

a = loadPPDB()
print a

