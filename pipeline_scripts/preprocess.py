#!/usr/bin/env python
# -*- coding: utf-8 -*-
# preprocessing script - run before tagging
# for now, the main function of the script is to connect few abbreviatons that have been splitted by unitok
import sys

tokens = sys.stdin.readlines()
tokens.append('EOF')

i = 1

while i < len(tokens):

    # join few abbreviations and exceptions
    if len(tokens[i].strip()) != 0:
        # abbreviation with digits at the end
        if tokens[i].strip().isdigit() and tokens[i-1].strip().isupper() and len(tokens[i-1].strip()) > 1:
            print tokens[i-1].strip() + tokens[i].strip()
            i += 2
        # ''' K+S '''
        if tokens[i].strip() == '+' and tokens[i-1].strip() == 'K' and tokens[i+1].strip() == 'S':
            print "K+S"
            i += 3
        # S&P[500]
        if tokens[i].strip() == '&' and tokens[i-1].strip() == 'S' and tokens[i+1].strip() == 'P':
            if tokens[i+2].strip().isdigit():
                print "S&P", tokens[i+2].strip()
                i += 1
            else:
                print "S&P"
            i += 3
        # ''' J&J '''
        if tokens[i].strip() == '&' and tokens[i-1].strip() == 'J' and tokens[i+1].strip() == 'J':
            print "J&J"
            i += 3
        # ''' Yahoo! '''
        if tokens[i-1].strip() == 'Yahoo' and tokens[i].strip() == '!':
            print 'Yahoo!'
            i += 2
        # join tokens split by & or '
        if tokens[i].strip() in "&\'´`":
            print tokens[i-1].strip() + tokens[i].strip() + tokens[i+1].strip()
            i += 3
        if tokens[i].strip() == '\'s' or tokens[i].strip() == '´s' or tokens[i].strip() == '`s':
            print tokens[i-1].strip() + tokens[i].strip()
            i += 2
        else:
            print tokens[i-1].strip()
            i += 1
