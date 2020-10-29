import json
from nltk.corpus import gutenberg
import functions as F
import os.path as PATH
import os as OS

if(not PATH.exists(PATH.join(OS.getcwd(),"stories.json"))):
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

    with open('stories.json', 'w') as outfile:
        json.dump(model, outfile)

with open('stories.json', 'r') as infile:    
    corpus = json.load(infile)
  
filestream = open('poems.html','w')
filestream.write("<html>")

for x in range(10):
    F.addPoem(corpus,filestream)

filestream.write("</html>")
filestream.close()
