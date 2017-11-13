# -*- coding: utf-8 -*-
import pandas as pd
import re
import numpy as np
from keras.utils import np_utils

def get_sequences(s,length):
  for i in range(len(s)-length+1):
    yield [s[i+j] for j in range(length)]

def process(seq_length):
  df = pd.read_csv('data/horoscopes.csv',sep='|',names=['ind','horo','date','sign'])
  patterns = [("’s"," 's"),("’ve"," 've"),("n’t"," n't"),("’re"," 're"),("’d"," 'd"),("’ll"," 'll"),(","," , "),("!"," ! "),("\("," ( "),("\)"," ) "),("\?"," ? "),("\."," . "),(":"," : "),('"',' " ')]
  sequences = []
  words = set([])
  next_words = []
  for idx,row in df.iterrows():
    s = row['horo']
    if type(s) == type('.'):
      for p in patterns:
        s = re.sub(p[0],p[1],s)
      s = s.lower().split()
      s.insert(0,'_S_')
      ends = []
      for i in range(len(s)):
        if s[i] == '.':
          ends.append(i)
      for e in reversed(ends):
        s.insert(e+1,'_E_')
        s.insert(e+2,'_S_')
      for seq in get_sequences(s[:-1],seq_length):
        sequences.append(seq[:-1])
        next_words.append(seq[-1])
        words = words.union(set(s))
      
  print('words: ',len(words))
  print('seqs: ',len(sequences))
  word_to_idx = dict((c,i) for i,c in enumerate(words))
  idx_to_word = dict((i,c) for i,c in enumerate(words))
  print('seq length',seq_length)
  
  for i in range(len(sequences)):
    for j in range(len(sequences[i])):
      sequences[i][j] = word_to_idx[sequences[i][j]]
    next_words[i] = word_to_idx[next_words[i]]
  X = np.reshape(sequences,(len(sequences),seq_length-1,1))
  X = X / len(words)
  y = np_utils.to_categorical(next_words)
  return (X,y,sequences,next_words,words,word_to_idx,idx_to_word)

