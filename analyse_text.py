#!/usr/bin/env python
''' text analysator - creates syntactic structure from set ouput with a bit of semantic information from valency frames '''
''' args: set output file, get-valency-frames output file '''
import sys

from lib import set_parser_ver02
from lib.frames.verb_frames.verb_frame_matcher import VerbFrameMatcher
from lib.frames.noun_frames.noun_frame_matcher import NounFrameMatcher
from lib.semantics.text_information import TextInformation


set_output_file = open(sys.argv[1], 'r')
sentences = set_parser_ver02.parse(set_output_file)

for sentence in sentences:
    print "\n" + str(sentence)
    for clause in sentence.clauses:
        print "<clause>"
        for phrase in clause.phrases:
            print phrase
    print

f_v = open('frames/verb.frames.02.data', 'r')
verb_matcher = VerbFrameMatcher(f_v)

f_n = open('frames/noun.frames.02.data', 'r')
noun_matcher = NounFrameMatcher(f_n)


all = 0
correct = 0
all_relations = []
for sentence in sentences:
    relations = verb_matcher.matchFrames(sentence)
    noun_relations = noun_matcher.matchFrames(sentence)
    for noun_relation in noun_relations:
        if not noun_relation in relations:
            relations.append(noun_relation)
    if relations:
        for relation in relations:
            if not relation in all_relations:
                all_relations.append(relation)
        correct += 1
    all += 1

text_information = TextInformation(all_relations, sentences)
information_objects = text_information.getTextInformation()
for inf in information_objects:
    print '***'
    print inf

print str(correct) + '/' + str(all)