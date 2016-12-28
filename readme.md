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

If you want to generate a horoscope, make sure you have states.txt and 
markovscope.py in the same place and run python markovscope.py <sign>

Results vary as you would expect. Here is a half decent example that was 
actually the first one generated:

python markovscope.py taurus
What happens over the next seven days is a very small risk. Before you 
proceed, ask yourself if you have noticed the difference. Friends and 
family will never happen. Remember too that quality is more to life in 
remarkable ways, so stop dithering and start thinking that you see it.
