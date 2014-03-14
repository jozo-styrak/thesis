#!/usr/bin/env python
''' text analysator - creates syntactic structure from set ouput with a bit of semantic information from valency frames '''
''' args: set output file, get-valency-frames output file '''
from lib import set_parser_ver02
from lib.frames.frame_matcher import FrameMatcher
import sys

    
set_output_file = open(sys.argv[1], 'r')
sentences = set_parser_ver02.parse(set_output_file)

for sentence in sentences:
    print "\n" + str(sentence)
    for clause in sentence.clauses:
        print "<clause>"
        for phrase in clause.phrases:
            print phrase
    print

f = open('data/patterns.data', 'r')
frame_matcher = FrameMatcher(f)
# frame_matcher.printFrames()

print '************************* MATCHING FRAMES *************************************************'

all = 0
correct = 0
for sentence in sentences:
    if frame_matcher.matchFrames(sentence):
        print sentence
        print
        correct += 1
    all += 1

print str(correct) + '/' + str(all)