import re

# simple module for extraction of concrete data from phrasal text, such as named entities, numbers, recommendations
class OutputFormatter:

    @staticmethod
    def getNamedEntity(phrase):
        # look for kA marker
        value = ''
        for token in phrase.tokens:
            if token.value.endswith('kA'):
                value += token.value[:-3].replace('_', ' ') + ' '
        return value.strip()

    @staticmethod
    def getNumberEntity(phrase):
        # look for number entity
        REAL_NUMBER_PATTERN = re.compile('[\+-]*\d+[\.,/:]*\d*')
        value = ''
        for token in phrase.tokens:
            if REAL_NUMBER_PATTERN.match(token.value.split('_')[0]):
                value = token.value.replace('_', ' ')
        return value


    @staticmethod
    def getRecommendation(phrase):
        value = ''
        for token in phrase.tokens:
            if token.value.endswith('kR'):
                value = token.value[:-3].replace('_', ' ')
            elif 'mF' in token.tag:
                value = token.lemma
        return value