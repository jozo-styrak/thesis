#!/usr/bin/env python
# -*- coding: utf-8 -*-
# module for task connected with named entity recognition
# simple pipeline
#       desamb
#         |
#         V
#        NER  (spoj zátvorky a úvodzovky/tag kA -> identifikácia menných entít, cien a doporučení (jeden cyklus?) -> spoj rovnako otagované entity za sebou -> spoj price a sufix )
#         |
#         V
# syntaktický preprocesor (urči tagy)
#         |
#         V
#        SET

import re
from lib.pipeline_utils import PipelineUtils
from lib.POS_editor import getValueFromTag, inContextAfter, inContextBefore

# definitions lists
# possible later on added loading from file
# pattern to identify real numbers
REAL_NUMBER_PATTERN = re.compile('[\+-]*\d+[\.,/:]*\d*')
# price follow
NUM_FOLLOW = ['KČ', 'Kč', '%', 'euro', 'USD', 'mil', 'tis', 'PLN', 'NOK', 'HUN', 'GBP', 'AUD', 'JPY', 'CHF', 'RUB', 'eur', 'dolar', 'jen', 'CZK', 'czk', 'zloty', 'zlotý', 'b.']
# recommendation strings
RECOMMENDATIONS = ['nákup', 'prodej', 'prodávat', 'držet', 'koupit', 'kupovat', 'redukovat', 'akumulovat', 'prodat', 'strong', 'buy', 'strong_buy', 'hold', 'sell', 'neutral', 'market', 'perform', 'underperform', 'underweight', 'accumulate', 'outperform', 'swap', 'overweight', 'reduce', 'equalweight', 'nadvážit', 'podvážit', 'market_perform']
# recommendation PREFIX
RECOMMENDATION_PREFIX = ['doporučení', 'titul', 'předchozí', 'stupeň', 'minulé']
# NER stoplist
NER_STOPWORDS = ['D']
# agencies for tag changes
AGENCIES = ['Goldman_Sachs', 'Morgan_Stanley', 'Credit_Suisse', 'Erste_Group', 'Nomura', 'Barclays']

def loadNamedEntities(f):
    entities = []
    for line in f.readlines():
        if len(line.strip()) > 0:
            entities.append(line.strip())
    return entities

# run NER on list of sentences
def executeNER(buffered_sentences):
    new_sentences = []

    # load named entities
    NAMED_ENTITES = loadNamedEntities(open('ner_data/named_entities.data', 'r'))

    # for each input sentence
    for sentence in buffered_sentences:

        # connect parenthesis and quotes
        # name 's' for brevity sake
        s = PipelineUtils.connectParenthesis(PipelineUtils.connectQuotes(sentence))

        # ner loop
        for i in range(len(s)):

            # ----- NAMED ENTITIES -----
            # check named entities list
            if s[i][0] in NAMED_ENTITES:
                s[i][2] = 'kA'
                s[i][1] = s[i][0]
                if not s[i][0] in NER_STOPWORDS + NUM_FOLLOW + RECOMMENDATIONS:
                    s[i][0] += '_ACTOR'
            # upper case first, other lower case
            elif i > 0 and s[i][0][0].isupper() and len(s[i][0]) > 2 and s[i][0][1].islower():
                s[i][1] = s[i][0]
                s[i][2] = 'kA'
                if not s[i][1] in NER_STOPWORDS + NUM_FOLLOW + RECOMMENDATIONS:
                    s[i][0] += '_ACTOR'
            # at least two upper case letters
            elif len(s[i][0]) > 1 and s[i][0].isupper():
                s[i][1] = s[i][0]
                s[i][2] = 'kA'
                if not s[i][0] in NER_STOPWORDS + NUM_FOLLOW + RECOMMENDATIONS:
                    s[i][0] += '_ACTOR'
            # first small, next upper
            elif len(s[i][0]) > 1 and s[i][0][0].islower() and s[i][0][1].isupper():
                s[i][1] = s[i][0]
                s[i][2] = 'kA'
                s[i][0] += '_ACTOR'
            # if is first and next token is '-' or ':'
            elif i == 0 and len(s) > 1 and (s[1][1] in '-:' or s[1][0].startswith('(')) and not s[0][1].lower() in ['akcie']:
                s[i][1] = s[i][0]
                s[i][2] = 'kA'
                s[i][0] += '_ACTOR'
            # if starts with ( and is upper
            elif s[i][0].startswith('('):
                s[i][1] = s[i][0]
                try:
                    if s[i][1].split('_')[0].isupper():
                        s[i][0] += '_ACTOR'
                except:
                    pass

            # ----- RECOMMENDATIONS -----
            # preposition + recommendation
            elif s[i][1].lower() in RECOMMENDATIONS and i > 0 and 'k7' in s[i-1][2]:
                s[i][1] = s[i][0]
                s[i][2] = 'kA'
                s[i][0] += '_STATE'
            # recommendation prefix + recommendation
            elif s[i][1].lower() in RECOMMENDATIONS and i > 0 and s[i-1][1].lower() in RECOMMENDATION_PREFIX:
                s[i][1] = s[i][0]
                s[i][2] = 'kA'
                s[i][0] += '_STATE'
            # 'nákupní', 'prodejní' + doporučení
            elif i + 1 < len(s) and s[i][1].lower() in ['nákupní', 'prodejní'] and s[i+1][1].lower() == 'doporučení':
                s[i][1] = s[i][0]
                s[i][2] = s[i+1][2]
                s[i][0] += '_STATE'
                s[i+1][0] += '_STATE'
            # doporučení + token with _
            elif i + 1 < len(s) and s[i][1].lower() in ['doporučení', 'titul'] and '_' in s[i+1][1]:
                s[i+1][1] = s[i+1][0]
                s[i+1][2] = 'kA'
                s[i+1][0] += '_STATE'
            # in recommendation list and last in sentence
            elif i == len(s) - 2 and s[i][0] in RECOMMENDATIONS:
                s[i][1] = s[i][0]
                s[i][2] = 'kA'
                s[i][0] += '_STATE'

            # ----- PRICE -----
            elif REAL_NUMBER_PATTERN.match(s[i][0]):
                s[i][1] = s[i][0]
                s[i][2] = 'k4'
                s[i][0] += '_PRICE'

        # add to new sentences
        new_sentences.append(connectTokens(s))

    return new_sentences

# connect tokens with same tag
def connectTokens(sentence):
    new_sentence = []
    new_sentence.append(sentence[0])
    # bug fix
    i = 1 if sentence[0][0] != '\"' else 2
    while i < len(sentence):
        # connects more tags in a row
        if isTagged(sentence[i][0]) and isTagged(new_sentence[len(new_sentence)-1][0]) and getTag(sentence[i][0]) == getTag(new_sentence[len(new_sentence)-1][0]):
            tag = sentence[i][0][sentence[i][0].rfind('_')+1:]
            new_sentence[len(new_sentence)-1][0] = new_sentence[len(new_sentence)-1][0][:new_sentence[len(new_sentence)-1][0].rfind('_')]
            new_sentence[len(new_sentence)-1][0] += '_' + sentence[i][0][:sentence[i][0].rfind('_')] + '_' + tag
            new_sentence[len(new_sentence)-1][1] += '_' + sentence[i][0][:sentence[i][0].rfind('_')]
        # connects price and sufix
        elif getTag(sentence[i-1][0]) == 'PRICE' and sentence[i][0] in NUM_FOLLOW:
            new_sentence[len(new_sentence)-1][0] = new_sentence[len(new_sentence)-1][0][:new_sentence[len(new_sentence)-1][0].rfind('_')]
            new_sentence[len(new_sentence)-1][0] += '_' + sentence[i][0] + '_PRICE'
            new_sentence[len(new_sentence)-1][1] += '_' + sentence[i][1]
        else:
            new_sentence.append(sentence[i])
        i += 1
    return new_sentence


# new method for changing tags
def changePOSTags(buffered_sentences):

    # for brevity sake
    for s in buffered_sentences:

        # if first element is abreviation, assume case 1
        if s[0][2] == 'kA':
            s[0][2] = 'k1gInSc1'
        i = 1
        while i < len(s):

            # tags for recommendations
            # change tag for recommendation if preceeded by preposition - same case
            if hasTag(s[i][1], 'STATE') and (getValueFromTag(s[i-1][2], 'k') == '7' or getValueFromTag(s[i-1][2], 'k') == '2'):
                s[i][2] = 'k1nPgIc' + getValueFromTag(s[i-1][2], 'c')
            # change tag for recommendation if preceeded by noun - from rec. synonym set - case 2
            elif hasTag(s[i][1], 'STATE') and s[i-1][1] in RECOMMENDATION_PREFIX:
                s[i][2] = 'k1nPgIc2'

            # tags for abbreviations & prices
            # change tag for kA if preceeded by preposition or adjective
            elif (s[i][2] == 'kA' and s[i][0].find('(') == -1) and (getValueFromTag(s[i-1][2], 'k') == '7' or getValueFromTag(s[i-1][2], 'k') == '2'):
                s[i][2] = 'k1nPgIc' + getValueFromTag(s[i-1][2], 'c')
            # change tag for kA if preceeded noun - genitiv case (in order to be included in same noun phrase)
            # if succeeded by verb, ignore - it is case, when kA splits PP and VP and has function of subject
            elif s[i][2] == 'kA' and getValueFromTag(s[i-1][2], 'k') == '1' and inContextAfter(i, s, 1, 'k5') == None:
                s[i][2] = 'k1nPgIc2'
            # change tag for abreviation if preceeded by ; or : to case 1
            elif s[i][2] == 'kA' and s[i-1][0] in ';:':
                s[i][2] = 'k1nPgIc1'
            # change tag for number if preceeded by preposition or adjective
            elif s[i][2] == 'k4' and (getValueFromTag(s[i-1][2], 'k') == '7' or getValueFromTag(s[i-1][2], 'k') == '2'):
                s[i][2] = 'k1nPgIc' + getValueFromTag(s[i-1][2], 'c')
            # if k4 is preceeded by noun, then (as with noun kA) set case to c2
            elif s[i][2] == 'k4' and getValueFromTag(s[i-1][2], 'k') == '1':
                s[i][2] = 'k1nPgIc2'
            # change tag for positive number, when isn't preceeded by preposition or adjective - apriori assume c1
            elif s[i][0].isdigit() and not (getValueFromTag(s[i-1][2], 'k') == '7' or getValueFromTag(s[i-1][2], 'k') == '2'):
                if int(s[i][0]) > 1:
                    s[i][2] = 'k4nPxCgIc1'
                else:
                    s[i][2] = 'k4nSxCgIc1'
            # change tag for word 'jeden'
            elif s[i][1] == 'jeden' and getValueFromTag(s[i][2], 'c') != '1':
                verb = inContextAfter(i, s, 3, 'k5')
                if verb != None:
                    if inContextAfter(i, s, 3, 'c1') == None:
                        s[i][2] = 'k4c1'
            # if preceeds conjunction or comma (comma + pronoun too), or particle, or adverb
            # valid for abreviation and number value such as percentage, money amount, etc.
            # ridiculously long condition, should do this for every other case
            elif (s[i][2] == 'kA' or (s[i][2] == 'k4' and not '(' in s[i][0])) and (getValueFromTag(s[i-1][2], 'k') == '8' or getValueFromTag(s[i-1][2], 'k') == '9' or getValueFromTag(s[i-1][2], 'k') == '6' or getValueFromTag(s[i-1][2], 'k') == '5' or getValueFromTag(s[i-1][2], 'k') == '1' or s[i-1][0] == ',' or (i > 1 and s[i-2][0] == ',')):
                # if succeeded by verb
                if inContextAfter(i, s, 2, 'k5') != None:
                    verb = inContextAfter(i, s, 2, 'k5')
                    # if verb has 1 person of plural, then it is probably object
                    if getValueFromTag(verb[2], 'n') == 'P' and getValueFromTag(verb[2], 'p') == '1':
                        s[i][2] = 'k1nPgIc4'
                    # if there is subject in lookahead, then this is probably object
                    elif inContextAfter(i, s, 3, 'c1') != None:
                        s[i][2] = 'k1nPgIc4'
                    # else it probably a subject
                    else:
                        s[i][2] = 'k1nPgIc1'
                # if preceeded by verb
                elif inContextBefore(i, s, 2, 'k5') != None:
                    # there is already subject before
                    if inContextBefore(i, s, 4, 'c1') != None:
                        s[i][2] = 'k1nPgIc4'
                    # there is no subject in close neighbourhood, but the kA is one of the last characters
                    elif inContextAfter(i, s, 3, 'x.') != None:
                        s[i][2] = 'k1nPgIc4'
                    # otherwise it is probably a subject
                    else:
                        s[i][2] = 'k1nPgIc1'
                # if it is a agency then it is probably a subject
                elif s[i][0] in AGENCIES:
                    s[i][2] = 'k1nPgIc1'
                # if there is a noun before, then get the same case - conjunction case
                elif inContextBefore(i, s, 3, 'k1') != None:
                    noun = inContextBefore(i, s, 3, 'k1')
                    s[i][2] = 'k1nPgIc' + getValueFromTag(noun[2], 'c')

            i += 1
    return buffered_sentences

# small tag utility functions
def isTagged(word):
    has = False
    for tag in ['PRICE', 'STATE', 'ACTOR']:
        if tag in word:
            has = True
    return has

def getTag(word):
    if isTagged(word):
        return word[word.rfind('_')+1:]
    else:
        return None

def hasTag(word, tag):
    return word.endswith(tag)