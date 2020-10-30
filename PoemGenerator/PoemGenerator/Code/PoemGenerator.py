import json
import functions as F
import os.path as PATH
import os as OS
import nltk
import sys
from nltk.corpus import gutenberg

#Handling the first input concerning if the right corpus are loaded in the system
if(not PATH.exists(PATH.join(OS.getcwd(),"stories.json"))):
    if(len(sys.argv) == 0 or sys.argv[0] == True):
        valid = False
        while(not valid):
            print("")
            valid_corpus = str(input())
            if(valid_corpus.lower() == "true" or valid_corpus.lower() == "false"):
                if(valid_corpus.lower() == "true"):
                    nltk.download()
                valid = True

    elif(len(sys.argv) != 0 and sys.argv[0] != False):
        print("The first argument is not a valid argument")
        exit()


    sentences = gutenberg.sents('austen-emma.txt')
    sentences += gutenberg.sents('austen-persuasion.txt')
    sentences += gutenberg.sents('austen-sense.txt')
    #sentences += gutenberg.sents('bible-kjv.txt')
    #sentences += gutenberg.sents('blake-poems.txt')
    #sentences += gutenberg.sents('bryant-stories.txt')
    #sentences += gutenberg.sents('burgess-busterbrown.txt')
    #sentences += gutenberg.sents('carroll-alice.txt')
    #sentences += gutenberg.sents('chesterton-ball.txt')
    #sentences += gutenberg.sents('chesterton-brown.txt')
    #sentences += gutenberg.sents('chesterton-thursday.txt')
    #sentences += gutenberg.sents('edgeworth-parents.txt')
    #sentences += gutenberg.sents('melville-moby_dick.txt')
    #sentences += gutenberg.sents('milton-paradise.txt')
    #sentences += gutenberg.sents('shakespeare-caesar.txt')
    #sentences += gutenberg.sents('shakespeare-hamlet.txt')
    #sentences += gutenberg.sents('shakespeare-macbeth.txt')
    #sentences += gutenberg.sents('whitman-leaves.txt')


    n_grams = []
    for sentence in sentences:
        n_grams += F.reversen_grams(sentence, 3)

    model = F.setupModel(n_grams)

    with open('Data_Output/stories.json', 'w') as outfile:
        json.dump(model, outfile)

with open('Data_Output/stories.json', 'r') as infile:    
    corpus = json.load(infile)
  
filestream = open('Data_Output/poems.html','w')
filestream.write("<html>")

valid_poems = int(sys.argv[1])
valid_couplets = int(sys.argv[2])

if(len(sys.argv) == 1 or int(sys.argv[1]) < 1):
    valid_poems = 0
    while(valid_poems < 1):
        print("")
        valid_poems = int(input())

if(len(sys.argv) == 2 or int(sys.argv[2]) < 1):
    valid_couplets = 0
    while(valid_couplets < 1):
        print("")
        valid_couplets = int(input())

for x in range(poems):
    F.addPoem(corpus,filestream,valid_couplets)

filestream.write("</html>")
filestream.close()
