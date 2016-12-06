__author__ = 'maulisye'

import difflib
def Skor(tokenW1,tokenW2):
    # tokenW1=[]
    # tokenW2=[]
    seq= difflib.SequenceMatcher(tokenW1,tokenW2)
    d= seq.ratio()*5
    return d

#------------------------------------------------------------------------------------------------#
#Monoligual alignment

def PerhitunganIdentik(aligned_word1, aligned_word2,W1, W2,s_identic,content_word,num_lines):
    for y in range(0,num_lines):
        value_align_word = len(aligned_word1[y])+len(aligned_word2[y])
        value_content_word = len(W1[y])+len(W2[y])
        content_word.append(value_content_word)
        similarity_score =(((value_align_word)/(content_word[y]))*5)
        s_identic.append(str(similarity_score)+'\n')

def PerhitunganPPDB(aligned_word1, aligned_word2,W1, W2,s_identic,content_word,num_lines):
    for y in range(0,num_lines):
        value_align_word = 0.81*(len(aligned_word1[y])+len(aligned_word2[y]))
        value_content_word = len(W1[y])+len(W2[y])
        content_word.append(value_content_word)
        if value_align_word==0 :
            similarity_score =0
        else:
            similarity_score =(((value_align_word)/(content_word[y]))*5)
        s_identic.append(str(similarity_score)+'\n')

def PerhitunganNE(aligned_word1, aligned_word2,W1, W2,s_identic,content_word,num_lines):
    for y in range(0,num_lines):
        value_align_word = 0.81*len(aligned_word1[y])+len(aligned_word2[y])
        value_content_word = len(W1[y])+len(W2[y])
        content_word.append(value_content_word)
        if value_align_word==0 :
            similarity_score =0
        else:
            similarity_score =(((value_align_word+0.000000001)/(content_word[y]+0.000000001))*5)
        s_identic.append(str(similarity_score)+'\n')

def PerhitunganSequence(sequencelist,numlines,W1,W2,sim):
    for y in range(numlines):
        sum = 0
        if (len(sequencelist[y])== 0):
            sim.append(str(0)+'\n')
        else:
            for a in range(len(sequencelist[y])):
               sum = sum + len(sequencelist[y][a])
            content_word = len(W1[y])+len(W2[y])
            skor = 5*2*sum / content_word
            sim.append(str(skor)+'\n')




#------------------------------------------------------------------------------------------------#
#-------------------------Metode proportions of aligned content words----------------------------#

def propS1(aligned2,words1):
    prop1 = len(aligned2) / len(words1)

    return prop1

def propS2(aligned1,words2):
    prop2 = len(aligned1) / len(words2)
    return prop2

def propS1pfa(aligned2,words1):
    prop1 = (0.81*(len(aligned2))) / len(words1)

    return prop1

def propS2pfa(aligned1,words2):
    prop2 = (0.81*(len(aligned1))) / len(words2)
    return prop2

def sim_prop_identic(aligned1,aligned2,W1,W2,skor,numlines):
    for y in range(numlines):
        if ((propS1(aligned2[y],W1[y])and propS2(aligned1[y],W2[y])) == 0):
            sim = 0
        else:
            sim = 5*((2*(propS1(aligned2[y],W1[y])*propS2(aligned1[y],W2[y]))) / (propS1(aligned2[y],W1[y])+propS2(aligned1[y],W2[y])))
        skor.append(str(sim)+'\n')

def sim_prop_pfa(aligned1,aligned2,W1,W2,skor,numlines):
    for y in range(numlines):
        if ((propS1pfa(aligned2[y],W1[y])or propS2pfa(aligned1[y],W2[y])) == 0):
            sim = 0
        else:
            sim = 5*((2*(propS1pfa(aligned2[y],W1[y])*propS2pfa(aligned1[y],W2[y]))) / (propS1pfa(aligned2[y],W1[y])+propS2pfa(aligned1[y],W2[y])))
        skor.append(str(sim)+'\n')

def seq_prop(sequencelist,numlines,W1,W2,sim):
    for y in range(numlines):
        sum = 1
        if (len(sequencelist[y])== 0):
            sim.append(str(0)+'\n')
        else:
            for a in range(len(sequencelist[y])):
                sum = sum + len(sequencelist[y][a])
            prop1 = sum / len(W2)
            prop2 = sum / len(W1)
            skor = 5*(2*(prop1*prop2)/(prop1+prop2+1))
            sim.append(str(skor)+'\n')

