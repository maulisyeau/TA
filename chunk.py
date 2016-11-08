import nltk
from nltk.corpus import state_union
from  nltk.tokenize import PunktSentenceTokenizer




'''
pos tag list :

CC      coordinating conjuction
CD      cardinal digit
DT      determiner
EX      existential there (like:" there is"... think of it like "there exists")
FW      foreign word
IN      preposition / subordinating conjunction
JJ      adjective 'big'
JJR     adjective, comparative 'bigger'
JJS     adjective, superlative 'biggest'
LS      list marker 1)
MD      modal could, will
NN      noun, singular 'desk'
NNS     noun plural 'desks'
NNP     proper noun, singular 'Harrison'
NNPS    proper noun, plural 'Americans'
PDT     predeterminer 'all the kids'
POS     possessive ending  parents's
PRP     personal pronoun  I, he, she
PRPS    prossessive pronoun my, his, hers
RB      adverb  very, silently
RBR     adverb, comparative better
RBS     adverb, superlative best
RP      particle  give up
TO      to  . go'to' the store
UH      interjection  errrrrrrrm
VB      verb, base from take
VBD     verb, past tense
VBG     verb, gerund/ present participle teking
VBN     verb, past participle taken
VBP     verb, sing. present, non-3d  take
VBZ     verb, 3rd person sing.persent takes
WDT     wh-determiner which
WP      wh-pronoun  who, what
WPS     possessive wh-pronoun whose
WRB     wh-abverb   where, when


'''
psng1= state_union.raw("STSint.testinput.headlines.sent1.txt")
psng2= state_union.raw("STSint.testinput.headlines.sent2.txt")

custom  = PunktSentenceTokenizer(psng1)
token = custom.tokenize(psng2)

def proses():
    try:
        for i in token:
            words= nltk.word_tokenize(i)
            tag=nltk.pos_tag(words)
            #print (tag)


            chunkGram = r"""chunk : {<RB.?>*<VB.?>*<NNP><NN>?}"""
            chunkParser=nltk.RegexpParser(chunkGram)
            chunked=chunkParser.parse(tag)
            print (chunked)
            chunked.draw()
            print "------------- ini batasannya ====================="

    except Exception as e:
        print (str(e))
proses()