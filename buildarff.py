import sys
import re
import math

# first person pronouns
def feat1(tweet):
    t = tweet.split(" ")
    for word in t:
        a = re.match("\w+/", word.lower())
        if a is not None and a.group() in FP:
            TWT_DATA[0] += 1
    return TWT_DATA   

# second person pronouns
def feat2(tweet):
    t = tweet.split(" ")
    for word in t:
        a = re.match("\w+/", word.lower())
        if a is not None and a.group() in SP:
            TWT_DATA[1] += 1 
    return TWT_DATA

# thrid person pronouns
def feat3(tweet):
    t = tweet.split(" ")
    for word in t:
        a = re.match("\w+/", word.lower())
        if a is not None and a.group() in TP:
            TWT_DATA[2] += 1 
    return TWT_DATA    

# Coordinating conjunctions
def feat4(tweet):
    t = re.findall("/CC", tweet)
    TWT_DATA[3] += len(t)
    return TWT_DATA

# Past-tense verbs
def feat5(tweet):
    t = re.findall("/VBD", tweet)
    TWT_DATA[4] += len(t)
    return TWT_DATA

# Future-tense verbs
def feat6(tweet):
    t = tweet.split(" ")
    for word in t:
        a = re.match("'?\w+/", word.lower())
        if a is not None and a.group() in FTV:
            TWT_DATA[5] += 1 
    t2 = re.findall("going/\w+ to/\w+ \w+/VB", tweet, flags=re.I)
    TWT_DATA[5] += len(t2)
    return TWT_DATA

# Commas
def feat7(tweet):
    t = re.findall(",/,", tweet)
    TWT_DATA[6] += len(t)
    return TWT_DATA

# Colons and semi-colons
def feat8(tweet):
    t = re.findall(":/:|;/:", tweet)
    TWT_DATA[7] += len(t)
    return TWT_DATA

# Dashes
def feat9(tweet):
    t = re.findall("-+/:", tweet)
    TWT_DATA[8] += len(t)
    return TWT_DATA

# Parentheses 
def feat10(tweet):
    t = re.findall("\(/\(|\)/\)", tweet)
    TWT_DATA[9] += len(t)
    return TWT_DATA

# Ellipses
def feat11(tweet):
    t = re.findall("\.\.+", tweet)
    TWT_DATA[10] += len(t)
    return TWT_DATA

# Common nouns
def feat12(tweet):
    t = re.findall("/NN\s|/NNS\s", tweet)
    TWT_DATA[11] += len(t)
    return TWT_DATA

# Proper nouns
def feat13(tweet):
    t = re.findall("/NNP\s|/NNPS\s", tweet)
    TWT_DATA[12] += len(t)
    return TWT_DATA

# Adverbs
def feat14(tweet):
    t = re.findall("/RB\s|/RBR\s|/RBS\s", tweet)
    TWT_DATA[13] += len(t)
    return TWT_DATA

# wh-words
def feat15(tweet):
    t = re.findall("/WDT\s|/WP\s|/WP\$\s|/WRB\s", tweet)
    TWT_DATA[14] += len(t)
    return TWT_DATA

# Modern slang acronyms
def feat16(tweet):
    t = tweet.split(" ")
    for word in t:
        a = re.match("\w+/", word.lower())
        if a is not None and a.group()[0:-1] in MS:
            TWT_DATA[15] += 1
    return TWT_DATA

# Words all in upper case
def feat17(tweet):
    t = re.findall("[A-Z][A-Z]+/", tweet)
    TWT_DATA[16] += len(t)
    return TWT_DATA

# Average length of sentences
def feat18(tweet):
    t = tweet.split()
    TWT_DATA[17] += len(t)
    return TWT_DATA

# Average length of tokens, no punctuation tokens
def feat19(tweet):
    t = re.findall("\w+(?=/\w+)", tweet)
    for word in t:
        TWT_DATA[18] += len(word)   
    return (TWT_DATA, len(t))

# Number of sentences
def feat20():
    TWT_DATA[19] += 1
    return TWT_DATA

# get positive/negative class
def getClass(clas):
    if clas:
        TWT_DATA[20] = clas.group()
        return TWT_DATA

# build the arff file
def arff(in_file, out_file, max_twts):
    # defining the bound if max tweets is > 20000
    max_twts = int(max_twts) + 1
    if max_twts >= 20000:
        max_twts = float('inf')
    of = open(out_file, "w")
    inf = open(in_file, "r")
    
    # write out the header of the arff file for WEKA
    of.write("@relation sentiment \n")
    of.write("\n")
    of.write("@attribute 'First person pronouns' numeric \n")
    of.write("@attribute 'Second person pronouns' numeric \n")
    of.write("@attribute 'Third person pronouns' numeric \n")
    of.write("@attribute 'Cordinating conjunctions' numeric \n")
    of.write("@attribute 'Past-tense verbs' numeric \n")
    of.write("@attribute 'Future-tense verbs' numeric \n")
    of.write("@attribute Commas numeric \n")
    of.write("@attribute 'Colons and semi-colons' numeric \n")
    of.write("@attribute Dashes numeric \n")
    of.write("@attribute Parenthesis numeric \n")
    of.write("@attribute Ellipses numeric \n")
    of.write("@attribute 'Common nouns' numeric \n")
    of.write("@attribute 'Proper nouns' numeric \n")
    of.write("@attribute Adverbs numeric \n")
    of.write("@attribute wh-words numeric \n")
    of.write("@attribute 'Modern slang acronyms' numeric \n")
    of.write("@attribute 'Words all in upper case'  numeric \n")
    of.write("@attribute 'Average length of sentence' numeric \n")
    of.write("@attribute 'Average length of tokens' numeric \n")
    of.write("@attribute 'Number of sentences' numeric \n")
    of.write("@attribute class {0,4} \n")
    of.write("\n")
    of.write("@data \n")
    wc = 0
    twt_count = 0
    numPosTweets = 0
    numNegTweets = 0
    
    # Parsing each tweet from the input file
    for line in inf:
        new_twt = re.search("<A=", line)
        if new_twt:
            twt_count += 1
            # Add class (positive|negative)
            clas = re.search("[0-4]", line)
            twt_class = int(clas.group())
            if twt_class == 0:
                numNegTweets += 1
            if twt_class == 4:
                numPosTweets += 1
            #Average length of sentences
            if TWT_DATA[19]: 
                TWT_DATA[17] = float(TWT_DATA[17]) / TWT_DATA[19]
            #Average length of tokens
            if wc:
                TWT_DATA[18] = float(TWT_DATA[18]) / wc
                wc = 0
            # write the stats vector to the output file
            if twt_count > 1: 
                str1 = ''.join((str(e) + ",") for e in TWT_DATA)
                str1 = str1[0:-1]                
                if twt_class == 0 and numNegTweets <= max_twts:
                    of.write(str1 + "\n")
                if twt_class == 4 and numPosTweets <= max_twts:
                    of.write(str1 + "\n")                
            # Everytime a new tweet starts zero the stats vector
            for i in range(21):
                TWT_DATA[i] = 0 
        else:
            feat1(line)
            feat2(line)
            feat3(line)
            feat4(line)
            feat5(line)
            feat6(line)
            feat7(line)
            feat8(line)
            feat9(line)
            feat10(line)
            feat11(line)
            feat12(line)
            feat13(line)
            feat14(line)
            feat15(line)
            feat16(line)
            feat17(line)
            feat18(line)
            wc += feat19(line)[-1]
            feat20() 
            getClass(clas)
    # write the last stats vector to the output file    
    str1 = ''.join((str(e) + ",") for e in TWT_DATA)
    str1 = str1[0:-1]
    if twt_class == 0 and numNegTweets <= max_twts:
        of.write(str1 + "\n")
    if twt_class == 4 and numPosTweets <= max_twts:
        of.write(str1 + "\n")
        
    of.close()
    inf.close()

if __name__ == '__main__':
    # Tweet vector
    TWT_DATA = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # First person pronouns
    FP = ["i/", "me/", "my/", "mine/", "we/", "us/", "our/", "ours/"]
    # Second person pronouns
    SP = ["you/", "your/", "yours/", "u/", "ur/", "urs/"]
    # Third person pronouns
    TP = ["he/", "him/", "his/", "she/", "her/", "hers/", "it/", "its/", "they/", "them/", "their/", "theirs/"]
    # Future Tense Verbs
    FTV = ["'ll/", "will/", "gonna/"]
    # Modern Slang-Words
    MS = ["smh", "fwb", "lmfao", "lmao", "lms", "tbh", "rofl", "wtf", "bff", "wyd", "lylc", "brb", "atm", "imao", "sml", "btw", "bw", "imho", "fyi", "ppl", "sob", "ttyl", "imo", "ltr", "thx", "kk", "omg", "ttys", "afn", "bbs", "cya", "ez", "f2f", "gtr",
"ic", "jk", "k", "ly", "ya", "nm", "np", "plz", "ru", "so", "tc", "tmi", "ym", "ur", "u", "sol", "lol"]
    # Handeling number of arguments
    if len(sys.argv) == 3:
        arff(sys.argv[1], sys.argv[2], 20000)
    if len(sys.argv) == 4:
        arff(sys.argv[1], sys.argv[2], sys.argv[3])
