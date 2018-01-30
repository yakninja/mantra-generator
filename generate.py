#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import glob
import re
import sys

import markovify
from indic_transliteration.xsanscript import transliterate, IAST, DEVANAGARI


class MantraText(markovify.Text):
    """
    The input text is much simpler than usual: each mantra makes a separate line of text
    and optionally ends with ॥ or ।
    """
    def sentence_split(self, text):
        delimiter = re.compile(r"[॥। ]*[\r\n]+", re.U | re.S)
        return re.split(delimiter, text)


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--deities",
                    help="use only mantras for a given deities (comma separated list)")
parser.add_argument("-l", "--list-deities", action="store_true",
                    help="print all possible deities (well, not all of them are deities) and exit")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
parser.add_argument("-n", "--no-output-test", action="store_false",
                    help="allow the output to be very similar to source mantras. By default it's "
                         "not the case and the output mantra will not overlap the source too much. But for some very " 
                         "short corpora the generation without this flag will " 
                         "not be possible or will give extremely boring results")
parser.add_argument("-m", "--min", type=int, default=40,
                    help="minimum character count for mantra (default 40)")
parser.add_argument("-x", "--max", type=int, default=140,
                    help="maximum character count for mantra (default 140)")
parser.add_argument("-s", "--state-size", type=int, default=2,
                    help="set Markov state size (default 2)")
parser.add_argument("-t", "--tries", type=int, default=10,
                    help="tries to generate mantra (default 10)")
parser.add_argument("-f", "--format", type=str, default='IAST', choices=['IAST', 'DEVANAGARI'],
                    help="output format (default is IAST)")
parser.add_argument("-c", "--count", type=int, default=1,
                    help="count of mantras to generate (default 1). Each mantra will start from a new line")
parser.add_argument("-w", "--words", type=int, default=0,
                    help="count of words per mantra. Will try to generate it using --tries count, so set "
                    "larger number in --tries if you can't get desired number of words")

args = parser.parse_args()

deities = None
if args.deities:
    deities = args.deities.split(',')

models = []
for filename in glob.glob("corpus/*.txt"):
    deity = filename[7:][:-4]
    if args.list_deities:
        print(deity)
        continue
    if (deities is None) or (deity in deities):
        if args.verbose:
            print('Loaded deity file:', filename)
        with open(filename) as f:
            models.append(MantraText(f.read(), state_size=args.state_size))

if args.list_deities:
    sys.exit(0)

if len(models) == 0:
    print('Error: no deities selected for generation')
    sys.exit(1)

model = markovify.combine(models)

for i in range(args.count):
    if args.words > 0:
        word_tries = args.tries
    else:
        word_tries = 1

    mantra = None
    for k in range(word_tries):
        mantra = model.make_short_sentence(min_chars=args.min, max_chars=args.max, tries=args.tries, test_output=args.no_output_test)
        if args.words == 0:
            break
        if len(mantra.split()) == args.words:
            break
        mantra = None

    if mantra is None:
        print('Error: could not generate mantra with given constraints')
        sys.exit(1)

    if args.format == 'IAST':
        mantra = transliterate(mantra, DEVANAGARI, IAST)

    print(mantra)

