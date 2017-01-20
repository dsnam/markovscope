import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.contrib import learn
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from preproc_rnn import process
import sys,random,os

#specify a weights file to just generate without training
weight = 'weights/'+sys.argv[-1]

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
    seq = h[i:i+step]
    seqs.append(seq)
    next_words.append((h[i+step]))
print len(seqs)

X = np.zeros((len(seqs),max_len,len(words)),dtype=np.bool)
y = np.zeros((len(seqs),len(words)),dtype=np.bool)

for i,seq in enumerate(seqs):
  for j,w in enumerate(seq):
    X[i,j,word_to_idx[w]] = 1
  y[i,word_to_idx[next_words[i]]] = 1

#set up model
model = Sequential()
model.add(LSTM(256,input_shape=(max_len,len(words)),return_sequences=True))
model.add(Dropout(.2))
model.add(LSTM(256))
model.add(Dropout(.2))
model.add(Dense(y.shape[1],activation='softmax'))

if os.path.exists(weight_file):
  model.load_weights(weight_file)
  model.compile(loss='categorical_crossentropy',optimizer='adam'
else:
  fp = 'weights-{epoch:02d}-{loss:.4f}-bigger.hdf5'
  checkpoint =ModelCheckpoint(fp,monitor='loss',verbose=1,save_best_only=True,mode='min')
  callbacks_list = [checkpoint]
  model.compile(loss='categorical_crossentropy',optimizer='adam')
  model.fit(X,y,batch_size=256,nb_epoch=5,callbacks=callbacks_list)


#generate text using sequences from the data as seeds
seed = get_seed(seqs)

generated = ''
generated += ' '.join(seed)
print 'seed: ',seed
for i in range(30):
  x = np.zeros((1,max_len,len(words)))
  for t,word in enumerate(seed):
    x[0,t,word_to_idx[word]] = 1.
    preds = model.predict(x,verbose=0)[0]
    next_idx = np.argmax(preds)
    next_word = idx_to_word[next_idx]
    generated += ' '+next_word
    del seed[0]
    seed.append(next_word)
    
print generated 
