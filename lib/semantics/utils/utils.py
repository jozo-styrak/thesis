# -*- coding: utf-8 -*-

import re

# utility class to check if roles are relevant for given phrases
# note: checking for actor for now doesn't have sense, because the role can contain pronouns, general nouns, ...
class Utils:

    # apply constraints on given sentence
    @staticmethod
    def applyConstraints(sentence):
        for clause in sentence.clauses:
            for phrase in clause.phrases:
                for role in phrase.semantic_roles:
                    # check of actor roles
                    # may be added editing of role in case of presence of prepositions with diff. cases
                    # if 'actor' in role.second_level_role:
                    #     if not self.isNamedEntity(phrase):
                    #         role.invalid = True
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
        # EXCEPTIONS = ['komerční banka']
        # contains = False
        # for token in phrase.tokens:
        #     if token.value.endswith('_kA'):
        #         contains = True
        # if not contains:
        #     lemma_str = ''
        #     for token in phrase.tokens:
        #         lemma_str += ' ' + token.lemma.lower()
        #     for exception in EXCEPTIONS:
        #         if exception in lemma_str.strip():
        #             contains = True
        # return contains
        contains = False
        for token in phrase.tokens:
            if token.value.endswith('_ACTOR'):
                contains = True
        return contains

    @staticmethod
    def isRecommendationValue(phrase):
        # contains = False
        # for i in range(len(phrase.tokens)):
        #     if phrase.tokens[i].value.endswith('_kR'):
        #         contains = True
        #     elif 'k5' in phrase.tokens[i].tag:
        #         contains = True
        #     elif phrase.tokens[i].value.endswith('_kA') and 'k7' in phrase.tokens[0].tag:
        #         contains = True
        #     elif phrase.tokens[i].lemma == 'doporučení' and i > 0 and phrase.tokens[i-1].lemma.lower() in ['nákupní', 'prodejní']:
        #         contains = True
        # return contains
        contains = False
        for token in phrase.tokens:
            if token.value.endswith('_STATE'):
                contains = True
        return contains

    @staticmethod
    def isPriceEntity(phrase):
        # PRICE_PATTERN = re.compile('[\+-]*\d+[\.,/:]*\d*_.*')
        # contains = False
        # for token in phrase.tokens:
        #     if PRICE_PATTERN.match(token.value):
        #         contains = True
        # return contains
        contains = False
        for token in phrase.tokens:
            if token.value.endswith('_PRICE'):
                contains = True
        return contains

    @staticmethod
    def getNamedEntityString(phrase):
        # look for kA marker
        # value = ''
        # for token in phrase.tokens:
        #     if token.value.endswith('kA'):
        #         value += token.value[:-3].replace('_', ' ') + ' '
        # return value.strip()
        value = ''
        for token in phrase.tokens:
            if token.value.endswith('ACTOR'):
                value += token.value[:-6].replace('_', ' ') + ' '
        return value.strip()

    # returns all named entities contained in phrase tokens as string representations
    @staticmethod
    def getNamedEntities(phrase):
        # # there is need to join tokens in form of: name_of_org_kA (abbr_price_value)_kA into one
        # entity_list = []
        # kA_list = []
        # # extract sub kAs
        # for i in range(len(phrase.tokens)):
        #     if phrase.tokens[i].value.endswith('kA'):
        #         kA_list.append(phrase.tokens[i].value[:-3])
        #     elif phrase.tokens[i].lemma == 'banka' and i > 0 and phrase.tokens[i-1].lemma == 'komerční':
        #         kA_list.append(phrase.tokens[i-1].lemma + ' ' + phrase.tokens[i].lemma)
        # if len(kA_list) > 0:
        #     entity_list.append(kA_list[0])
        #     # join names with abbreviations
        #     for i in range(1,len(kA_list)):
        #         if kA_list[i].startswith('('):
        #             entity_list[len(entity_list)-1] += ' ' + kA_list[i]
        #         else:
        #             entity_list.append(kA_list[i])
        # return entity_list
        # there is need to join tokens in form of: name_of_org_kA (abbr_price_value)_kA into one
        entity_list = []
        # extract actors
        for token in phrase.tokens:
            if token.value.endswith('ACTOR'):
                entity_list.append(token.value[:-6])
        return entity_list

    @staticmethod
    def getNumberEntityString(phrase):
        # # look for number entity
        # REAL_NUMBER_PATTERN = re.compile('[\+-]*\d+[\.,/:]*\d*')
        # value = ''
        # for token in phrase.tokens:
        #     if REAL_NUMBER_PATTERN.match(token.value.split('_')[0]):
        #         value = token.value.replace('_', ' ')
        # return value
        # look for number entity
        value = ''
        for token in phrase.tokens:
            if token.value.endswith('PRICE'):
                value = token.value[:-6].replace('_', ' ')
        return value

    @staticmethod
    def getRecommendationString(phrase):
        # value = ''
        # for i in range(len(phrase.tokens)):
        #     if phrase.tokens[i].value.endswith('kR'):
        #         value = phrase.tokens[i].value[:-3].replace('_', ' ')
        #     elif 'mF' in phrase.tokens[i].tag:
        #         value = phrase.tokens[i].lemma
        #     elif phrase.tokens[i].lemma == 'doporučení' and i > 0 and phrase.tokens[i-1].lemma.lower() in ['nákupní', 'prodejní']:
        #         value = phrase.tokens[i-1].lemma.lower() + ' ' + phrase.tokens[i].lemma
        # return value
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
        PRICE_CHANGE_PATTERN = re.compile('([-+][0-9]*[,\.]+[0-9]*\ [^\)\(]*)')
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
