# -*- coding: utf-8 -*-

import re

# utility class to check if roles are relevant for given phrases
# also output methods
# note: checking for actor for now doesn't have sense, because the role can contain pronouns, general nouns, ...
class Utils:

    # apply constraints on given sentence
    @staticmethod
    def applyConstraints(sentence):
        for clause in sentence.clauses:
            for phrase in clause.phrases:
                for role in phrase.semantic_roles:
                    # check for recommendation value roles
                    if 'state_' in role.second_level_role:
                        if not Utils.isRecommendationValue(phrase):
                            role.invalid = True
                    # try to expand role
                    elif role.second_level_role == '<state:1>':
                        if Utils.isRecommendationValue(phrase):
                            if 'c2' in phrase.tokens[0].tag:
                                role.second_level_role = '<state_past:1>'
                            else:
                                role.second_level_role = '<state_current:1>'
                        else:
                            role.invalid = True
                    # check price values
                    elif 'price_' in role.second_level_role:
                        if not Utils.isPriceEntity(phrase):
                            role.invalid = True
                    # try to expand role
                    elif role.second_level_role == '<price:1>':
                        if Utils.isPriceEntity(phrase):
                            if phrase.tokens[0].value == 'o' or phrase.containsSequence('%'):
                                role.second_level_role = '<price_change:1>'
                            elif 'c2' in phrase.tokens[0].tag:
                                role.second_level_role = '<price_past:1>'
                            else:
                                role.second_level_role = '<price_current:1>'
                        else:
                            role.invalid = True

    # check whether given phrase is named entity
    @staticmethod
    def isNamedEntity(phrase):
        contains = False
        for token in phrase.tokens:
            if token.value.endswith('_ACTOR'):
                contains = True
        return contains

    @staticmethod
    def isRecommendationValue(phrase):
        contains = False
        for token in phrase.tokens:
            if token.value.endswith('_STATE'):
                contains = True
        return contains

    @staticmethod
    def isPriceEntity(phrase):
        contains = False
        for token in phrase.tokens:
            if token.value.endswith('_PRICE'):
                contains = True
        return contains

    @staticmethod
    def getNamedEntityString(phrase):
        value = ''
        for token in phrase.tokens:
            if token.value.endswith('ACTOR'):
                value += token.value[:-6].replace('_', ' ') + ' '
        return value.strip()

    # returns all named entities contained in phrase tokens as string representations
    @staticmethod
    def getNamedEntities(phrase):
        entity_list = []
        # extract actors
        for token in phrase.tokens:
            if token.value.endswith('ACTOR'):
                entity_list.append(token.value[:-6])
        return entity_list

    # returns all named entities contained in phrase tokens as string representations
    @staticmethod
    def getNumberEntityString(phrase):
        value = ''
        for token in phrase.tokens:
            if token.value.endswith('PRICE'):
                value = token.value[:-6].replace('_', ' ')
        return value

    @staticmethod
    def getRecommendationString(phrase):
        value = ''
        for token in phrase.tokens:
            if token.value.endswith('STATE'):
                value = token.value[:-6].replace('_', ' ')
            elif 'mF' in token.tag:
                value = token.lemma
        return value

    # get price change information from kA string
    @staticmethod
    def extractPriceChange(entity_str):
        PRICE_CHANGE_PATTERN = re.compile('([-+][0-9]+[,\.]*[0-9]*\ [^\)\(]*)')
        changes = PRICE_CHANGE_PATTERN.findall(entity_str)
        if len(changes) == 0:
            return None
        else:
            return changes[0]

    # whether given stock title is an abbreviation - (TWTR), (OPL)
    @staticmethod
    def isStockAbbreviation(value):
        abbreviation = True
        for letter in value:
            if not letter in '( )' and not letter.isupper():
                abbreviation = False
        return abbreviation

    # returns parts of given string - name, abbreviation, price
    # return type is dictionary
    @staticmethod
    def getEntityParts(value):
        parts = {}
        try:
            # contains abbreviation?
            if '(' in value and value.endswith(')'):
                if not value.startswith('('):
                    parts['name'] = value[:value.find('(')].strip()
                parts['abbreviation'] = value[value.find('('):][1:-1].split()[0].strip()
                price_change = Utils.extractPriceChange(value[value.find('('):])
                if price_change != None:
                    parts['price change'] = price_change
            else:
                if value.isupper():
                    parts['abbreviation'] = value.strip()
                else:
                    parts['name'] = value.strip()
        except:
            parts['name'] = value
        return parts
