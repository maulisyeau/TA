__author__ = 'maulisye'
from preproses import *
from alignerTA import *
import sys
import time
#reload(sys)
#sys.setdefaultencoding('utf8')
import  nltk
from nltk import FreqDist
start_time=time.time()
headlineC ='dataTA/gabung.txt' #udah di chunk yang headline
headlinesC ='dataTA/data/gabungan.txt' #Coba aja dulu hehehe
#headline ='dataTA/STSint.testinput.headlines.sent2.txt'

#Data Chunk
dataChunk=open((headlineC.lower()))
bacaChunk=dataChunk.readlines()
coupleChunk = [] #menyimpan pasangan ayat dalam indeks terpisah
tokenW1Chunk =[]
tokenW2Chunk =[]
jml_lineChunk = sum(1 for line in open(headlineC))
#tag
for i in range(0,jml_lineChunk):
    coupleChunk.append(bacaChunk[i].split('\t'))

    tokenW1Chunk.append(tokenWord((coupleChunk[i][0]).lower()))
   # print tokenW1
    tokenW2Chunk.append(tokenWord((coupleChunk[i][1]).lower()))
  #  print tokenW2


    #removal tagnya
    for j in range(len(tokenW1Chunk[i])):
        tokenW1Chunk[i][j]=Removal(tokenW1Chunk[i][j])
        tokenW1Chunk[i][j]=Hapus_stopword(tokenW1Chunk[i][j])
    for j in range(len(tokenW2Chunk[i])):
        tokenW2Chunk[i][j]=Removal(tokenW2Chunk[i][j])
        tokenW2Chunk[i][j]=Hapus_stopword(tokenW2Chunk[i][j])



#Hapus spasi token
    j=0
    while j < len(tokenW1Chunk[i]) :
        if tokenW1Chunk[i][j]=='':
            tokenW1Chunk[i].pop(j)
        else:
            j +=1

    j = 0
    while j < len(tokenW2Chunk[i]):
        if tokenW2Chunk[i][j] == '':
            tokenW2Chunk[i].pop(j)
        else:
            j += 1



# membaca inputan Data  Bukan chunk
data = open((headlinesC).lower())
baca = data.readlines()

#hitung jumlah baris data
jml_line = sum(1 for line in open(headlinesC))
print  "Jumlah baris :",jml_line

i= 0

couple = [] #menyimpan pasangan ayat dalam indeks terpisah
tokenW1 =[]
tokenW2 =[]
potonganP1 =[]
potonganP2 =[]

k=0
Chunk1=[]
Chunk2=[]
HasilChunkFIX1=[]
HasilChunkFIX2=[]
#PREPROSES#

#tag bukan chunk
for i in range(0,jml_line):
    couple.append(baca[i].split('\t'))

    tokenW1.append(tokenWord((couple[i][0]).lower()))
   # print tokenW1
    tokenW2.append(tokenWord((couple[i][1]).lower()))
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

loadPPDB(ppdbNamaFile='dataTA/penting/ppdb-2.0-xxxl-lexical')
#loadPPDB(ppdbNamaFile='dataTA/penting/ppdb-1.0-xxxl-lexical.extended.synonyms.uniquepairs')
align_ppdb (jml_line,aligned_word1PPDB,aligned_word2PPDB,tokenW1,tokenW2)

for k in range(0,jml_line):
     print ("==========================================================================================================================")
     print ("==========================================================================================================================")
     print ("Pasangan ayat Al-qur'an Ke- ",k+1)
     print "ayat 1 = " ,couple[k][0]
     print "ayat 2 = ",couple[k][1]
     r1 = []
     r2 = []
     text1 = nltk.word_tokenize(Hapus_stopword((couple[k][0]).lower()))
     text2 = nltk.word_tokenize(Hapus_stopword((couple[k][1]).lower()))
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


     print (" Pasangan ayat Al-quran yang sudah di chunk :")
     #nampilin parsernya
     print "result1",result1
     print "result2",result2
     jml=0
     HasilChunk11=[]
     HasilChunk22=[]
     for subtree1 in result1.subtrees(filter=lambda t: t.label() == 'Chunk'):
         print "hasil subtree 1:", subtree1
         HasilChunk11.append(subtree1)

     for subtree2 in result2.subtrees(filter=lambda t: t.label() == 'Chunk'):
         print "hasil subtree 2:", subtree2
         HasilChunk22.append(subtree2)

     Chunk1.append(HasilChunk11)
     Chunk2.append(HasilChunk22)
     print "-------------------------------------------"
     print "chunk 1 ya", Chunk1[k]
     print "chunk 2 ya", Chunk2[k]
     jmlc1=len(Chunk1[k])
     jmlc2 = len(Chunk2[k])
     jmlk1=len(set(FreqDist(text1)))
     jmlk2 = len(set(FreqDist(text2)))
     print "Jumlah chunk di potongan ayat 1=",jmlc1,"jumlah kata di potongan ayat 1 =",jmlk1 ,"rata-rata =",float (jmlc1)/(jmlk1)
     print "Jumlah chunk di potongan ayat 2=", jmlc2, "jumlah kata di potongan ayat 1 =", jmlk2, "rata-rata =", float (jmlc2)/(jmlk2)
     print "==================================================="
     #print "removal:",removeNoChunk(HasilChunk11)
     #print "removal:",removeNoChunk(HasilChunk22)
     HasilChunkFIX1.append(removeNoChunk(HasilChunk11))
     HasilChunkFIX2.append(removeNoChunk(HasilChunk22))
     print "Hasil chunk 1 fix nih = ",HasilChunkFIX1[k]
     print "Hasil chunk 2 fix nih = ", HasilChunkFIX2[k]
     print (" Hasil Proses tokenisasi : ")
     print (tokenW1[k])
     print (tokenW2[k])

     # Lemmatization
     for y in range(0, jml_line):
         for tes1 in range(len(tokenW1[y])):
             #t = unicode(tokenW1[y][tes1], errors='replace')
             tokenW1[y][tes1] = lematisasi(tokenW1[y][tes1])
             # print t
             # print  tokenW1[y][tes1]

         for tes2 in range(len(tokenW2[y])):
             #ts2 = unicode(tokenW2[y][tes2], errors='replace')
             tokenW2[y][tes2] = lematisasi(tokenW2[y][tes2])
             # print t
             # tokenW2[y][tes2]=lematisasi((tokenW2[y][tes2]).lower())
             # print  tokenW2[y][tes2]

     print "========================================="
     print (" Hasil Proses  Stemming dan lemmatisasi :")
     print tokenW1[k]
     print tokenW2[k]


     a = open('hasil/identik.txt', 'w')
     alignIdenticalWord(jml_line, align1, align2, tokenW1, tokenW2)

     print "============================"
     print "=====Identical Alignment==== :"
     print align1[k]
     print align2[k]

     #

     # f.writelines(s_identic)
     # f.close()
     # g.writelines(sim_identic)
     # g.close()

     # Alignment dengan ppdb /pharaprase


     print "================================="
     print "======Alignment dengan PPDB======"
     print aligned_word1PPDB[4]
     print aligned_word2PPDB[4]

     k +=1




# for hsl in HasilChunk1:
#     print "Sementara 1",str(hsl)+"\n"



# NE

aligned_word1NE=[]
aligned_word2NE=[]
hasilNE=[]

LoadNE(neNamaFile='dataTA/penting/ne.txt')
align_NE(jml_line,aligned_word1NE,aligned_word2NE,tokenW1,tokenW2)
print "=============================="
print "========Named entity=========="
print aligned_word1NE[4]
print aligned_word2NE[4]


print ("---%s seconds---"% (time.time()-start_time))