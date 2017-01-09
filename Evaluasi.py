import re
__author__ = 'maulisye'

import time
start_time=time.time()

GStematik1 =  open("dataTA/data/fix/GS1tematik.chunk.txt","r")
bacagstm1= GStematik1.read()
bacagstm1=bacagstm1.split('\n')

GStematik2 =  open("dataTA/data/fix/GS2tematik.chunk.txt","r")
bacagstm2= GStematik2.read()
bacagstm2=bacagstm2.split('\n')

GSqursim1 =  open("dataTA/data/fix/GS1qursim.chunk.txt","r")
bacagsq1= GSqursim1.read()
bacagsq1=bacagsq1.split('\n')

GSqursim2 =  open("dataTA/data/fix/GS1qursim.chunk.txt","r")
bacagsq2= GSqursim2.read()
bacagsq2=bacagsq2.split('\n')

tematik1 =  open("dataTA/data/fix/simpandata1tematik.chunk.txt","r")
bacatm1= tematik1.read()
bacatm1=bacatm1.split('\n')


tematik2 =  open("dataTA/data/fix/simpandata1tematik.chunk.txt","r")
bacatm2= tematik2.read()
bacatm2=bacatm2.split('\n')

qursim1 =  open("dataTA/data/fix/simpandata1qursim.chunk.txt","r")
bacaq1= qursim1.read()
bacaq1=bacaq1.split('\n')

qursim2 =  open("dataTA/data/fix/simpandata2qursim.chunk.txt","r")
bacaq2= qursim2.read()
bacaq2=bacaq2.split('\n')

gstm1=[]
hasiltm1=[]
gstm2=[]
hasiltm2=[]
gsq1=[]
hasilq1=[]
gsq2=[]
hasilq2=[]
#buat tematik 1
for line in bacagstm1 :
    line=line.split(' ] [ ')
    tmp = []
    for line2 in line:
        tmp.append(re.sub(r'[^a-z]+','',line2.lower()))
    gstm1.append(tmp)

for line in bacatm1:
    line = line.split(' ] [ ')
    tmp = []
    for line2 in line:
        tmp.append(re.sub(r'[^a-z]+', '', line2.lower()))
    hasiltm1.append(tmp)

#buat tematik 2
for line in bacagstm2 :
    line=line.split(' ] [ ')
    tmp = []
    for line2 in line:
        tmp.append(re.sub(r'[^a-z]+','',line2.lower()))
    gstm2.append(tmp)

for line in bacatm2:
    line = line.split(' ] [ ')
    tmp = []
    for line2 in line:
        tmp.append(re.sub(r'[^a-z]+', '', line2.lower()))
    hasiltm2.append(tmp)

#buat qursim 1
for line in bacagsq1 :
    line=line.split(' ] [ ')
    tmp = []
    for line2 in line:
        tmp.append(re.sub(r'[^a-z]+','',line2.lower()))
    gsq1.append(tmp)

for line in bacaq1:
    line = line.split(' ] [ ')
    tmp = []
    for line2 in line:
        tmp.append(re.sub(r'[^a-z]+', '', line2.lower()))
    hasilq1.append(tmp)


#buat qursim 2
for line in bacagsq2 :
    line=line.split(' ] [ ')
    tmp = []
    for line2 in line:
        tmp.append(re.sub(r'[^a-z]+','',line2.lower()))
    gsq2.append(tmp)

for line in bacaq1:
    line = line.split(' ] [ ')
    tmp = []
    for line2 in line:
        tmp.append(re.sub(r'[^a-z]+', '', line2.lower()))
    hasilq2.append(tmp)

def sim(arr1, arr2) :
    hasil = 0.0
    for i in range(len(arr1)) :
        n = 0
        for line in arr2[i] :
            if line in arr1[i] :
                n+=1
        hasil += n/len(arr1[i])
    return hasil/len(arr1)

print sim(gstm1,hasiltm1)
print sim(gstm2,hasiltm2)
print sim(gsq1,hasilq1)
print sim(gsq2,hasilq2)


print ("------%s seconds----" %(time.time()-start_time))









