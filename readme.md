Markov Horoscopes
=================

An attempt to generate convincingly fake horoscopes (aka horoscopes) using
Markov Chains and a bunch of data from the NY Post. Data is about 3 years
of horoscopes for each sign and can be found in the csv file.

A bit about how these are generated: each "state" in the chain consists of two
words. Longer sequences lead to better sounding results but you also risk just reprinting what was in the data.
The distributions of words that follow are built on a per sign basis, as
I think there are certain planets and things associated with each sign. The next word at each
step is chosen uniformly, but duplicates are allowed in the lists of available words, which weights
words appropriately according to how they are distributed in the data.

If you want to generate a horoscope, make sure you have the states in your data folder and 
markovscope.py and run:
```python markovscope.py <sign>```

Results are generally pretty nonsensical, but some of the generated text does have a horoscope tone to it. Here's an example that was actually the first one generated.

python markovscope.py taurus
What happens over the next seven days is a very small risk. Before you 
proceed, ask yourself if you have noticed the difference. Friends and 
family will never happen. Remember too that quality is more to life in 
remarkable ways, so stop dithering and start thinking that you see it.

RNN
===

Since Markov Chains didn't fly so good I figured training an RNN on the same dataset might produce something interesting.

I preprocessed the data by creating sequences out of each horoscope and inserting sentence start and end tags. Then each word
gets mapped to an integer and divided by the total number of words to produce sequences of small valued inputs to feed into the
network. Currently it'll produce a decent sentence or two but then just repeat itself.
