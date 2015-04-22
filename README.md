# Philogen

Philogen is a Python Flask webapp with three functions:

- **New** - Use [markov chains](http://en.wikipedia.org/wiki/Markov_chain), mostly with 2 lookback, to generate 10 sentences from text lines in the `sources` folder. Users select the best one and it is added to the database.
- **Vote** - Display 10 random entries in the database and vote on the best one, incrementing it's score.
- **Best** - Display the 500 best entries by score.

It was built as a debate resolution generator for the [Philolexian Society](http://en.wikipedia.org/wiki/Philolexian_Society) of Columbia university, based on 1,413 resolutions scraped from Philo Facebook groups.
