__author__ = 'maulisye'
import os
from preproses import *
from alignerTAAutoChunk import *
from HitungKesamaan_TA import *
import time
import  nltk
from nltk import FreqDist

start_time=time.time()
#headlinesC ='dataTA/data/gabungan.txt' #alquran
#headlinesC ='dataTA/gabung.txt' # headline chunk
#headlinesC ='dataTA/data/fix/ibnukatsir.txt'
headlinesC ='dataTA/data/fix/IndeksTematik.txt'
# membaca inputan Data chunk
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

#PREPROSES#

#tag
for i in range(0,jml_line):
    couple.append(baca[i].split('\t'))
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


k=0

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

Chunk:{<DT>?<JJ>*<NN>}
Chunk:{<DT>?<JJ>*<NNS>}
Chunk:{<CC>}
Chunk:{<WRB>}
Chunk:{<NN>*}
Chunk:{<IN>}
Chunk:{<RB>}
Chunk:{<NNS>}
Chunk:{<V.*>}
Chunk:{<TO>}
Chunk:{<JJ>?<JJ>?<JJ>?<NN>}
Chunk:{<JJ>*}
Chunk:{<WP>*}
Chunk:{<WDT>*}
Chunk:{<MD>*}
Chunk:{<PRP>*}
Chunk:{<JJS>*}
Chunk:{<P>*<NP>}
Chunk:{<NP>?<CC>*<NP>}
Chunk:{<PP>*<NP>}
Chunk:{<VP>*<PRT>}
Chunk:{<V> <NP|PP>*}
Chunk:{<PP>*<NP>}
Chunk:{<PRP>*<VP>*<PRT>}
Chunk:{<DT>?<IN>?<JJ>*<NN>?<NNS>}
"""
cp = nltk.RegexpParser(grammar)
result1 = cp.parse(sentence1)
result2 = cp.parse(sentence2)

r1.append(result1)
r2.append(result2)


     #print (" Pasangan ayat Al-quran yang sudah di chunk :")
     #nampilin parsernya
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
# print "-------------------------------------------"
# print "chunk 1 ya", Chunk1[k]
# print "chunk 2 ya", Chunk2[k]
jmlc1=len(Chunk1[k])
jmlc2 = len(Chunk2[k])
jmlk1=len(set(FreqDist(text1)))
jmlk2 = len(set(FreqDist(text2)))
#print "Jumlah chunk di potongan ayat 1=",jmlc1,"jumlah kata di potongan ayat 1 =",jmlk1 ,"rata-rata =",float (jmlc1)/(jmlk1)
#print "Jumlah chunk di potongan ayat 2=", jmlc2, "jumlah kata di potongan ayat 1 =", jmlk2, "rata-rata =", float (jmlc2)/(jmlk2)
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

     # #print "w1= ",tokenW1
print (" Hasil Proses tokenisasi : ")
print (tokenW1[k])
print (tokenW2[k])
     # print len(tokenW1[k])
     # Lemmatization
     #for k in range(0,10):
for tes1 in range(len(tokenW1[k])):
    #t = unicode(tokenW1[y][tes1], errors='replace')
    tokenW1[k][tes1] = lematisasi(tokenW1[k][tes1])
for tes2 in range(len(tokenW2[k])):
     #ts2 = unicode(tokenW2[y][tes2], errors='replace')
     tokenW2[k][tes2] = lematisasi(tokenW2[k][tes2])
     #print tokenW2[k][tes2],"uuuaa"
     #
     #
print "========================================="
print (" Hasil Proses  Stemming dan lemmatisasi :")
print tokenW1[k]
print tokenW2[k]
def Kata_Identik(word1,word2):
    if word1 ==word2:
        return 1
    else:
        return 0
align_identic=0
for i in range(0, len(tokenW1[k])):
    for j in range(0, len(tokenW2[k])):
        align_identic = align_identic + Kata_Identik((tokenW1[k][i]).lower(), (tokenW2[k][j]).lower())
    if align_identic >= 1:
        word1.append(tokenW1[k][i])
        align_identic = 0
align1.append(word1)
print align1
word1 = []
align_identic1=0
for x in range(0, len(tokenW2[k])):
    for z in range(0, len(tokenW1[k])):
        align_identic1 = align_identic1 + Kata_Identik((tokenW2[k][x]).lower(), (tokenW2[k][z]).lower())
    if align_identic1>= 1:
        word2.append(tokenW2[k][x])
    align_identic = 0
align2.append(word2)
print align2
word2 = []

print "============================"
print "=====Identical Alignment==== :"
#print align1[k]
#print align2[k]

#print align1[1]





print ("---%s seconds---"% (time.time()-start_time))