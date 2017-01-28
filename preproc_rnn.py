# -*- coding: utf-8 -*-
import pandas as pd
import re
#from keras.preprocessing.text import Tokenizer

def get_sequences(s,length):
  for i in xrange(len(s)-length):
    yield [s[i+j] for j in xrange(length)]

def process(seq_length):
  df = pd.read_csv('data/horoscopes.csv',sep='|',names=['ind','horo','date','sign'])
  patterns = [("’s"," 's"),("’ve"," 've"),("n’t"," n't"),("’re"," 're"),("’d"," 'd"),("’ll"," 'll"),(","," , "),("!"," ! "),("\("," \( "),("\)"," \) "),("\?"," \? "),("\."," . "),("\s{2,}"," ")]
  sequences = []
  words = set([])
  next_words = []
  for idx,row in df.iterrows():
    s = row['horo']
    if type(s) == type('.'):
      for p in patterns:
	s = re.sub(p[0],p[1],s)
      for seq in get_sequences(s.lower().split(),seq_length):
	sequences.append(seq[:-1])
	next_words.append(seq[-1])
      words = words.union(set(s.lower().split()))
      
  print 'words: ',len(words)
  print 'seqs: ',len(sequences)
  word_to_idx = dict((c,i) for i,c in enumerate(words))
  idx_to_word = dict((i,c) for i,c in enumerate(words))
  print 'seq length',seq_length
  
  for i in xrange(len(sequences)):
    for j in xrange(len(sequences[i])):
      sequences[i][j] = word_to_idx[sequences[i][j]]
    next_words[i] = word_to_idx[next_words[i]]

  return (sequences,next_words,words,word_to_idx,idx_to_word)

