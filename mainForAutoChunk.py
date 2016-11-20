__author__ = 'maulisye'
from preproses import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import  nltk
#headlinesC ='dataTA/gabung.txt' #udah di chunk yang headline
headlinesC ='dataTA/data/gabungan.txt' #Coba aja dulu hehehe
#headline ='dataTA/STSint.testinput.headlines.sent2.txt'

# membaca inputan Data chunk
data = open(headlinesC.lower())
baca = data.readlines()
#hitung jumlah baris data
jml_line = sum(1 for line in open(headlinesC))
print  "Jumlah baris :",jml_line




# r =[]
# text = nltk.word_tokenize(" Conservatives sweep to Australia election victory ")
# print  nltk.pos_tag(text)
# sentence = nltk.pos_tag(text)
# grammar = "NP:{<DT>?<JJ>*<NN>}"
# cp = nltk.RegexpParser(grammar)
# result = cp.parse(sentence)
# r.append(result)
# print result.draw()
# print r

i= 0

couple = [] #menyimpan pasangan ayat dalam indeks terpisah
tokenW1 =[]
tokenW2 =[]
potonganP1 =[]
potonganP2 =[]

#PREPROSES#

#tag
for i in range(0,jml_line):
    couple.append(baca[i].split('\t'))

    tokenW1.append(tokenWord(couple[i][0]))
   # print tokenW1
    tokenW2.append(tokenWord(couple[i][1]))
  #  print tokenW2

    potonganP1.append(tokenFrase(couple[i][0]))
    potonganP2.append(tokenFrase(couple[i][1]))

    #removal tagnya
    for j in range(len(tokenW1[i])):
        tokenW1[i][j]=Removal(tokenW1[i][j])
        tokenW1[i][j]=Hapus_stopword(tokenW1[i][j])
    for j in range(len(tokenW2[i])):
        tokenW2[i][j]=Removal(tokenW2[i][j])
        tokenW2[i][j]=Hapus_stopword(tokenW2[i][j])

    #removal tag berdasarkan frasenya

    for j in range(len(potonganP1[i])):
        potonganP1[i][j]=Removal(potonganP1[i][j])
       # potonganP1[i][j]=Hapus_stopword(potonganP1[i][j])
    for j in range(len(potonganP2[i])):
        potonganP2[i][j]=Removal(potonganP2[i][j])
       # potonganP2[i][j]=Hapus_stopword(potonganP2[i][j])

#Hapus spasi token
    j=0
    while j < len(tokenW1[i]) :
        if tokenW1[i][j]=='':
            tokenW1[i].pop(j)
        else:
            j +=1

    j = 0
    while j < len(tokenW2[i]):
        if tokenW2[i][j] == '':
            tokenW2[i].pop(j)
        else:
            j += 1

#Berdasarkan frase hapus spasinya
    j = 0
    while j < len(potonganP1[i]):
        if potonganP1[i][j] == '':
            potonganP1[i].pop(j)
        else:
            j += 1

    j = 0
    while j < len(potonganP2[i]):
        if potonganP2[i][j] == '':
            potonganP2[i].pop(j)
        else:
            j += 1

k=0
HasilChunk1=[]
HasilChunk2=[]
def removeNoPar(token):
    # menghapus semua tanda
    token = re.sub(r'([A-Z])\w+', '', str(token))
    token = re.sub(r'[,"-$-\']', '', str(token))  # menghapus tanda hubung , ' . ;
    token = re.sub('\n', '', str(token))
    return token
for k in range(0,jml_line):
     print ("==========================================================================================================================")
     print ("==========================================================================================================================")
     print ("Pasangan ayat Al-qur'an Ke- ",k+1)
     print (couple[k][0])
     print (couple[k][1])
     r1 = []
     r2 = []
     text = nltk.word_tokenize((couple[k][0]).lower())
     text2 = nltk.word_tokenize((couple[k][1]).lower())


     sentence1 = nltk.pos_tag(text)
     sentence2 = nltk.pos_tag(text2)
     # grammar = "NP:{<DT>?<JJ>*<NN>}"
     grammar = r"""
     Chunk:{<PP>*<NP>},
     Chunk:{<VP>*<PRT>},
     Chunk:{<DT>?<JJ>*<NN>}
     """
     cp = nltk.RegexpParser(grammar)
     result1 = cp.parse(sentence1)
     result2 = cp.parse(sentence2)

     r1.append(result1)
     r2.append(result2)


     print (" Pasangan ayat Al-quran yang sudah di chunk :")
     print "result1",result1
     print result2
     # print "Hasil chunk 1:",HasilChunk1
     # print "Hasil chunk 2:",HasilChunk2
     # print result1.draw()
     # print result2.draw()
     jml=0
     HasilChunk11=[]
     HasilChunk22=[]
     for subtree1 in result1.subtrees(filter=lambda t: t.label() == 'Chunk'):
         print ("hasil subtree :", subtree1)
         HasilChunk11.append(subtree1)

     for subtree2 in result2.subtrees(filter=lambda t: t.label() == 'Chunk'):
         print ("hasil subtree :", subtree2)
         HasilChunk22.append(subtree2)

     HasilChunk1.append(HasilChunk11)
     HasilChunk2.append(HasilChunk22)
     print "chunk 1 ya", HasilChunk1[k]
     print "chunk 2 ya", HasilChunk2[k]
     print "Jumalah chunk 1 di potongan ayat 1:",len(HasilChunk1[k])
     print (" Hasil Proses tokenisasi : ")
     print (tokenW1[k])
     print (tokenW2[k])
     #
     k +=1


for hsl in HasilChunk1:
    print "Sementara 1",str(hsl)+"\n"


# print ("Pasangan ayat Al-qur'an : ")
# c1= couple[4][0]
# c2=couple[4][1]
# print (c1)
# print (c2)


#print result1.draw()
#print  r1

#print result2.draw()
#print  r2



# l=0
# for l in range(0,jml_line):
#     print (" Hasil Proses tokenisasi : ",l+1)
#     print (tokenW1[l])
#     print (tokenW2[l])


#Lemmatization
for y in range(0,jml_line):
    for tes1 in range(len(tokenW1[y])):
        t = unicode(tokenW1[y][tes1], errors='replace')
        tokenW1[y][tes1]=prosesStemdanLem(t)
        #print t
        #print  tokenW1[y][tes1]

    for tes2 in range(len(tokenW2[y])):

        ts2 = unicode(tokenW2[y][tes2], errors='replace')
        tokenW2[y][tes2] = prosesStemdanLem(ts2)
        #print t
        #tokenW2[y][tes2]=lematisasi((tokenW2[y][tes2]).lower())
        #print  tokenW2[y][tes2]

