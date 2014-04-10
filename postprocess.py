#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' post-processing script run after tagginf '''
''' replaces tags for abbreviations '''
''' adds tags to real numbers '''
''' one command line argument - file with replacement data in utf '''
import sys
import re


REAL_NUMBER_PATTERN = re.compile("^[\+-]*\d+[\.,/:]*\d*$")
EXCEPTIONS = ['komerční']

# check if abbreviation is in replacement set
def inReplacementSet(tokens, word):
    for token in tokens:
        if word == token.strip().split()[0]:
            return token
    return False

# sole argument is name of file with replacement data
if len(sys.argv) != 2:
    exit(0)
    
f = open(sys.argv[1], "r")
tokens = []
for line in f.readlines():
    #tokens.append(line.strip().split())
    tokens.append(line.strip())
    
lines = []
input_lines = sys.stdin.readlines()

if len(input_lines) != 0:
    for i in range(len(input_lines)): #line in input_lines:
        line_tokens = input_lines[i].strip().split()
        if len(line_tokens) == 3:
            replacement = inReplacementSet(tokens, line_tokens[0])
            # replaces abbreviation from abbreviation list
            if replacement != False:
                #print replacement[0].ljust((((len(replacement[0])+1)/8) + 1)*8) + replacement[1].ljust((((len(replacement[0])+1)/8) + 1)*8) + replacement[2] 
                print replacement
                # changes tag for real number
            elif REAL_NUMBER_PATTERN.match(line_tokens[0]):
                print line_tokens[0] + '\t' + line_tokens[0] + '\tk4'
                # replaces tag for every token which is upper case and at least 2 characters long
            elif line_tokens[2] != 'kA' and line_tokens[0].isupper() and len(line_tokens[0]) > 1:
                print line_tokens[0] + '\t' + line_tokens[0] + '\tkA'
                # replaces tag for every word starting upper case and with at least 3 letters and is not in exceptions
            elif i>0 and not input_lines[i-1].strip().startswith('<s') and line_tokens[0][0].isupper() and len(line_tokens[0])>2 and line_tokens[1].strip() not in EXCEPTIONS:
                print line_tokens[0] + '\t' + line_tokens[0] + '\tkA'
            else:
                print input_lines[i].strip()
        else:
            print input_lines[i].strip()
