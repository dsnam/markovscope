#generates a random horoscope for a particular sign
#Alexander Dodson
#2016-12-13

import pickle
import sys
import random

sign = sys.argv[-1]
with open('states.txt') as data:
  all_states = pickle.loads(data.read())

start_states = [x for x in all_states[sign] if x[0] == '_S_']
state = random.choice(start_states)
horo = state[1]
while state:
  next_word = random.choice(all_states[sign][state])
  if next_word == '_E_':
    break
  horo = horo +' '+next_word
  state = (state[1],next_word)

print horo
