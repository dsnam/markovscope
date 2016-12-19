#parses the horoscope csv into a dict structred as such:
#{sign : {(word_1,word_2):[word_3_1, word_3_2,...]}}
#
#Alexander Dodson
#2016-12-15
import os
import sys
import pickle
signs = ['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces']
states = {x:{} for x in signs}
csvfile = sys.argv[-1]

def triples(s):
  for i in xrange(len(s)-2):
    yield (s[i],s[i+1],s[i+2])

with open(csvfile) as infile:
  for line in infile:
    s = line.split('|') #0 is num, 1 is horo, 2 is date, 3 is sign
    sign = s[3].rstrip()
    horo = s[1].rstrip().split()
    horo.insert(0,'_S_')
    horo.append('_E_')
    for w1,w2,w3 in triples(horo):
      k = (w1,w2)
      if k in states[sign]:
	states[sign][k].append(w3)
      else:
	states[sign][k] = [w3]
with open('states.txt','wb') as outfile:
  pickle.dump(states,outfile)
