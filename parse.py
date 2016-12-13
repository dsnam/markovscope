import os
import sys
import json
signs = ['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces']
states = {x:{} for x in signs}
csvfile = sys.argv[-1]


def triples(s):
  for i in xrange(len(s)-2):
    yield (s[i],s[i+1],s[i+2])

#yeah this is a lazy check. don't pass bad files
if csvfile[-3:] != 'csv':
  print 'not a valid file'
else:
  with open(csvfile) as infile:
    for line in infile:
      s = line.split('|') #0 is num, 1 is horo, 2 is date, 3 is sign
      sign = s[3].rstrip()
      horo = s[1].rstrip()
      for w1,w2,w3 in triples(horo.split()):
	k = w1+','+w2
	if k in states[sign]:
	  states[sign][k].append(w3)
	else:
	  states[sign][k] = [w3]
  #print states
  with open('states.json','w') as outfile:
    json.dump(states,outfile,ensure_ascii=False)
