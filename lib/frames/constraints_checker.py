import re

# utility class to check if roles are relevant for given phrases
# note: checking for actor for now doesn't have sense, because the role can contain pronouns, general nouns, ...
class ConstraintsChecker:

    def __init__(self):
        # pattern to identify real numbers
        self.REAL_NUMBER_PATTERN = re.compile('[\+-]*\d+[\.,/:]*\d*')

    # apply constraints on given sentence
    def applyConstraints(self, sentence):
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
                        if not self.isRecommendationValue(phrase):
                            role.invalid = True
                    # check price values
                    elif 'price_' in role.second_level_role:
                        if not self.isPriceEntity(phrase):
                            role.invalid = True

    # check whether given phrase is named entity
    def isNamedEntity(self, phrase):
        contains = False
        for token in phrase.tokens:
            if token.value.endswith('_kA'):
                contains = True
        return contains

    def isRecommendationValue(self, phrase):
        contains = False
        for token in phrase.tokens:
            if token.value.endswith('_kR'):
                contains = True
            elif 'k5' in token.lemma:
                contains = True
        return contains

    def isPriceEntity(self, phrase):
        contains = False
        for token in phrase.tokens:
            if self.REAL_NUMBER_PATTERN.match(token.value.split('_')[0]):
                contains = True
        return contains
