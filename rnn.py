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
weight_file = 'weights/'+sys.argv[-1]

#specify sequence length
seq_length = 10

def sample(a,temp=1.0):
  a = np.log(a) / temp
  a = np.exp(a) / np.sum(np.exp(a))
  return np.argmax(np.random.multinomial(1,a,1))

def get_seed(seqs):
  return seqs[random.randint(0,len(seqs))]

def data_gen(batch_size):
  X = np.zeros((batch_size,seq_length-1,len(words)))
  y = np.zeros((batch_size,len(words)))
  batch = 0
  for i in xrange(len(sequences)):
    batchIdx = i%batch_size
    X[batchIdx] = sequences[i]
    y[batchIdx] = next_words[i]
    if batchIdx == 0 and i != 0:
      batch += 1
      print 'batch:',batch
      yield (X,y)

#process the data
sequences,next_words,words,word_to_idx,idx_to_word = process(seq_length)
sequences = sequences[:500001]
next_words = next_words[:50000]
#data_gen(1).next()
#set up model
model = Sequential()
model.add(LSTM(256,input_shape=(seq_length-1,len(words)),return_sequences=True))
model.add(Dropout(.2))
model.add(LSTM(256))
model.add(Dropout(.2))
model.add(Dense(len(words),activation='softmax'))

if os.path.exists(weight_file):
  model.load_weights(weight_file)
  model.compile(loss='categorical_crossentropy',optimizer='adam')
else:
  fp = 'weights-{epoch:02d}-{loss:.4f}-bigger.hdf5'
  checkpoint = ModelCheckpoint(fp,monitor='loss',verbose=1,save_best_only=True,mode='min')
  callbacks_list = [checkpoint]
  model.compile(loss='categorical_crossentropy',optimizer='adam')
  model.fit_generator(data_gen(500),samples_per_epoch=len(sequences),nb_epoch=5,callbacks=callbacks_list)


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
