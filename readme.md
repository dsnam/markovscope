Markov Horoscopes
=================

An attempt to generate convincingly fake horoscopes (aka horoscopes) using
Markov Chains and a bunch of data from the NY Post. Data is about 3 years
of horoscopes for each sign and can be found in the csv file.

A bit about how these are generated: each "state" in the chain consists of two
words, as random text generation tends to produce better results when more 
preceeding words are considered. Obviously if you start to use too many you'll
just be spitting out exact copies of sentences in your data, so that needs to be avoided
The distributions of words that follow are built on a per sign basis, as
I think there are certain planets and things associated with each sign. The next word at each
step is chosen uniformly, but duplicates are allowed in the lists of available words, which weights
words appropriately according to how they are distributed in data.

If you want to generate a horoscope, make sure you have in your data folder and 
and markovscope.py and run:
```python markovscope.py <sign>```

Results vary as you would expect. Here an example that was 
actually the first one generated. Parts of it make sense, but a better model for text
generation is clearly needed.

python markovscope.py taurus
What happens over the next seven days is a very small risk. Before you 
proceed, ask yourself if you have noticed the difference. Friends and 
family will never happen. Remember too that quality is more to life in 
remarkable ways, so stop dithering and start thinking that you see it.

RNN
===

Work in progress RNN to generate text using this data. Current model is an LSTM that trains on
sequences to learn to predict words. Results so far are poor, perhaps due to how the data is being
fed in or just due to the fact that I can't realistically train on my laptop.
