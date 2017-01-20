# -*- coding: utf-8 -*-
import pandas as pd
import re
import math
#from keras.preprocessing.text import Tokenizer

def horo_generator(df):
  for t in df['horo'].iteritems():
    yield t[1]

def process():
  df = pd.read_csv('horoscopes.csv',sep='|',names=['ind','horo','date','sign'])
  patterns = [("’s"," 's"),("’ve"," 've"),("n’t"," n't"),("’re"," 're"),("’d"," 'd"),("’ll"," 'll"),(","," , "),("!"," ! "),("\("," \( "),("\)"," \) "),("\?"," \? "),("\."," . "),("\s{2,}"," ")]
  horos = []
  words = set([])
  for s in horo_generator(df):
    if type(s) == type('.'):
      for p in patterns:
	s = re.sub(p[0],p[1],s)
      horos.append(s.lower().split())
      words = words.union(set(s.lower().split()))
      #print set(s.lower().split())
      #print words
  words.union(set(['=']))
  print 'words: ',len(words)
  print 'horos: ',len(horos)
  #df['horo'] = df['horo'].str.replace(p[0],p[1])
  #df['horo'] = df['horo'].str.strip()
  word_to_idx = dict((c,i) for i,c in enumerate(words))
  idx_to_word = dict((i,c) for i,c in enumerate(words))
  max_len = max(len(h) for h in horos)-1
  #print 'max_len: ',max_len
  for h in horos:
    while len(h) < max_len:
      h.append('=')
    while len(h) > max_len:
      h = h[:-1]
  max_lea = max(len(h) for h in horos)
  print 'max_len',max_len
  return (horos,words,word_to_idx,idx_to_word,max_len)

