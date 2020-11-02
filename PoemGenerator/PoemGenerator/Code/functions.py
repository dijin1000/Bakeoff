import random
import pronouncing
import regex as re
import numpy as np

sign_pattern = re.compile("[^0-9a-zA-Z *]")
sign_weird_pattern = re.compile(r'[_\(\){}+="-]')

#defining all symbols
def is_sign(word):
    return (sign_pattern.match(word) != None)

#defining symbols that are not allowed in titels.
def is_weird_sign(word):
    return (sign_weird_pattern.match(word) != None)


# Create reverse N-grams from a list of tokens
def reversen_grams(tokens, n):
    n_grams = []
    for i in range(len(tokens)-1, 0+n-2, -1):
        n_gram = []
        for j in range(i, i-n, -1):
            n_gram.append(tokens[j])
        n_grams.append(n_gram)
    return n_grams

# Organize N-grams in a frequency table (N-layer nested dictionaries)
def setupModel(n_grams):
    table = {}
    n = len(n_grams[0])
    for n_gram in n_grams:
        ptr = table
        for i in range(0, n):
            if i == n-1:
                ptr.setdefault(n_gram[i], 0)
                ptr[n_gram[i]] += 1
            else:
                try: ptr = ptr[n_gram[i]]
                except KeyError: 
                    ptr.setdefault(n_gram[i], {})
                    ptr = ptr[n_gram[i]]
    return table

# Loads all first words into an array for efficiency
def getFirstWords(corpus):
    firstWords = []
    for first in corpus:
        if(not is_weird_sign(first)):
            firstWords.append(first)
    return firstWords

# Randomly chooses a word from the corpus
def findFirst(corpus, firstWords):
    idx = random.randrange(0, len(firstWords)-1)
    return firstWords[idx]

# Randomly chooses a second word from the corpus based on the first 
def findSecond(first, corpus, firstWords):
    list_of_words = []
    try:
        for second in corpus[first]:
            list_of_words.append(second)
    except KeyError:
        return findFirst(corpus, firstWords)
        
    if len(list_of_words) == 0: return findFirst(corpus, firstWords)
    elif len(list_of_words) == 1: return list_of_words[0]
    
    idx = random.randrange(0, len(list_of_words)-1)
    return list_of_words[idx]
   
# Randomly chooses a third word from the corpus based on the first and second    
def findThird(first, second, corpus, firstWords):
    list_of_words = []
    try: 
        for third in corpus[first][second]:
            list_of_words.append(third)
    except KeyError:
        return findSecond(second, corpus, firstWords)
            
    if len(list_of_words) == 0: return findSecond(second, corpus, firstWords)
    elif len(list_of_words) == 1: return list_of_words[0]
    
    pick = random.randrange(0, len(list_of_words)-1)
    return list_of_words[pick]

# Builds sentences word by word
def addWord(sentence, first, second, corpus, firstWords):
    third = findThird(first, second, corpus, firstWords)
    sentence.append(third.lower())
    first, second = second, third
    return first, second

# Randomly chooses a rhyming word from the corpus
def findRhyme(word, corpus):
    rhymes = pronouncing.rhymes(word)
    while (True):
        if len(rhymes) == 0:
            return None
      
        elif len(rhymes) == 1:
            try:
                corpus[rhymes[0]]
                return rhymes[0]
            except KeyError:
                return None        
        
        else:
            pick = random.randrange(0, len(rhymes)-1)
            try:
                corpus[rhymes[pick]]
                return rhymes[pick]
            except KeyError:
                rhymes.remove(rhymes[pick])
                continue

# Implementation of a 1 a 10 word
def generateTitle(corpus):
    return generateCouplet(corpus,1,max(int(np.random.normal(3,3)),1))

# Implementation of a couplet - AABB CCDD EEFF GGHH
def generateCouplet(corpus, lines, wordsPerLine):
    firstWords = getFirstWords(corpus)
    poem = []   
    for i in range(lines):            
        line = []  
        if i % 2 == 0:
            while (True):
                A = findFirst(corpus, firstWords)
                AA = findRhyme(A, corpus)                
                if AA != None:
                    break 
    
            first = A
            second = findSecond(first, corpus, firstWords)
            line += [first.lower(), second.lower()]
            
        
        if i % 2 == 1:
            first = AA
            second = findSecond(first, corpus, firstWords)
            line += [first.lower(), second.lower()]
        
        for j in range(wordsPerLine-2):
            first, second = addWord(line, first, second, corpus, firstWords)

        if(is_sign(second)):
            line = line[:-1]
        
        poem.append(line[::-1])
    return poem
 
# Handles capitalization lost from pre-processing
def processing(poem):
    for line in poem:
        line[0] = line[0][0].upper()+line[0][1:]
        for index, word in enumerate(line):
            if word[0:2] == "i'":
                line[index] = word[0:2].upper()+word[2:]
            if word == 'i':
                line[index] = word.upper()

def stringfyText(poem):
    p = ""
    for line in poem:
        l = ""
        first = True
        for word in line:
            if(not is_sign(word) and first == False):
                l += " "  + word
            else:
                l += word
            first = False
        p += l + "<br />"
    return p

def stringfyTitle(title):
    titlestring = ""
    for line in title:
        l = ""
        first = True
        for word in line:
            if(not is_sign(word) and first == False):
                l += " "  + word
            elif(not is_weird_sign(word)):
                l += word
                first = False
        titlestring += l 
    return titlestring

def addPoem(corpus,file,nmbr_couplets):

    title = generateTitle(corpus)
    processing(title) 
    title = stringfyTitle(title)
    couplets = []
    poem = ""
    for i in range(nmbr_couplets):
        couplet = generateCouplet(corpus, 8, 10)
        processing(couplet) 
        couplet = stringfyText(couplet)
        poem += couplet + "<br />"

    message = """<article class="w3-third">
    <p style="font-size:20px">{0}</p>
    <p><i>{1}</i></p>
  </article>
    """.format(title,poem)

    file.write(message)

