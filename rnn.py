import numpy as np
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.contrib import learn
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Flatten
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from preproc_rnn import process
import sys,random,os

#specify a weights file to just generate without training
weight_file = sys.argv[-1]
#specify sequence length
seq_length = 4

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
  while 1:
    for i in range(len(sequences)):
      batchIdx = i%batch_size
      for j in range(seq_length-1):
        X[batchIdx,j,sequences[i][j]] = 1
      y[batchIdx,next_words[i]] = 1
      if batchIdx == 0 and i != 0:
        batch += 1
        print('batch:',batch)
        yield (X,y)

#process the data
X,y,sequences,next_words,words,word_to_idx,idx_to_word = process(seq_length)

#set up model
model = Sequential()
model.add(LSTM(256,input_shape=(X.shape[1],X.shape[2]),return_sequences=True))
model.add(Dropout(.2))
model.add(LSTM(256))
model.add(Dropout(.2))
#model.add(Flatten())
model.add(Dense(y.shape[1],activation='softmax'))

if weight_file[-4:] == 'hdf5':
  model.load_weights(weight_file)
  model.compile(loss='categorical_crossentropy',optimizer='adam')
else:
  fp = 'weights-{epoch:02d}-{loss:.4f}-bigger.hdf5'
  checkpoint = ModelCheckpoint(fp,monitor='loss',verbose=1,save_best_only=True,mode='min')
  callbacks_list = [checkpoint]
  model.compile(loss='categorical_crossentropy',optimizer='adam')
  model.fit(X,y,epochs=30,batch_size=128,callbacks=callbacks_list)


#generate text using sequences from the data as seeds
#seed = get_seed(sequences)
seed = sequences[np.random.randint(0,len(sequences)-1)]
generated = []
print('seed: ',seed)
for i in range(50):
  x = np.reshape(seed,(1,len(seed),1))
  x = x / float(len(words))
  pred = model.predict(x,verbose=0)
  idx = np.argmax(pred)
  result = idx_to_word[idx]
  generated.append(result)
  seed.append(idx)
  seed = seed[1:len(seed)]
      
print(generated)
