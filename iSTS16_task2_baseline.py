#!/usr/bin/python
from nltk.corpus import wordnet as wn
import re
import os
from munkres import Munkres, print_matrix
import sys
import munkres
from nltk.corpus import wordnet as wn


def readFile(filename):
    return [line.strip().decode("utf-8") for line in open(filename)]

def readFileWithChunks(filename):
    lines_marked = [line.strip().decode("utf-8") for line in open(filename)]
    lines_clean1 = [line.replace('[ ', "") for line in lines_marked]
    lines_clean2 = [line.replace(' ]', "") for line in lines_clean1]
    return lines_clean2

def removeNoise(line):
    line = line.replace('[', "")
    line = line.replace(']', "")
    line = line.replace(',', "")
    line = line.replace('.', "")
    line = line.replace(':', "")
    line = line.replace(';', "")
    line = line.replace('"', "")
    line = line.replace("'", "")
    line = line.replace("''", "")
    line = line.replace("`", "")
    line = line.replace("-", "")
    return line

def isNoise(token):
    if token == "[" or token == "]" or token == "," or token == "." or token == ";" or token == ":" or token == "'" or token == '"' or token == "''" or token == " " or token == "" or token == "`" or token == "-":
        return True
    else:
        return False

def findTokensForChunk(sentenceChunks, sentenceTokens):
    tokensChunk = []
    token_index = 0

    for chunk_index in range(len(sentenceChunks)):
		#merubah dari kalimat ke token-token chunk
        chunk = sentenceChunks[chunk_index]
        chunk = removeNoise(chunk)
        chunk_words = chunk.split()

        for chunk_word in chunk_words:
            if token_index > len(sentenceTokens):
                return tokensChunk

            token = removeNoise(sentenceTokens[token_index][1])
            token_lemma = removeNoise(sentenceTokens[token_index][2])

            while isNoise(token):
                token_index += 1
                token = removeNoise(sentenceTokens[token_index][1])
                token_lemma = removeNoise(sentenceTokens[token_index][2])

            while isNoise(chunk_word):
                continue

            if chunk_word == token or chunk_word == token_lemma:
                triplet = [token_index + 1, token, chunk_index + 1]
                tokensChunk.append(triplet)
                token_index += 1
            else:
                triplet1 = [token_index + 1, token, chunk_index + 1]
                triplet2 = [token_index + 2, removeNoise(sentenceTokens[token_index + 1][1]), chunk_index + 1]

                tokensChunk.append(triplet1)
                tokensChunk.append(triplet2)

                token_index += 2
    return tokensChunk
#mengilangkan tanda siku
def extractChunksFromSentence(sentence):
    chunks = re.findall(r"\[[^\[]+\]", sentence)
    return chunks

def extractChunksFromIxaPipes(sentenceTokens):
    sentence_tok_list = []
    for triplet in sentenceTokens:
        sentence_tok_list.append(triplet[2])
    sentence_tok = " ".join(sentence_tok_list)

    f = open("temp_sent.tmp", "w")
    f.write(sentence_tok.encode("utf-8"))
    f.close()
    os.system("sleep 0.15")

    CAT = "cat temp_sent.tmp | "
    JAVA_BIN = "java -jar "
    IXA_PIPES_TOK = JAVA_BIN + "ixa-pipes/ixa-pipe-tok-1.5.3.jar  tok -l en --notok | "
    IXA_PIPES_POS = JAVA_BIN + "ixa-pipes/ixa-pipe-pos-1.2.0.jar tag | "
    IXA_PIPES_CHUNK = JAVA_BIN + "ixa-pipes/ixa-pipe-chunk-1.0.jar --nokaf -o pretty > temp.tmp"
    COMMAND = CAT + IXA_PIPES_TOK + IXA_PIPES_POS + IXA_PIPES_CHUNK
    os.system(COMMAND)
    os.system("sleep 0.15")

    [line.strip().decode("utf-8") for line in open("temp.tmp")]

    chunks = extractChunksFromSentence(line)

    clean_chunks = []
    for chunk in chunks:
        new_chunk = " ".join(re.findall(r" [^_]+_", chunk)).replace("_", "")
        clean_chunks.append("[ " + new_chunk + " ]")
	
    return [x.decode("utf-8") for x in clean_chunks]

#hasil sentence 1 yang sudah ditoken chunk
def createToken2tokenLinkMatrix(sentence1TokensChunk, sentence2TokensChunk, idAlignments):
    epsilon = 1E-20

    Matrix = [[epsilon for x in xrange(len(sentence2TokensChunk))] for x in xrange(len(sentence1TokensChunk))]

    for alignment in idAlignments:
        if mustAlignTokens(sentence1TokensChunk, sentence2TokensChunk, alignment):
            S1token = alignment[0]
            S2token = alignment[1]
            S1TokenIdVariation = getTokenVariation(S1token, sentence1TokensChunk)
            S2TokenIdVariation = getTokenVariation(S2token, sentence2TokensChunk)
            Matrix[S1token - 1 - S1TokenIdVariation][S2token - 1 - S2TokenIdVariation] += 1
    return Matrix

def getTokenVariation(token_focus, sentenceTokensChunk):
    notAlignables = 0

    for token_id in xrange(1, token_focus):
        if not isTokenAlignable(token_id, sentenceTokensChunk):
            notAlignables += 1
    return notAlignables

def getNotAlignableTokenIds(sentenceTokens, sentenceTokensChunk):
    NotAlignable = []
    missingChunks = getMissingChunks(sentenceTokensChunk)
    index = 0
    for triplet in sentenceTokens:
        if index >= len(missingChunks):
            break

        if (not isTokenAlignable(triplet[0], sentenceTokensChunk)) and ( not isTokenInChunk(triplet[0], sentenceTokensChunk)):
            NotAlignable.append([triplet[0], triplet[1], missingChunks[index]])
            index += 1

    return NotAlignable

def isTokenInChunk(tokenId, sentenceTokensChunk):
    for triplet in sentenceTokensChunk:
        if tokenId == triplet[0]:
            return True
    return False

def getMissingChunks(sentenceTokensChunk):
    missingChunks = []

    for i in xrange(1, getNumberChunks(sentenceTokensChunk)):
        if chunkIdNotPresent(i, sentenceTokensChunk):
            missingChunks.append(i)
    return missingChunks

def chunkIdNotPresent(chunkFocus, sentenceTokensChunk):
    for triplet in sentenceTokensChunk:
        if triplet[2] == chunkFocus:
            return False
    return True

def isTokenAlignable(token_id, sentenceTokensChunk):
    for triplet in sentenceTokensChunk:
        if int(triplet[0]) == int(token_id):
            return True
    return False

def mustAlignTokens(sentence1TokensChunk, sentence2TokensChunk, alignment):
    AlignS1token = False
    S1token = alignment[0]

    AlignS2token = False
    S2token = alignment[1]

    for triplet in sentence1TokensChunk:
        if S1token == triplet[0]:
            AlignS1token = True
            break

    for triplet in sentence2TokensChunk:
        if S2token == triplet[0]:
            AlignS2token = True
            break

    return (AlignS1token and AlignS2token)

def getChunkVariation(chunk_focus, sentenceTokensChunk):
    chunkVariation = 0
    for index in xrange(1, chunk_focus):
        if not isChunkAlignable(index, sentenceTokensChunk):
            chunkVariation += 1
    return chunkVariation

def isChunkAlignable(chunk_index, sentenceTokensChunk):
    for chunk_triplet in sentenceTokensChunk:
        if chunk_triplet[2] == chunk_index:
            if isTokenAlignable(chunk_triplet[0], sentenceTokensChunk):
                return True
        if chunk_triplet[2] > chunk_index:
            break
    return False

def createChunk2chunkLinkMatrix(sentence1TokensChunk, sentence2TokensChunk, token2tokenLinkMatrix):
    epsilon = 1E-20
    S1ChunkNumber = getNumberChunks(sentence1TokensChunk)
    S2ChunkNumber = getNumberChunks(sentence2TokensChunk)
    S1ChunkNumber -= getChunkVariation(S1ChunkNumber, sentence1TokensChunk)
    S2ChunkNumber -= getChunkVariation(S2ChunkNumber, sentence2TokensChunk)

    Matrix = [[epsilon for x in xrange(S2ChunkNumber)] for x in xrange(S1ChunkNumber)]

    S1chunkRegions = getChunkRegions(sentence1TokensChunk)
    S2chunkRegions = getChunkRegions(sentence2TokensChunk)

    for S1ChunkIndex in xrange(S1ChunkNumber):
        for S2ChunkIndex in xrange(S2ChunkNumber):
            regionSum = sumRegion(S1chunkRegions[S1ChunkIndex], S2chunkRegions[S2ChunkIndex], token2tokenLinkMatrix, sentence1TokensChunk, sentence2TokensChunk)
            Matrix[S1ChunkIndex][S2ChunkIndex] += regionSum
    return Matrix

def sumRegion(S1chunkRegion, S2chunkRegion, token2tokenLinkMatrix, sentence1TokensChunk, sentence2TokensChunk):
    i_start = S1chunkRegion[0]
    i_end = S1chunkRegion[1]
    i_start -= getTokenVariation(i_start, sentence1TokensChunk)
    i_start -= 1
    i_end -= getTokenVariation(i_end, sentence1TokensChunk)

    j_start = S2chunkRegion[0]
    j_end = S2chunkRegion[1]
    j_start -= getTokenVariation(j_start, sentence2TokensChunk)
    j_start -= 1
    j_end -= getTokenVariation(j_end, sentence2TokensChunk)

    cumSum = 0

    for i in xrange(i_start, i_end):
        for j in xrange(j_start, j_end):
            cumSum += token2tokenLinkMatrix[i][j]
    return int(cumSum)

def getChunkRegions(sentenceTokensChunk):
    range_pairs = []

    for index in xrange(getNumberChunks(sentenceTokensChunk)):
        chunk_index = index + 1
        tokens = []
        range_pair = []
        for triplet in sentenceTokensChunk:
            if chunk_index == triplet[2]:
                tokens.append(triplet[0])
        if not tokens:
            continue
        range_pair = [min(tokens), max(tokens)]
        range_pairs.append(range_pair)
    return range_pairs

def getNumberChunks(SentenceTokensChunk):
    return SentenceTokensChunk[len(SentenceTokensChunk) - 1][2]

def getAlignableChunksInSentence(sentenceTokensChunk):
    alignableChunks = []
    numberChunksSentence = getNumberChunks(sentenceTokensChunk)
    for i in xrange(1, numberChunksSentence + 1):
        if isChunkAlignable(i, sentenceTokensChunk):
            alignableChunks.append(i)
    return alignableChunks

def getNotLinkedChunkIdsSentence1(chunk2chunkLinkMatrix, sentence1TokensChunk):
    chunkIdsWithNoLink = []
    chunkIndexNOALI = []
    numberRows = len(chunk2chunkLinkMatrix)

    for row_index in xrange(0, numberRows):
        if not chunkRowHasAnyLink(row_index, chunk2chunkLinkMatrix):
            chunkIndexNOALI.append(row_index)

    alignableChunks = getAlignableChunksInSentence(sentence1TokensChunk)

    for index in chunkIndexNOALI:
        realChunkIndex = alignableChunks[index]
        chunkIdsWithNoLink.append(realChunkIndex)
    return chunkIdsWithNoLink

def getNotLinkedChunkIdsSentence2(chunk2chunkLinkMatrix, sentence2TokensChunk):
    chunkIdsWithNoLink = []
    chunkIndexNOALI = []
    numberCols = len(chunk2chunkLinkMatrix[0])

    for col_index in xrange(0, numberCols):
        if not chunkColHasAnyLink(col_index, chunk2chunkLinkMatrix):
            chunkIndexNOALI.append(col_index)

    alignableChunks = getAlignableChunksInSentence(sentence2TokensChunk)

    for index in chunkIndexNOALI:
        realChunkIndex = alignableChunks[index]
        chunkIdsWithNoLink.append(realChunkIndex)
    return chunkIdsWithNoLink

def getLinkedChunkIdsSentence1(chunk2chunkLinkMatrix, sentence1TokensChunk):
    chunkIdsWithLink = []
    chunkIndexALI = []
    numberRows = len(chunk2chunkLinkMatrix)

    for row_index in xrange(0, numberRows):
        if chunkRowHasAnyLink(row_index, chunk2chunkLinkMatrix):
            chunkIndexALI.append(row_index)

    alignableChunks = getAlignableChunksInSentence(sentence1TokensChunk)

    for index in chunkIndexALI:
        realChunkIndex = alignableChunks[index]
        chunkIdsWithLink.append(realChunkIndex)
    return chunkIdsWithLink

def getLinkedChunkIdsSentence2(chunk2chunkLinkMatrix, sentence2TokensChunk):
    chunkIdsWithLink = []
    chunkIndexALI = []
    numberCols = len(chunk2chunkLinkMatrix[0])

    for col_index in xrange(0, numberCols):
        if chunkColHasAnyLink(col_index, chunk2chunkLinkMatrix):
            chunkIndexALI.append(col_index)

    alignableChunks = getAlignableChunksInSentence(sentence2TokensChunk)

    for index in chunkIndexALI:
        realChunkIndex = alignableChunks[index]
        chunkIdsWithLink.append(realChunkIndex)

    return chunkIdsWithLink

def chunkRowHasAnyLink(row_index, chunk2chunkLinkMatrix):
    for col_index in xrange(len(chunk2chunkLinkMatrix[0])):
        if chunk2chunkLinkMatrix[row_index][col_index] >= 1:
            return True
    return False

def chunkColHasAnyLink(col_index, chunk2chunkLinkMatrix):
    for row_index in xrange(len(chunk2chunkLinkMatrix)):
        if chunk2chunkLinkMatrix[row_index][col_index] >= 1:
            return True
    return False

def chunkIds2TokenIds(chunkIds, sentenceTokensChunk):
    allTokens = []

    for chunkId in chunkIds:
        for token in chunkId2TokenId(chunkId, sentenceTokensChunk):
            allTokens.append(token)

    return allTokens

def chunkId2TokenId(chunkId, sentenceTokensChunk):
    allTokens = []

    for triplet in sentenceTokensChunk:
        if triplet[2] == chunkId:
            allTokens.append(triplet)
    return allTokens

def getChunksForNotAlignableTokens(Sentence1_NotAlignable_tokens):
    ChunkIds = []

    for triplet in Sentence1_NotAlignable_tokens:
        ChunkIds.append(triplet[2])

    return ChunkIds

def createChunk2chunkReducedLinkMatrix(chunk2chunkLinkMatrix, Sentence1_Linked_chunks, sentence1TokensChunk, Sentence2_Linked_chunks, sentence2TokensChunk):
    sentence1AlignableChunks = getAlignableChunksInSentence(sentence1TokensChunk)
    sentence2AlignableChunks = getAlignableChunksInSentence(sentence2TokensChunk)
    epsilon = 1E-20
    numberRows = len(chunk2chunkLinkMatrix)
    numberCols = len(chunk2chunkLinkMatrix[0])
    reducedNumberRows = len(Sentence1_Linked_chunks)
    reducedNumberCols = len(Sentence2_Linked_chunks)
    i_reduced = 0
    j_reduced = 0

    Matrix = [[epsilon for x in xrange(reducedNumberCols)] for x in xrange(reducedNumberRows)]

    for i in xrange(numberRows):
        try:
            realChunkI = sentence1AlignableChunks[i]
        except IndexError:
            continue

        if not isChunkLinked(realChunkI, Sentence1_Linked_chunks):
            continue

        for j in xrange(numberCols):
            try:
                realChunkJ = sentence2AlignableChunks[j]
            except IndexError:
                continue

            if not isChunkLinked(realChunkJ, Sentence2_Linked_chunks):
                continue

            Matrix[i_reduced][j_reduced] += chunk2chunkLinkMatrix[i][j]
            j_reduced += 1
            if j_reduced >= reducedNumberCols:
                i_reduced += 1
                j_reduced = 0

    return Matrix

def isChunkNotLinked(chunk_index, Sentence_NotLinked_chunks):
    for chunkId in Sentence_NotLinked_chunks:
        if chunkId == chunk_index:
            return True
    return False

def isChunkLinked(chunk_index, Sentence1LinkedChunks):
    for ChunkId in Sentence1LinkedChunks:
        if ChunkId == chunk_index:
            return True
    return False

def cleanEpsilons(matrix):
    epsilon = 1E-20
    numberRows = len(matrix)

    if numberRows == 0:
        return []

    numberCols = len(matrix[0])
    if numberCols == 0:
        return []

    cleanMatrix = [[0 for x in xrange(numberCols)] for x in xrange(numberRows)]

    for i in xrange(numberRows):
        for j in xrange(numberCols):
            if matrix[i][j] >= 1:
                cleanMatrix[i][j] = matrix[i][j]
            else:
                cleanMatrix[i][j] = epsilon

    return cleanMatrix

def getMaximunRelatedChunkIds(bestIndexes, Sentence1_Linked_chunks, Sentence2_Linked_chunks):
    bestAlignedChunkIds = []
    print "--1--",bestIndexes
    for bestPair in bestIndexes:
        sentence1index = bestPair[0]
        sentence2index = bestPair[1]
        #print "--1--",bestPair[0]
        #print "--2--",bestPair[1]
        sentence1chunkId = Sentence1_Linked_chunks[sentence1index]
        sentence2chunkId = Sentence2_Linked_chunks[sentence2index]
        bestAlignedChunkIds.append([sentence1chunkId, sentence2chunkId])
    return bestAlignedChunkIds

def getOtherRelatedChunkIds(chunk2chunkReducedLinkMatrix, bestIndexes, Sentence1_Linked_chunks, Sentence2_Linked_chunks):
    bestAlignedChunkIds = []
    sentence1BestIndexes = [pair[0] for pair in bestIndexes]
    sentence2BestIndexes = [pair[1] for pair in bestIndexes]
    sentence1otherLinkIndexes = getOtherLinkIndexesSentence1(chunk2chunkReducedLinkMatrix, sentence1BestIndexes)
    sentence2otherLinkIndexes = getOtherLinkIndexesSentence2(chunk2chunkReducedLinkMatrix, sentence2BestIndexes)
    sentence1otherLinkChunkIds = [Sentence1_Linked_chunks[index] for index in sentence1otherLinkIndexes]
    sentence2otherLinkChunkIds = [Sentence2_Linked_chunks[index] for index in sentence2otherLinkIndexes]
    return [sentence1otherLinkChunkIds, sentence2otherLinkChunkIds]

def getOtherLinkIndexesSentence1(chunk2chunkReducedLinkMatrix, sentenceBestIndexes):
    numberRows = len(chunk2chunkReducedLinkMatrix)
    if numberRows == 0:
        return []

    numberCols = len(chunk2chunkReducedLinkMatrix[0])
    if numberCols == 0:
        return []

    OtherLinkIndexes = []

    for i in xrange(numberRows):
        if chunkRowHasAnyLink(i, chunk2chunkReducedLinkMatrix) and not indexIsBestMatch(i, sentenceBestIndexes):
            OtherLinkIndexes.append(i)

    return OtherLinkIndexes

def getOtherLinkIndexesSentence2(chunk2chunkReducedLinkMatrix, sentenceBestIndexes):
    numberRows = len(chunk2chunkReducedLinkMatrix)
    if numberRows == 0:
        return []

    numberCols = len(chunk2chunkReducedLinkMatrix[0])

    if numberCols == 0:
        return []

    OtherLinkIndexes = []

    for j in xrange(numberCols):
        if chunkColHasAnyLink(j, chunk2chunkReducedLinkMatrix) and not indexIsBestMatch(j, sentenceBestIndexes):
            OtherLinkIndexes.append(j)

    return OtherLinkIndexes

def indexIsBestMatch(chunkIndex, sentenceBestIndexes):
    for index in sentenceBestIndexes:
        if chunkIndex == index:
            return True
    return False

def addMissings(tokenTriplets, sentenceTokens):
    tokenIds = [triplet[0] for triplet in tokenTriplets]
    idStart = tokenIds[0]
    idEnd = tokenIds[-1]
    missings = sorted(set(range(idStart, idEnd + 1)).difference(tokenIds))
    chunkId = tokenTriplets[0][2]

    for missingTokenId in missings:

        newTriplet = [missingTokenId, sentenceTokens[missingTokenId - 1][1], chunkId ]
        insertPos = missingTokenId - idStart
        tokenTriplets.insert(insertPos,newTriplet)

    return tokenTriplets
def labelKeterhubungan(word1,word2):


    # word1 = "fruit"
    # word2 = "banana"


    from nltk.corpus import wordnet as wn

    word1 = "fruit"
    word2 = "bowl"

    sinonim_word1 = []
    sinonim_word2 = []
    sinonim = False

    for synset in wn.synsets(word1):
        for line1 in synset.lemma_names():
            if line1 not in sinonim_word1:
                sinonim_word1.append(line1)

    for synset in wn.synsets(word2):
        for line2 in synset.lemma_names():
            if line2 not in sinonim_word2:
                sinonim_word2.append(line2)

    # print("Synonym 1 : ",sinonim_word1)
    # print("Synonym 2 : ",sinonim_word2)

    antonim_word1 = []
    antonim_word2 = []
    antonim = False

    for synset in wn.synsets(word1):
        for line1 in synset.lemmas():
            for line11 in line1.antonyms():
                if line11.name() not in antonim_word1:
                    antonim_word1.append(line11.name())

    for synset in wn.synsets(word2):
        for line2 in synset.lemmas():
            for line22 in line2.antonyms():
                if line22.name() not in antonim_word2:
                    antonim_word2.append(line22.name())

    # print("Antonym 1 : ", antonim_word1)
    # print("Antonym 2 : ", antonim_word2)

    # Hipernim (Kata Umum) dari kata khusus atau Hiponim.

    # Hipernim adalah kata-kata yang mewakili banyak kata lain. Kata hipernim dapat menjadi kata umum dari penyebutan kata-kata lainnya. Sedangkan hiponim adalah kata-kata yang terwakili artinya oleh kata hipernim. Umumnya kata-kata hipernim adalah suatu kategori dan hiponim merupakan anggota dari kata hipernim.

    # Hipernim = buah
    # Hiponim  = anggur, apel, jeruk, manggis dll

    hypernim_word1 = []
    hypernim_word2 = []
    hypernim = False

    for synset in wn.synsets(word1):
        for line1 in synset.hypernyms():
            for line11 in line1.lemma_names():
                if line11 not in hypernim_word1:
                    hypernim_word1.append(line11)

    for synset in wn.synsets(word2):
        for line2 in synset.hypernyms():
            for line22 in line2.lemma_names():
                if line22 not in hypernim_word2:
                    hypernim_word2.append(line22)

    # print("Hyper 1 : ",hypernim_word1)
    # print("Hyper 2 : ",hypernim_word2)

    hyponyms_word1 = []
    hyponyms_word2 = []
    hyponyms = False

    for synset in wn.synsets(word1):
        for line1 in synset.hyponyms():
            for line11 in line1.lemma_names():
                if line11 not in hyponyms_word1:
                    hyponyms_word1.append(line11)

    for synset in wn.synsets(word2):
        for line2 in synset.hyponyms():
            for line22 in line2.lemma_names():
                if line22 not in hyponyms_word2:
                    hyponyms_word2.append(line22)

    # print("Hypo 1 : ",hyponyms_word1)
    # print("Hypo 2 : ",hyponyms_word2)

    # for synset1 in wn.synsets(word1):
    #     for synset2 in wn.synsets(word2):
    #        print "skorrrrrrrrrrrrrrrrr",synset1.path_similarity(synset2),synset1,synset2
    for line1 in sinonim_word1:
        if line1 in sinonim_word2:
            sinonim = True
    #print("Synonym : ", sinonim)

    for line1 in sinonim_word1:
        if line1 in antonim_word2:
            antonim = True
    for line1 in sinonim_word2:
        if line1 in antonim_word1:
            antonim = True
    #print("Antonym : ", antonim)

    for line1 in hyponyms_word1:
        if line1 in hypernim_word2:
            hypernim = True
    if word1 in hypernim_word2:
        hypernim = True
    #print ("hypernim : ", hypernim)

    for line1 in hypernim_word1:
        if line1 in hyponyms_word2:
            hyponyms = True
    if word1 in hyponyms_word2:
        hyponyms = True
    #print "hyponyms : ", hyponyms

    label = "NOALI"
    if sinonim == True:
        label = ' // SIMI //'
    elif antonim == True:
        label = ' // OPPO // 3 //'
    elif hypernim == True:
        label = ' // SPE2 // 4 //'
    elif hyponyms == True:
        label = ' // SPE1 // 4 //'
    else:
        for synset1 in wn.synsets(word1):
            for synset2 in wn.synsets(word2):
                synset1.path_similarity(synset2)
                if synset1.path_similarity(synset2) == 0:
                    label = ' // NOALI // NIL //'
                else:
                    label = ' // REL // '

    sys.stdout.write (label)


def writeMaximunRelatedChunkIds(MaximunRelatedChunkIds, sentence1TokensChunk, sentence2TokensChunk):
    for bestPairCids in MaximunRelatedChunkIds:
        s1Cid = bestPairCids[0]
        s2Cid = bestPairCids[1]
        s1CidTokenTriplet = chunkId2TokenId(s1Cid, sentence1TokensChunk)
        s2CidTokenTriplet = chunkId2TokenId(s2Cid, sentence2TokensChunk)
        s1CidTokenTriplet = addMissings(s1CidTokenTriplet, sentence1Tokens)
        s2CidTokenTriplet = addMissings(s2CidTokenTriplet, sentence2Tokens)
        s1CidTokens = [triplet[0] for triplet in s1CidTokenTriplet]
        s2CidTokens = [triplet[0] for triplet in s2CidTokenTriplet]
        s1CidTokensText = [triplet[1] for triplet in s1CidTokenTriplet]
        s2CidTokensText = [triplet[1] for triplet in s2CidTokenTriplet]

        global S1AlignmentControl
        global S2AlignmentControl

        for tid in s1CidTokens:
            S1AlignmentControl[tid] = True
        for tid in s2CidTokens:
            S2AlignmentControl[tid] = True

        sys.stdout.write(str(s1CidTokens).replace("[", "").replace("]", "").replace(",", ""))
        sys.stdout.write(' <==> ')
        sys.stdout.write(str(s2CidTokens).replace("[", "").replace("]", "").replace(",", ""))

        sys.stdout.write(' // EQUI // 5 // ')
        sys.stdout.write(" ".join([x.encode('UTF8') for x in s1CidTokensText]))
        sys.stdout.write(' <==> ' )
        sys.stdout.write(" ".join([x.encode('UTF8') for x in s2CidTokensText]))
        sys.stdout.write(" \n")
        

def writeOtherRelatedChunkIds(OtherRelatedChunkIdsSentence1, OtherRelatedChunkIdsSentence2, sentence1TokensChunk, sentence2TokensChunk):
    for S1OtherPairCids in OtherRelatedChunkIdsSentence1:
        s1CidTokenTriplet = chunkId2TokenId(S1OtherPairCids, sentence1TokensChunk)
        s1CidTokenTriplet = addMissings(s1CidTokenTriplet, sentence1Tokens)
        s1CidTokens = [triplet[0] for triplet in s1CidTokenTriplet]
        s1CidTokensText = [triplet[1] for triplet in s1CidTokenTriplet]

        global S1AlignmentControl
        global S2AlignmentControl

        for tid in s1CidTokens:
            S1AlignmentControl[tid] = True

        sys.stdout.write(str(s1CidTokens).replace("[", "").replace("]", "").replace(",", ""))
        sys.stdout.write(' <==> ')
        sys.stdout.write(str(0))
        sys.stdout.write(' // NOALI // NIL // ')
        sys.stdout.write(" ".join([x.encode('UTF8') for x in s1CidTokensText]))
        sys.stdout.write(' <==> ' )
        sys.stdout.write("-not aligned-")
        sys.stdout.write(" \n")

    for S2OtherPairCids in OtherRelatedChunkIdsSentence2:
        s2CidTokenTriplet = chunkId2TokenId(S2OtherPairCids, sentence2TokensChunk)
        s2CidTokenTriplet = addMissings(s2CidTokenTriplet, sentence2Tokens)
        s2CidTokens = [triplet[0] for triplet in s2CidTokenTriplet]
        s2CidTokensText = [triplet[1] for triplet in s2CidTokenTriplet]

        for tid in s2CidTokens:
            S2AlignmentControl[tid] = True

        sys.stdout.write(str(0))
        sys.stdout.write(' <==> ')
        sys.stdout.write(str(s2CidTokens).replace("[", "").replace("]", "").replace(",", ""))
        sys.stdout.write(' // NOALI // NIL // ')
        sys.stdout.write("-not aligned-")
        sys.stdout.write(' <==> ' )
        sys.stdout.write(" ".join([x.encode('UTF8') for x in s2CidTokensText]))
        sys.stdout.write(" \n")


def writeAllNotLinkedChunkIds(Sentence1_NotLinked_chunks, Sentence2_NotLinked_chunks, sentence1TokensChunk, sentence2TokensChunk):
    for S1NotLinkedPairCids in Sentence1_NotLinked_chunks:
        s1CidTokenTriplet = chunkId2TokenId(S1NotLinkedPairCids, sentence1TokensChunk)
        s1CidTokenTriplet = addMissings(s1CidTokenTriplet, sentence1Tokens)
        s1CidTokens = [triplet[0] for triplet in s1CidTokenTriplet]
        s1CidTokensText = [triplet[1] for triplet in s1CidTokenTriplet]

        global S1AlignmentControl
        global S2AlignmentControl

        for tid in s1CidTokens:
            S1AlignmentControl[tid] = True


    for S2NotLinkedPairCids in Sentence2_NotLinked_chunks:
        s2CidTokenTriplet = chunkId2TokenId(S2NotLinkedPairCids, sentence2TokensChunk)
        s2CidTokenTriplet = addMissings(s2CidTokenTriplet, sentence2Tokens)
        s2CidTokens = [triplet[0] for triplet in s2CidTokenTriplet]
        s2CidTokensText = [triplet[1] for triplet in s2CidTokenTriplet]

        for tid in s2CidTokens:
            S2AlignmentControl[tid] = True

        # sys.stdout.write(str(s1CidTokens).replace("[", "").replace("]", "").replace(",", ""))
        # sys.stdout.write(' <==> ')
        # sys.stdout.write(str(0))
        # sys.stdout.write(' // NOALI // NIL // ')
        # sys.stdout.write(" ".join([x.encode('UTF8') for x in s1CidTokensText]))
        # sys.stdout.write(' <==> ' )
        # sys.stdout.write("-not aligned-")
        # sys.stdout.write(" \n")
        #
        #
        # sys.stdout.write(str(0))
        # sys.stdout.write(' <==> ')
        # sys.stdout.write(str(s2CidTokens).replace("[", "").replace("]", "").replace(",", ""))
        # sys.stdout.write(' // NOALI // NIL // ')
        # sys.stdout.write("-not aligned-")
        # sys.stdout.write(' <==> ' )
        # sys.stdout.write(" ".join([x.encode('UTF8') for x in s2CidTokensText]))
        # sys.stdout.write(" \n")



        sys.stdout.write(str(s1CidTokens).replace("[", "").replace("]", "").replace(",", ""))
        sys.stdout.write(' <==> ')
        sys.stdout.write(str(s2CidTokens).replace("[", "").replace("]", "").replace(",", ""))
        a= labelKeterhubungan(" ".join([x.encode('UTF8') for x in s1CidTokensText]),
                 " ".join([x.encode('UTF8') for x in s2CidTokensText]))
        #sys.stdout.write(a)
        #sys.stdout.write(a,' // SIMI // NIL // ')
        sys.stdout.write(" ".join([x.encode('UTF8') for x in s1CidTokensText]))
        sys.stdout.write(' <==> ' )
        sys.stdout.write(" ".join([x.encode('UTF8') for x in s2CidTokensText]))
        sys.stdout.write(" \n")



def writeAllNotAlignableTokenIds(Sentence1_NotAlignable_tokens, Sentence2_NotAlignable_tokens):
    for S1NotAlignableTokenId in Sentence1_NotAlignable_tokens:
        s1CidToken = S1NotAlignableTokenId[0]
        s1CidTokenText = S1NotAlignableTokenId[1]

        global S1AlignmentControl
        global S2AlignmentControl

        S1AlignmentControl[s1CidToken] = True

        sys.stdout.write(str(s1CidToken).replace("[", "").replace("]", "").replace(",", ""))
        sys.stdout.write(' <==> ')
        sys.stdout.write(str(0))
        sys.stdout.write(' // NOALI // NIL // ')
        sys.stdout.write(" ".join([x.encode('UTF8') for x in s1CidTokenText]))
        sys.stdout.write(' <==> ' )
        sys.stdout.write("-not aligned-")
        sys.stdout.write(" \n")


    for S2NotAlignableTokenId in Sentence2_NotAlignable_tokens:
        s2CidToken = S2NotAlignableTokenId[0]
        s2CidTokenText = S2NotAlignableTokenId[1]
        S2AlignmentControl[s2CidToken] = True


        sys.stdout.write(str(0))
        sys.stdout.write(' <==> ')
        sys.stdout.write(str(s2CidToken).replace("[", "").replace("]", "").replace(",", ""))
        sys.stdout.write(' // NOALI // NIL // ')
        sys.stdout.write("-not aligned-")
        sys.stdout.write(' <==> ' )
        sys.stdout.write(" ".join([x.encode('UTF8') for x in s2CidTokenText]))
        sys.stdout.write("\n")


def writeAllForgottenTokenIds(sentence1_forgottens, sentence2_forgottens, sentence1Tokens, sentence2Tokens):
    for S1ForgottenTokenId in sentence1_forgottens:
        s1CidToken = S1ForgottenTokenId
        s1CidTokenText = sentence1Tokens[S1ForgottenTokenId-1][1]

        global S1AlignmentControl
        global S2AlignmentControl

        S1AlignmentControl[s1CidToken] = True

        sys.stdout.write(str(s1CidToken).replace("[", "").replace("]", "").replace(",", ""))
        sys.stdout.write(' <==> ')
        sys.stdout.write(str(0))
        sys.stdout.write(' // NOALI // NIL // ')
        sys.stdout.write(" ".join([x.encode('UTF8') for x in s1CidTokenText]))
        sys.stdout.write(' <==> ' )
        sys.stdout.write("-not aligned-")
        sys.stdout.write("\n")


    for S2ForgottenTokenId in sentence2_forgottens:
        s2CidToken = S2ForgottenTokenId
        s2CidTokenText = sentence2Tokens[S2ForgottenTokenId-1][1]
        S2AlignmentControl[s2CidToken] = True

        sys.stdout.write(str(0))
        sys.stdout.write(' <==> ')
        sys.stdout.write(str(s2CidToken).replace("[", "").replace("]", "").replace(",", ""))
        sys.stdout.write(' // NOALI // NIL // ')
        sys.stdout.write("-not aligned-")
        sys.stdout.write(' <==> ' )
        sys.stdout.write(" ".join([x.encode('UTF8') for x in s2CidTokenText]))
        sys.stdout.write(" \n")


def findSameTokens(sentence1Tokens,sentence2Tokens):
    sameTokens = []
    for i in xrange(len(sentence1Tokens)):
        for j in xrange(len(sentence2Tokens)):
            if (sentence2Tokens[j][1] == sentence1Tokens[i][1]):
                sameTokens.append([i+1, j+1])
    return sameTokens

############################################
################ MAIN SCRIPT ###############
############################################

lines_chunked = 'True'
a='train_2015_10_22.utf-8/simpandata1.chunk.txt'
b='train_2015_10_22.utf-8/simpandata2.chunk.txt'
if lines_chunked == "True":
    sent1_lines = readFileWithChunks(a.lower())
    sent2_lines = readFileWithChunks(b.lower())
    sent1_lines_chunked = readFile(a.lower())
    sent2_lines_chunked = readFile(b.lower())
else:
    sent1_lines = readFile(a.lower())
    sent2_lines = readFile(b.lower())

if len(sent1_lines) != len(sent2_lines):
    print "files have different number of lines... quiting"
    exit(-1)

for pair_id in range(len(sent1_lines)):
    sentence1 = sent1_lines[pair_id]
    sentence2 = sent2_lines[pair_id]

    sentence1Tokens = []
    index = 1
    for element in re.findall(r"[^ ]+", sentence1):
        sentence1Tokens.append([index, element, element])
        index += 1

    sentence2Tokens = []
    index = 1
    for element in re.findall(r"[^ ]+", sentence2):
        sentence2Tokens.append([index, element, element])
        index += 1

    print 'sentence1Tokens',sentence1Tokens
    print 'sentence2Tokens', sentence2Tokens
    idAlignments = findSameTokens(sentence1Tokens,sentence2Tokens)
    print 'idAlignments',idAlignments

    sentence1Chunks = []
    sentence2Chunks = []
    sentence1TokensChunk = []
    sentence2TokensChunk = []

    if lines_chunked == "True":
        sentence1Chunks = extractChunksFromSentence(sent1_lines_chunked[pair_id])
        sentence2Chunks = extractChunksFromSentence(sent2_lines_chunked[pair_id])
    else:       
        sentence1Chunks = extractChunksFromIxaPipes(sentence1Tokens)
        sentence2Chunks = extractChunksFromIxaPipes(sentence2Tokens)

    print "sentence1chunk", sentence1Chunks
    print "sentence2chunk",sentence2Chunks

    sentence1TokensChunk = findTokensForChunk(sentence1Chunks, sentence1Tokens)
    sentence2TokensChunk = findTokensForChunk(sentence2Chunks, sentence2Tokens)

    print "sentence1Tokenschunk", sentence1TokensChunk
    print "sentence2Tokenschunk", sentence2TokensChunk

    token2tokenLinkMatrix = createToken2tokenLinkMatrix(sentence1TokensChunk, sentence2TokensChunk, idAlignments)
    chunk2chunkLinkMatrix = createChunk2chunkLinkMatrix(sentence1TokensChunk, sentence2TokensChunk, token2tokenLinkMatrix)

    print "token2tokenLinkMatrix", token2tokenLinkMatrix
    print "chunk2chunkLinkMatrix", chunk2chunkLinkMatrix

    Sentence1_NotAlignable_tokens = getNotAlignableTokenIds(sentence1Tokens, sentence1TokensChunk)
    Sentence2_NotAlignable_tokens = getNotAlignableTokenIds(sentence2Tokens, sentence2TokensChunk)

    print "Sentence1_NotAlignable_tokens", Sentence1_NotAlignable_tokens
    print "Sentence2_NotAlignable_tokens", Sentence2_NotAlignable_tokens

    Sentence1_NotAlignable_chunks = getChunksForNotAlignableTokens(Sentence1_NotAlignable_tokens)
    Sentence2_NotAlignable_chunks = getChunksForNotAlignableTokens(Sentence2_NotAlignable_tokens)

    print "Sentence1_NotAlignable_chunks", Sentence1_NotAlignable_chunks
    print "Sentence2_NotAlignable_chunks", Sentence2_NotAlignable_chunks

    Sentence1_NotLinked_chunks = getNotLinkedChunkIdsSentence1(chunk2chunkLinkMatrix, sentence1TokensChunk)
    Sentence2_NotLinked_chunks = getNotLinkedChunkIdsSentence2(chunk2chunkLinkMatrix, sentence2TokensChunk)

    print "Sentence1_NotLinked_chunks", Sentence1_NotLinked_chunks
    print "Sentence2_NotLinked_chunks", Sentence2_NotLinked_chunks
    Sentence1_Linked_chunks = getLinkedChunkIdsSentence1(chunk2chunkLinkMatrix, sentence1TokensChunk)
    Sentence2_Linked_chunks = getLinkedChunkIdsSentence2(chunk2chunkLinkMatrix, sentence2TokensChunk)

    print "Sentence1_Linked_chunks", Sentence1_Linked_chunks
    print "Sentence2_Linked_chunks", Sentence2_Linked_chunks
    Sentence1_Noali_Tokens = Sentence1_NotAlignable_tokens + chunkIds2TokenIds(Sentence1_NotLinked_chunks, sentence1TokensChunk)
    Sentence2_Noali_Tokens = Sentence2_NotAlignable_tokens + chunkIds2TokenIds(Sentence2_NotLinked_chunks, sentence2TokensChunk)

    print "Sentence1_Noali_Tokens", Sentence1_Noali_Tokens
    print "Sentence2_Noali_Tokens", Sentence2_Noali_Tokens
    chunk2chunkReducedLinkMatrix = createChunk2chunkReducedLinkMatrix(chunk2chunkLinkMatrix, Sentence1_Linked_chunks, sentence1TokensChunk, Sentence2_Linked_chunks, sentence2TokensChunk)
    print 'chunk2chunkReducedLinkMatrix',chunk2chunkReducedLinkMatrix
    cleanMatrix = cleanEpsilons(chunk2chunkReducedLinkMatrix)
    print 'cleanMatrix',cleanMatrix
    LinkCostMatrix = munkres.make_cost_matrix(cleanMatrix, lambda cost: 100 - cost)
    hungarianMunkres = Munkres()
    
    try:
        bestIndexes = hungarianMunkres.compute(LinkCostMatrix)
    except:
        bestIndexes = []

    MaximunRelatedChunkIds = getMaximunRelatedChunkIds(bestIndexes, Sentence1_Linked_chunks, Sentence2_Linked_chunks)
    #urutan chunk
    print "MaximunRelatedChunkIds",MaximunRelatedChunkIds
    OtherRelatedChunkIds = getOtherRelatedChunkIds(chunk2chunkReducedLinkMatrix, bestIndexes, Sentence1_Linked_chunks, Sentence2_Linked_chunks)
    print " OtherRelatedChunkIds", OtherRelatedChunkIds
    OtherRelatedChunkIdsSentence1 = OtherRelatedChunkIds[0]
    print "OtherRelatedChunkIdsSentence1",OtherRelatedChunkIdsSentence1
    OtherRelatedChunkIdsSentence2 = OtherRelatedChunkIds[1]

    S1AlignmentControl = {}
    S2AlignmentControl = {}

    print '<sentence id="' + str(pair_id+1) + '" status="">'
    print '// ' + sentence1.encode("utf-8")
    print '// ' + sentence2.encode("utf-8")
    print '<source>'
    for item in sentence1Tokens:
        print str(item[0]) + " " + item[1].encode("utf-8") + " : "
        S1AlignmentControl[item[0]] = False
    print '</source>'
    print '<translation>'
    for item in sentence2Tokens:
        print str(item[0]) + " " + item[1].encode("utf-8") + " : "
        S2AlignmentControl[item[0]] = False
    print '</translation>'
    print '<alignment>'

    print "Maximum"
    writeMaximunRelatedChunkIds(MaximunRelatedChunkIds, sentence1TokensChunk, sentence2TokensChunk)
    print "Other Related"
    writeOtherRelatedChunkIds(OtherRelatedChunkIdsSentence1, OtherRelatedChunkIdsSentence2, sentence1TokensChunk, sentence2TokensChunk)
    print "Not Linked"
    writeAllNotLinkedChunkIds(Sentence1_NotLinked_chunks,Sentence2_NotLinked_chunks, sentence1TokensChunk, sentence2TokensChunk)
    print "Not Align"
    writeAllNotAlignableTokenIds(Sentence1_NotAlignable_tokens, Sentence2_NotAlignable_tokens)

    # sentence1_forgottens = []
    #
    # for key in S1AlignmentControl.keys():
    #     if S1AlignmentControl[key] == False:
    #         sentence1_forgottens.append(int(key))
    #
    # sentence2_forgottens = []
    #
    # for key in S2AlignmentControl.keys():
    #     if S2AlignmentControl[key] == False:
    #         sentence2_forgottens.append(int(key))
    #
    # writeAllForgottenTokenIds(sentence1_forgottens, sentence2_forgottens, sentence1Tokens, sentence2Tokens)

    print '</alignment>'
    print
    print
