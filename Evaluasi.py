
__author__ = 'maulisye'
from preproses import *
import sys
import time
# reload(sys)
# sys.setdefaultencoding('utf8')
start_time=time.time()
headlinesC ='dataTA/gabung.txt' #udah di chunk yang headline

# membaca inputan Data chunk
data = open(headlinesC)
baca = data.readlines()
headlinesBC ='dataTA/gabungBC.txt'

# membaca inputan Data chunk
data1 = open((headlinesBC).lower())
baca1 = data1.readlines()
#hitung jumlah baris data
jml_line = sum(1 for line in open(headlinesC))
print  "Jumlah baris :",jml_line
jml_line1 = sum(1 for line in open(headlinesBC))
print  "Jumlah baris :",jml_line1
i= 0

coupleChunk = [] #menyimpan pasangan ayat dalam indeks terpisah
tokenW1Chunk =[]
tokenW2Chunk =[]
potonganP1Chunk =[]
potonganP2Chunk =[]

#PREPROSES#

#tag
a=0
for a in range(0,5):
    coupleChunk.append(baca[a].split('\t'))

    tokenW1Chunk.append(tokenChunk((coupleChunk[a][0]).lower()))
   # print tokenW1
    tokenW2Chunk.append(tokenChunk((coupleChunk[a][1]).lower()))
  #  print tokenW2

    potonganP1Chunk.append(tokenFrase(coupleChunk[a][0]))
    potonganP2Chunk.append(tokenFrase(coupleChunk[a][1]))

    #removal tagnya
    for j in range(len(tokenW1Chunk[a])):
        tokenW1Chunk[a][j]=Removal(tokenW1Chunk[a][j])
        tokenW1Chunk[a][j]=Hapus_stopword(tokenW1Chunk[a][j])
    for j in range(len(tokenW2Chunk[a])):
        tokenW2Chunk[a][j]=Removal(tokenW2Chunk[a][j])
        tokenW2Chunk[a][j]=Hapus_stopword(tokenW2Chunk[a][j])

    #removal tag berdasarkan frasenya

    for j in range(len(potonganP1Chunk[a])):
        potonganP1Chunk[a][j]=Removal(potonganP1Chunk[a][j])
       # potonganP1[i][j]=Hapus_stopword(potonganP1[i][j])
    for j in range(len(potonganP2Chunk[a])):
        potonganP2Chunk[a][j]=Removal(potonganP2Chunk[a][j])
       # potonganP2[i][j]=Hapus_stopword(potonganP2[i][j])

#Hapus spasi token
    j=0
    while j < len(tokenW1Chunk[a]) :
        if tokenW1Chunk[a][j]=='':
            tokenW1Chunk[a].pop(j)
        else:
            j +=1

    j = 0
    while j < len(tokenW2Chunk[a]):
        if tokenW2Chunk[a][j] == '':
            tokenW2Chunk[a].pop(j)
        else:
            j += 1

#Berdasarkan frase hapus spasinya
    j = 0
    while j < len(potonganP1Chunk[a]):
        if potonganP1Chunk[a][j] == '':
            potonganP1Chunk[a].pop(j)
        else:
            j += 1

    j = 0
    while j < len(potonganP2Chunk[a]):
        if potonganP2Chunk[a][j] == '':
            potonganP2Chunk[a].pop(j)
        else:
            j += 1


for a in range(0,5):
    print ("==========================================================================================================================")
    print ("==========================================================================================================================")
    print ("Pasangan ayat Al-qur'an Ke- ", a + 1)
    print "ayat 1 = ", coupleChunk[a][0]
    print "ayat 2 = ", coupleChunk[a][1]
    print ("Tokenisasi :")
    print "ayat 1 = ", tokenW1Chunk[a]
    print "ayat 2 = ", tokenW2Chunk[a]




i= 0

couple = [] #menyimpan pasangan ayat dalam indeks terpisah
tokenW1 =[]
tokenW2 =[]
potonganP1 =[]
potonganP2 =[]

#PREPROSES#

#tag
for i in range(0,jml_line):
    couple.append(baca1[i].split('\t'))
    i+=1

k=0
Chunk1=[]
Chunk2=[]
HasilChunkFIX1=[]
HasilChunkFIX2=[]


align_word=[]
word1=[]
word2=[]
identik=[]
ss=[]
s_identic=[]
sim_identic=[]
align1=[]
align2=[]
konteksKata =[]
alignIdentic=0


aligned_word1PPDB=[]
aligned_word2PPDB=[]
hasilPFA=[]

#loadPPDB(ppdbNamaFile='dataTA/penting/ppdb-2.0-xxxl-lexical')
#loadPPDB(ppdbNamaFile='dataTA/penting/ppdb-1.0-xxxl-lexical.extended.synonyms.uniquepairs')
#align_ppdb (jml_line,aligned_word1PPDB,aligned_word2PPDB,tokenW1,tokenW2)

#for k in range(0,jml_line-300):

def Kata_Identik(word1,word2):
    if word1 ==word2:
        return 1
    else:
        return 0
#
for k in range(0,5):
     print ("==========================================================================================================================")
     print ("==========================================================================================================================")
     print ("Pasangan ayat Al-qur'an Ke- ",k+1)
     print "ayat 1 = " ,couple[k][0]
     print "ayat 2 = ",couple[k][1]
     r1 = []
     r2 = []
     text1 = nltk.word_tokenize(Removal((couple[k][0]).lower()))
     text2 = nltk.word_tokenize(Removal((couple[k][1]).lower()))
     #print "text 1:",text1

     sentence1 = nltk.pos_tag(text1)
     sentence2 = nltk.pos_tag(text2)
     # grammar = "NP:{<DT>?<JJ>*<NN>}"
     grammar = r"""
     Chunk:{<IN>}
     Chunk:{<RB>}
     Chunk:{<V.*>}
     Chunk:{<P> <NP>}
     Chunk:{<NP>?<CC>*<NP>}
     Chunk:{<PP>*<NP>}
     Chunk:{<VP>*<PRT>}
     Chunk:{<V> <NP|PP>*}
     Chunk:{<PP>*<NP>}
     Chunk:{<PRP>*<VP>*<PRT>}
     Chunk:{<DT>?<JJ>*<NN>}
     """
     cp = nltk.RegexpParser(grammar)
     result1 = cp.parse(sentence1)
     result2 = cp.parse(sentence2)

     r1.append(result1)
     r2.append(result2)


     # print (" Pasangan ayat Al-quran yang sudah di chunk :")
     # #nampilin parsernya
     # print "result1",result1
     # print "result2",result2
     jml=0
     HasilChunk11=[]
     HasilChunk22=[]
     for subtree1 in result1.subtrees(filter=lambda t: t.label() == 'Chunk'):
         #print "hasil subtree 1:", subtree1
         HasilChunk11.append(subtree1)

     for subtree2 in result2.subtrees(filter=lambda t: t.label() == 'Chunk'):
         #print "hasil subtree 2:", subtree2
         HasilChunk22.append(subtree2)

     Chunk1.append(HasilChunk11)
     Chunk2.append(HasilChunk22)
     print Chunk1
     print "==================================================="
     HasilChunkFIX1.append(removeNoChunk(HasilChunk11))
     HasilChunkFIX2.append(removeNoChunk(HasilChunk22))
     print "Hasil chunk 1 fix nih = ",HasilChunkFIX1[k]
     print "Hasil chunk 2 fix nih = ", HasilChunkFIX2[k]

     tokenW1.append(tokenChunk((HasilChunkFIX1[k]).lower()))
     # print tokenW1
     tokenW2.append(tokenChunk((HasilChunkFIX2[k]).lower()))

     # removal tagnya
     for j in range(len(tokenW1[k])):
         tokenW1[k][j] = Removal(tokenW1[k][j])
         tokenW1[k][j] = Hapus_stopword(tokenW1[k][j])
         #print "token1 =",tokenW1[k][j]
     for j in range(len(tokenW2[k])):
         tokenW2[k][j] = Removal(tokenW2[k][j])
         tokenW2[k][j] = Hapus_stopword(tokenW2[k][j])


         # Hapus spasi token
     j = 0
     while j < len(tokenW1[k]):
         if tokenW1[k][j] == '':
             tokenW1[k].pop(j)
         else:
             j += 1

     j = 0
     while j < len(tokenW2[k]):
         if tokenW2[k][j] == '':
             tokenW2[k].pop(j)
         else:
             j += 1

     #print "w1= ",tokenW1
     print (" Hasil Proses tokenisasi : ")
     print (tokenW1[k])
     print (tokenW2[k])
i=0
akurasiTotal=[]
for i in range(0, 5):
    print "======================================================================================"
    print tokenW1Chunk[i]
    print tokenW1[i]
    pnjng= len(tokenW1Chunk[i])+len(tokenW1[i])
    print "pnjng",pnjng
    benar = 0
    salah = 0
    tn = 0
    jml = 0
    for v in range(0,len(tokenW1Chunk[i])):
        for f in range(0,len(tokenW1[i])):
            if (tokenW1Chunk[i][v] == tokenW1[i][f]):
                print 1, tokenW1Chunk[i][v], "=", tokenW1[i][f]
                benar+=2
                jml += 1
                #print tokenW1Chunk[i][f]

            else:
                print 0,tokenW1Chunk[i][v],"!=", tokenW1[i][f]
                salah+=1
                jml += 1
            #print "aa", float(benar / pnjng), "benr1=", benar, "pnjng=", pnjng
    akurasiperChunk = 0
    print "pnjng=", pnjng
    print "benar=", benar
    #print "salah=", salah
    #print "jml=", jml
    akurasiperChunk = float(benar) / (pnjng)
    print akurasiperChunk
    akurasiTotal.append(akurasiperChunk)
print "==================================================================================="
print "AKURASI CHUNK KESELURUHAN"

akurasi=0
#print "jml=",jml
length=0
length=len(akurasiTotal)
#print length,akurasiTotal
jmlah=0
for i in range(0,len(akurasiTotal)):

    jmlah+=akurasiTotal[i]

#print jmlah
print float(jmlah)/(length)

#print evaluasiChunk(tokenW1Chunk,tokenW1Chunk,tokenW1,tokenW2)
#print Kata_Identik(tokenW1[k][0],tokenW1Chunk[a][0])
print ("------%s seconds----" %(time.time()-start_time))









