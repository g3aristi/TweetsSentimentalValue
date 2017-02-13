import sys
import csv
import re
import HTMLParser
import NLPlib
import linecache

abbrevGlobal = ['ala.', 'ariz.', 'assn.', 'atty.', 'aug.', 'ave.', 'bldg.', 'blvd.', 'calif.', 'capt.', 'cf.', 'ch.', 'co.', 'col.', 'colo.', 'conn.', 'corp.', 'dr.', 'dec.', 'dept.', 'dist.', 'dr.', 'drs.', 'ed.', 'eq.', 'feb.', 'feb.', 'fig.', 'figs.', 'fla.', 'ga.', 'gen.', 'gov.', 'hon.', 'ill.', 'inc.', 'jr.', 'jan.', 'jr.', 'kan.', 'ky.', 'la.', 'lt.', 'ltd.', 'mr.', 'mrs.', 'mar.', 'mass.', 'md.', 'messrs.', 'mich.', 'minn.', 'miss.', 'mmes.', 'mo.', 'mr.', 'mrs.', 'mt.', 'no.', 'no.', 'nov.', 'oct.', 'okla.', 'op.', 'ore.', 'pa.', 'pp.', 'prof.', 'prop.', 'rd.', 'ref.', 'rep.', 'reps.', 'rev.', 'rte.', 'sen.', 'sept.', 'sr.', 'st.', 'stat.', 'supt.', 'tech.', 'tex.', 'va.', 'vol.', 'wash.', 'al.', 'av.', 'ave.', 'ca.', 'cc.', 'chap.', 'cm.', 'cu.', 'dia.', 'dr.', 'eqn.', 'etc.', 'fig.', 'figs.', 'ft.', 'gm.', 'hr.', 'in.', 'kc.', 'lb.', 'lbs.', 'mg.', 'ml.', 'mm.', 'mv.', 'nw.', 'oz.', 'pl.', 'pp.', 'sec.', 'sq.', 'st.', 'vs.', 'yr.', 'capt.', 'col.', 'dr.', 'drs.', 'fig.', 'figs.', 'gen.', 'gov.', 'hon.', 'mr.', 'mrs.', 'messrs.', 'miss.', 'mmes.', 'mr.', 'mrs.', 'ref.', 'rep.', 'reps.', 'sen.', 'fig.', 'figs.', 'vs.', 'lt.', 'e.g.', 'i.e', 'capt.', 'col.', 'dr.', 'drs.', 'fig.', 'figs.', 'gen.', 'gov.', 'hon.', 'mr.', 'mrs.', 'messrs.', 'miss.', 'mmes.', 'mr.', 'mrs.', 'ref.', 'rep.', 'reps.', 'sen.', 'fig.', 'figs.', 'vs.', 'lt.', 'e.g.', 'i.e', 'p.y.t']

tagger = NLPlib.NLPlib()
        
#extracting the tweet from the csv file
def get_rawTweet(CSV_tweet):  
    return CSV_tweet[-1]

#extracting the polarity of the tweet from the csv file
def get_pol(CSV_tweet):  
    return CSV_tweet[0]

# All html tags and attributes (i.e.,/<[^>]+>/) are removed.
def twtt1(tweet):
    return re.sub("<[^>]+?>", '', tweet)

# Html character codes (i.e.,&...;) are replaced with an ASCII equivalent.
def twtt2(tweet):
    h = HTMLParser.HTMLParser()
    for match in re.finditer("&.{1,5};", tweet):
        tweet = tweet.replace(match.group(), str(h.unescape(match.group())))
    return tweet

# All URLs (i.e., tokens beginning with http or www) are removed
def twtt3(tweet):
    return re.sub(r'[h|H][t|T][t|T][p|P][s]?://[^\s<>"]+|www\.[^\s<>"]+', '',tweet)

# The first character in Twitter user names and hash tags (i.e., @ and #) are removed
def twtt4(tweet):
    return re.sub("(@|#)", '',tweet)

# Each sentence within a tweet is on its own line.
def twtt5(tweet):  
    for match in re.finditer('\w+\.(\s|\")|\w+\?+(\s|\")|\w+!+(\s|\")', tweet):
        if match.group().lower() not in abbrevGlobal:
            tweet = tweet.replace(match.group(), match.group() + "\n") 
    return tweet

# Ellipsis (i.e., `...'), and other kinds of multiple punctuation (e.g., `!!!')  are not split.
def twtt6(tweet):
    return tweet

#My own replace function for separating punctuation
def myRepl(match_obj):
    return " " + match_obj.group() + " "

# Each token, including punctuation and clitics, is separated by spaces.
def twtt7(tweet):
    tweet = re.sub(",+\s|\.+\"?|!+|;+\s|:+\s|\?+|n't|'\w+|'|\s\(|\)\s|_+|\s\*|\*\s", myRepl, tweet)
    return tweet.replace("  ", " ")

# Each token is tagged with its part-of-speech.
def twtt8(tweet):
    twt = ""
    s = tweet.split("\n")
    sent = []
    for sentence in s:
        sent.append(sentence.strip())
    for item in sent:
        words = item.split(" ")
        tags = tagger.tag(words)
        for i in range(len(words)):
            twt += words[i] + "/" +tags[i] + " "
        twt += "\n"
    return twt

# Before each tweet is demarcation `<A=#>', which occurs on its own line, where # is the numeric class of the tweet (0 or 4).
def twtt9(tweet, pol):
    tweet = re.sub("\s/\w+", "", tweet)
    return "<A=" + pol + "> \n" + tweet

#reading revelant tweets depending on stu number
def get_stuTweets(in_f, stu_Num):
    fileToProcess = ''
    start = (int(stu_Num) % 80) * 10000
    end = start + 10000
    start2 = start + 800000
    end2 = start2 + 10000
    f = open(in_f)
    trunkedFile = open("trunkedFile", "w+")
    lc = 0
    for line in f:
        lc += 1
    if lc >= 1600000:
        for i in range(start, end):
            trunkedFile.write(linecache.getline(in_f, i))
        for i in range(start2, end2):
            trunkedFile.write(linecache.getline(in_f, i))
        fileToProcess = "trunkedFile"
    else:
        fileToProcess = str(in_f)
    f.close()
    trunkedFile.close()
    return fileToProcess

# twtt takes an input file, student id number, and the name of the output file.
def twtt(in_f, stu_ID, out_f):
    fielToProcess = get_stuTweets(in_f, stu_ID)
    f = open(fielToProcess)
    csv_f = csv.reader(f)
    outfile = open(out_f, "w")
    for line in csv_f:
	# processing each tweet
        twt_pol = get_pol(line)
        raw_tweet = get_rawTweet(line)
        rt1 = twtt1(raw_tweet)
        rt2 = twtt2(rt1)
        rt3 = twtt3(rt2)
        rt4 = twtt4(rt3)
        rt5 = twtt5(rt4)
        rt7 = twtt7(rt5)
        rt8 = twtt8(rt7)
        rt9 = twtt9(rt8, twt_pol)
        outfile.write(rt9)
    f.close()    
    outfile.close()
    
if __name__ == '__main__':
    twtt(sys.argv[1], sys.argv[2], sys.argv[3])
