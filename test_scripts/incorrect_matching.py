#!/usr/bin/env python
import sys

from lib import set_output_parser
from lib.frames.verb_frames.verb_frame_matcher import VerbFrameMatcher


set_output_file = open(sys.argv[1], 'r')
sentences = set_output_parser.parse(set_output_file)

f = open('../data/patterns.data', 'r')
frame_matcher = VerbFrameMatcher(f)
# frame_matcher.printFrames()

all = 0
incorrect = 0
for sentence in sentences:
    if not frame_matcher.matchFrames(sentence):
        print '\n' + str(sentence)
        for clause in sentence.clauses:
            print "<clause>"
            for phrase in clause.phrases:
                print phrase
        print
        incorrect += 1
    all += 1

print str(incorrect) + '/' + str(all)