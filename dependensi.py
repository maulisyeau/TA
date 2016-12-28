import os

from nltk.parse import stanford
import re

# os.environ['STANDFORD_PARSER']='D:/BESTLUCK/bismillahTA/stanford-parser-full-2016-10-31'
# os.environ['STANDFORD_MODELS']='D:/BESTLUCK/bismillahTA/stanford-parser-full-2016-10-31'

parser = stanford.StanfordParser(
    model_path="D:/BESTLUCK/bismillahTA/stanford-parser-full-2016-10-31/englishPCFG.ser.gz",
    path_to_jar="D:/BESTLUCK/bismillahTA/stanford-parser-full-2016-10-31/stanford-parser.jar",
    path_to_models_jar="D:/BESTLUCK/bismillahTA/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar")

DataInputAyat1 = open('dataTA/data/fix/ayat1tanpachunk.txt','r')
BacaInputanAyat1 = DataInputAyat1.read()
DataInputanAyat1 = []
for line in BacaInputanAyat1.split('\n'):
    DataInputanAyat1.append(line)
print DataInputanAyat1
def OutputData(text):
    try :
        tmp = [str(parse) for parse in parser.raw_parse(text.lower())][0].split("\n")
    except :
        text = text.decode("UTF-8")
        tmp = [str(parse) for parse in parser.raw_parse(text.lower())][0].split("\n")

    arr = []
    for line in tmp:
        if re.sub(r'[^a-z]', '', line) != "":
            tmp1 = re.sub(r'[^a-z- ]', '', line)
            tmp1 = re.sub(r'[ ]{5,}', '', tmp1)
            tmp1 = re.sub(r'[ ]{2,4}', ' ', tmp1)
            arr.append(tmp1)


    tmp = ""
    for line in arr:
        tmp += "[ " + line + " ] "
    return tmp

dataOutput=[]

for line in DataInputanAyat1 :
    print OutputData(line)
    dataOutput.append(OutputData(line))

f = open("dataTA/data/fix/simpandata.txt", "w")
for data in dataOutput :
     f.writelines(data+" \n")
f.close()



def ChunkSama(kata1, kata2):
    nilai=0
    kata2 = kata2.split(" ] [ ")

    kata2[0] = kata2[0][2:]
    kata2[-1] = kata2[-1][:-3]

    i = 0
    tmp = []
    for a in kata1.split(" ] [ "):
        tmp.append(a);

    tmp[0] = tmp[0][2:]
    tmp[-1] = tmp[-1][:-2]


    if len(kata2) > len(tmp):
        maxLoop = len(tmp)
    else :
        maxLoop = len(kata2)

    for j in range(0,maxLoop):
        # if (tmp[j].lower() == kata2[j].lower()):
        if j == 11:
            print kata2[-1], ' test'
            print tmp[j], ' test'
        if tmp[j].lower() in kata2:
            print j, tmp[j]
            nilai +=1

    #
    # for a in kata1.split(" ] [ "):
    if (a.lower() == kata2[i].lower()):
        return 1
        nilai +=1
    #     i+=1
    else:
        return 0


def noTanda(token):
    token = re.sub(r'[\[\]\n]', '', token)
    return token


def evaluasi_chunking():
    panjangManual=0
    panjang= 0
    evalAyat1 = open('dataTA/data/fix/ayat1.txt') #ayat yang udah di chunk manual
    BacaevalAyat1 = evalAyat1.read()

    tmp1=[]
    BacaevalAyat1 = BacaevalAyat1.split("\r\n")[0:2]
    for b in BacaevalAyat1:
        tmp1.append(b.split(" ] [ "))
    tmp = []
    for b in tmp1:
        b[0] = b[0][2:]
        b[-1] = b[-1][:-3]
        tmp.append(b)

    tmp1 = tmp
    #print len(dataOutput),"aa"
    tmp = []
    print dataOutput,"outpu"
    for i in range(0,len(dataOutput)):
        for a in dataOutput[i].split(" ] [ "):
            tmp.append(a);


        tmp[0] = tmp[0][1:]
        tmp[-1] = tmp[-1][:-2]
    i += 1
    #print 'tmp1', tmp1,len(tmp1)
    print 'otomatis', len(tmp)


    for k in range(0,len(tmp1)):
        panjangManual+=len(tmp1[k])
        k+=1
        #print "pnj",panjangManual
    print "manual",panjangManual

    panjang= panjangManual+len(tmp)
    print panjang
    print "aaa",tmp[0]
    print "uuu",tmp1[0]
    benar=0
    # if ChunkSama(tmp[i],tmp1[0][i]) == 1 :
    #     benar += 2
    #     print benar,"ini benar"
    #     i +=1
    # #
    # # hasil = float(benar)/float(jumlahKata)
    return tmp

#print evaluasi_chunking()

