import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.contrib import learn
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Masking
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from preproc_rnn import process
import sys,random

def sample(a,temp=1.0):
  a = np.log(a) / temp
  a = np.exp(a) / np.sum(np.exp(a))
  return np.argmax(np.random.multinomial(1,a,1))

def get_seed(seqs):
  return seqs[random.randint(0,len(seqs))]

#process the data
horos,words,word_to_idx,idx_to_word,max_len = process()
step = 5
max_len = 30
#transform the data into sequences, create seq:next pairs, vectorize
next_words = []
seqs = []
for h in horos[:len(horos)/4]:
  for i in xrange(0,len(h)-max_len,step):
    seq = ' '.join(h[i:i+step])
    seqs.append(seq)
    next_words.append((h[i+step]))
print len(seqs)

X = np.zeros((len(seqs),max_len,len(words)),dtype=np.bool)
y = np.zeros((len(seqs),len(words)),dtype=np.bool)

for i,seq in enumerate(seqs):
  for j,w in enumerate(seq.split()):
    X[i,j,word_to_idx[w]] = 1
  y[i,word_to_idx[next_words[i]]] = 1

#mask = word_to_idx['=']
model = Sequential()
#model.add(Masking(mask_value=mask,input_shape=(max_len,len(words))))
model.add(LSTM(256,input_shape=(max_len,len(words))))
model.add(Dropout(.2))
model.add(Dense(y.shape[1],activation='softmax'))
model.compile(loss='categorical_crossentropy',optimizer='adam')

for it in xrange(1,300):
  print '-'*50
  print 'Iteration:',it
  model.fit(X,y,batch_size=128,nb_epoch=2)
  #model.save_weights('horoweights',overwrite=True)

  seed = ['=']
  while '=' in seed:
    seed = get_seed(seqs)
  for diversity in [0.2,.5,1.0,1.2]:
    print 'diversity:',diversity
    generated = ''
    generated += ' '.join(seed)
    print 'seed: ',seed
    sys.stdout.write(generated)
    for i in range(30):
      x = np.zeros((1,max_len,len(words)))
      for t,word in enumerate(seed):
	x[0,t,word_to_idx[word]] = 1.
	preds = model.predict(x,verbose=0)[0]
	next_idx = sample(preds,diversity)
	next_word = idx_to_word[next_idx]
	generated += next_word
	del seed[0]
	seed.append(next_word)
	sys.stdout.write(' ')
	sys.stdout.write(next_word)
	sys.stdout.flush()
