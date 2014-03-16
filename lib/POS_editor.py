#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 what to connect
    number following abbreviations to number
    abbreviations to previous token
    recommendation with previous prepositions
    multi word recommendations
    remove "
    connecting abreviations to nouns with same case - set doesn't recognize them as one phrase, therefore genitiv case
    resolve NP + abreviation + verb -> abreviation should be case 1
'''

import re


# pattern to identify real numbers
REAL_NUMBER_PATTERN = re.compile('[\+-]*\d+[\.,/:]*\d*')

# lists of words used for tag editing
NUM_FOLLOW = ['KČ', 'Kč', '%', 'euro', 'USD', 'mil', 'tis', 'PLN', 'NOK', 'HUN', 'GBP', 'AUD', 'JPY', 'CHF', 'RUB', 'eur', 'dolar']
RECOMMENDATIONS = ['držet', 'koupit', 'kupovat', 'redukovat', 'akumulovat', 'prodat', 'strong', 'buy', 'hold', 'sell', 'neutral', 'market', 'perform', 'underperform', 'underweight', 'accumulate', 'outperform', 'swap', 'overweight', 'reduce', 'equalweight']
RECOMMENDATION_SYNONYMS = ['doporučení', 'titul', 'předchozí', 'stupeň']
AGENCIES = ['Goldman_Sachs', 'Morgan_Stanley', 'Credit_Suisse', 'Erste_Group']


# simple function to get value of a marker from morphologic tag, missing tag proof
def getValueFromTag(tag, identifier):
    if tag.find(identifier) == -1:
        return 0
    else:
        return tag[tag.find(identifier)+1]

# if there is specific tag value in tokens before specified position
# returns token with given tag value combination
def inContextBefore(position, sentence, count, tag_value):
    token = None
    i = 0
    while i < count and position - i > 0 and token == None:
        i += 1
        if tag_value in sentence[position - i][2]:
            token = sentence[position - i]
    return token

# if there is specific tag value in tokens after specified position
# returns token with given tag value combination
def inContextAfter(position, sentence, count, tag_value):
    token = None
    i = 0
    while i < count and position + i + 1 < len(sentence) and token == None:
        i += 1
        if tag_value in sentence[position + i][2]:
            token = sentence[position + i]
    return token

# method for connecting objects inside parenthesis
def connectParenthesis(tokens):
    return tokens

# main function of script
# connect some tokens and edit tags
def editTags(buffered_sentences):
    new_sentences = []
    for sentence in buffered_sentences:
        new_sentence = []
        new_sentence.append(sentence[0])

        # first traverse - joining && removing
        i = 1
        while i < len(sentence):
            # skip " character
            if sentence[i][0] == "\"":
                pass
            # connects more abbreviations in a row
            elif sentence[i][2] == 'kA' and new_sentence[len(new_sentence)-1][2] == 'kA':
                new_sentence[len(new_sentence)-1][0] += '_' + sentence[i][0]
                new_sentence[len(new_sentence)-1][1] += '_' + sentence[i][1]
            # connects real number and sufix
            elif REAL_NUMBER_PATTERN.match(sentence[i-1][0]) and sentence[i][1] in NUM_FOLLOW:
                new_sentence[len(new_sentence)-1][0] += '_' + sentence[i][0]
                new_sentence[len(new_sentence)-1][1] += '_' + sentence[i][1]
            # connect number to abbreviation
            elif sentence[i][2] == 'k4' and new_sentence[len(new_sentence)-1][2] == 'kA':
                new_sentence[len(new_sentence)-1][0] += '_' + sentence[i][0]
                new_sentence[len(new_sentence)-1][1] += '_' + sentence[i][1]
            # connect ending parenthese
            # elif sentence[i][2] == 'kIx)' and (new_sentence[len(new_sentence)-1][2] == 'k4' or (new_sentence[len(new_sentence)-1][2] == 'kA' and not new_sentence[len(new_sentence)-1][1]) in RECOMMENDATIONS):
            elif sentence[i][2] == 'kIx)' and (sentence[i-1][2] == 'k4' or (sentence[i-1][2] == 'kA' and not sentence[i-1][1] in RECOMMENDATIONS) or sentence[i-1][1] in NUM_FOLLOW):
                new_sentence[len(new_sentence)-1][0] += '_' + sentence[i][0]
                new_sentence[len(new_sentence)-1][1] += '_' + sentence[i][1]
            # connect beginning parenthese
            elif new_sentence[len(new_sentence)-1][2] == 'kIx(' and (sentence[i][2] == 'k4' or sentence[i][2] == 'kA'):
                new_sentence[len(new_sentence)-1][0] += '_' + sentence[i][0]
                new_sentence[len(new_sentence)-1][1] += '_' + sentence[i][1]
                new_sentence[len(new_sentence)-1][2] = 'kA'
            else:
                new_sentence.append(sentence[i])
            i += 1

        # connect tokens inside parenthesis
        new_sentence = connectParenthesis(new_sentence)

        # second traverse - editing tags based on some rules
        # if first element is abreviation, assume case 1
        if new_sentence[0][2] == 'kA':
            new_sentence[0][2] = 'k1gInSc1'
        i = 1
        while i < len(new_sentence):
            # change tag for kA if preceeded by preposition or adjective
            if (new_sentence[i][2] == 'kA' and new_sentence[i][0].find('(') == -1) and (getValueFromTag(new_sentence[i-1][2], 'k') == '7' or getValueFromTag(new_sentence[i-1][2], 'k') == '2'):
                new_sentence[i][2] = 'k1nPgIc' + getValueFromTag(new_sentence[i-1][2], 'c')
            # change tag for kA if preceeded noun - genitiv case (in order to be included in same noun phrase)
            # commented version - abreviation of type (_EU_) doesn't connect to previous noun - not sure if that is pleasable
            # elif (new_sentence[i][2] == 'kA' and new_sentence[i][0].find('(') == -1) and getValueFromTag(new_sentence[i-1][2], 'k') == '1':
            elif new_sentence[i][2] == 'kA' and getValueFromTag(new_sentence[i-1][2], 'k') == '1':
                new_sentence[i][2] = 'k1nPgIc2'
            # change tag for kA if preceeded by verb - almost solely followed by case 1, exception: pokryvat + c4
            # elif (new_sentence[i][2] == 'kA' and new_sentence[i][0].find('(') == -1) and getValueFromTag(new_sentence[i-1][2], 'k') == '5' and new_sentence[i-1][1] != 'pokrývat':
            #     new_sentence[i][2] = 'k1nPgIc1'
            # change tag for recommendation if preceeded by preposition - same case
            elif new_sentence[i][0] in RECOMMENDATIONS and getValueFromTag(new_sentence[i-1][2], 'k') == '7':
                new_sentence[i][2] = 'k1nPgIc' + getValueFromTag(new_sentence[i-1][2], 'c')
            # change tag for recommendation if preceeded by noun - from rec. synonym set - case 2
            elif new_sentence[i][0] in RECOMMENDATIONS and new_sentence[i-1][1] in RECOMMENDATION_SYNONYMS:
                new_sentence[i][2] = 'k1nPgIc2'
            # change tag for abreviation if preceeded by ; or : to case 1
            elif new_sentence[i][2] == 'kA' and new_sentence[i-1][0] in ';:':
                new_sentence[i][2] = 'k1nPgIc1'
            # change tag for number if preceeded by preposition or adjective
            elif new_sentence[i][2] == 'k4' and (getValueFromTag(new_sentence[i-1][2], 'k') == '7' or getValueFromTag(new_sentence[i-1][2], 'k') == '2'):
                new_sentence[i][2] = 'k1nPgIc' + getValueFromTag(new_sentence[i-1][2], 'c')
            # change tag for positive number, when isn't preceeded by preposition or adjective - apriori assume c1
            elif new_sentence[i][0].isdigit() and not (getValueFromTag(new_sentence[i-1][2], 'k') == '7' or getValueFromTag(new_sentence[i-1][2], 'k') == '2'):
                if int(new_sentence[i][0]) > 1:
                    new_sentence[i][2] = 'k4nPxCgIc1'
                else:
                    new_sentence[i][2] = 'k4nSxCgIc1'
            # change tag for word 'jeden'
            elif new_sentence[i][1] == 'jeden' and getValueFromTag(new_sentence[i][2], 'c') != '1':
                verb = inContextAfter(i, new_sentence, 3, 'k5')
                if verb != None:
                    if inContextAfter(i, new_sentence, 3, 'c1') == None:
                        new_sentence[i][2] = 'k4c1'
            # if preceeds conjunction or comma (comma + pronoun too), or particle, or adverb
            elif new_sentence[i][2] == 'kA' and (getValueFromTag(new_sentence[i-1][2], 'k') == '8' or getValueFromTag(new_sentence[i-1][2], 'k') == '9' or getValueFromTag(new_sentence[i-1][2], 'k') == '6' or getValueFromTag(new_sentence[i-1][2], 'k') == '5' or new_sentence[i-1][0] == ',' or (i > 1 and new_sentence[i-2][0] == ',')):
                # if succeeded by verb
                if inContextAfter(i, new_sentence, 2, 'k5') != None:
                    verb = inContextAfter(i, new_sentence, 2, 'k5')
                    # if verb has 1 person of plural, then it is probably object
                    if getValueFromTag(verb[2], 'n') == 'P' and getValueFromTag(verb[2], 'p') == '1':
                        new_sentence[i][2] = 'k1nPgIc4'
                    # if there is subject in lookahead, then this is probably object
                    elif inContextAfter(i, new_sentence, 3, 'c1') != None:
                        new_sentence[i][2] = 'k1nPgIc4'
                    # else it probably a subject
                    else:
                        new_sentence[i][2] = 'k1nPgIc1'
                # if preceeded by verb
                elif inContextBefore(i, new_sentence, 2, 'k5') != None:
                    if inContextBefore(i, new_sentence, 4, 'c1') != None:
                        new_sentence[i][2] = 'k1nPgIc4'
                    else:
                        new_sentence[i][2] = 'k1nPgIc1'
                # if it is a agency then it is probably a subject
                elif new_sentence[i][0] in AGENCIES:
                    new_sentence[i][2] = 'k1nPgIc1'
                # if there is a noun before, then get the same case
                elif inContextBefore(i, new_sentence, 3, 'k1') != None:
                    noun = inContextBefore(i, new_sentence, 3, 'k1')
                    new_sentence[i][2] = 'k1nPgIc' + getValueFromTag(noun[2], 'c')

            i += 1
        new_sentences.append(new_sentence)
    return new_sentences
