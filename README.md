# mantra-generator

Generates mantras in Sanskrit, allowing you to discover secret mantras. 

Those are not just words taken in random order: by using Markov chains we extract 
regular patterns from existing set of mantras. You can generate mantras to a specified
deity (Shiva, Kali, etc) or combine them to reach the desired effect.

It's basically just a wrapper over [markovify](https://github.com/jsvine/markovify)
with predefined text corpora and optional Devanagari romanization.

Requirements
------------

Python 3.x

Installation
------------

Install dependencies:

  - `pip install indic-transliteration`
  - `pip install markovify`

Running from the command line
-----------------------------

Run:

`python generate.py`

This will generate and print a secret mantra with default parameters. To see all possible
arguments, run `python generate.py --help`

If mantra generation is not possible with these arguments, the program will tell you about that.

Extending default mantra corpora
--------------------------------

Source corpora is kept in the `corpus` directory in `deity.txt` files. Each mantra must
be written in Devanagari Sanskrit and be each on a separate line. So you can add new
mantras to existing deity files as well as add new files. 

Please contact me directly at [yakninjayeti@gmail.com](mailto:yakninjayeti@gmail.com) to add new mantras and deities to the project.
