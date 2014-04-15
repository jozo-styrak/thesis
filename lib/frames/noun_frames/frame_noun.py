from lib.sentence.phrases import NPhrase
from lib.semantics.semantic_relation import SemanticRelation
from lib.semantics.semantic_role import SemanticRole
from lib.semantics.utils.utils import Utils


# abstract class for all types of noun phrase types
class FrameNoun:

    def __init__(self):
        self.complements = []
        self.role = None

    # create list of phrases from dependency tree based on given phrase
    def generateDependencyTree(self, clause, phrase):
        changed = True
        tree_phrases = clause.getDependentPhrases(phrase)
        while changed:
            changed = False
            for phr in tree_phrases:
                dependent = clause.getDependentPhrases(phr)
                for dep_phr in dependent:
                    if not dep_phr in tree_phrases:
                        changed = True
                        tree_phrases.append(dep_phr)
        return tree_phrases


    # return candidate phrases for complements for given phrase for containing clause
    def getCandidatePhrases(self, clause, phrase):
        phrases = self.generateDependencyTree(clause, phrase)
        # for phr in clause.getSucceedingPhrases(phrase):
        #     if isinstance(phr, NPhrase) and phr.dependent_on == None and phr not in phrases:
        #         phrases.append(phr)
        return phrases

    # unmatch all complements after usage
    def resetFrame(self):
        for complement in self.complements:
            complement.matched = False

    # whole matching method
    def matchClauseTokens(self, clause):
        relations = []
        for phrase in clause.phrases:

            # does any frame noun match some phrase in clause?
            # takes coordination phrases as one
            if isinstance(phrase, NPhrase) and not phrase.isInCoordination() and self.matchesPhrase(phrase) and not phrase.roleConflict(self.role):
                # relation = None
                roles = []

                # for now, if phrase is already in a relation, use this relation
                # if len(phrase.semantic_roles) > 0:
                #     relation = phrase.semantic_roles[0].getRelation()  # use first, but they're all the same

                # if clause doesn't have containing relation, create one
                if clause.containing_relation == None:
                    clause.containing_relation = SemanticRelation()
                    clause.containing_relation.containing_clause = clause

                # add semantic role to matching phrase
                # if role does not exist, create new one
                # if exists, use this one
                # and at same time tries to upgrade existing base role to specific role
                if not phrase.findRoleAndUpgrade(self.role):
                    role = SemanticRole('OBJ', self.role)
                    role.setPhrase(phrase)
                    phrase.addSemanticRole(role)
                    roles.append(role)
                # else:
                #     # use this relation
                #     relation = phrase.findRoleAndUpgrade(self.role).getRelation()

                # match complements
                for complement in self.complements:
                    if not complement.matched:
                        for phr in self.getCandidatePhrases(clause, phrase):
                            # does complement match?
                            if complement.matchPhrase(phr):
                                # does given phrase already have given role?
                                if not phr.findRoleAndUpgrade(complement.second_level_role):
                                    role = SemanticRole(complement.first_level_role, complement.second_level_role)
                                    role.setPhrase(phr)
                                    phr.addSemanticRole(role)
                                    roles.append(role)
                                # elif phr.findRoleAndUpgrade(complement.second_level_role) and relation == None:  # if given phrase already has given role, use this relation
                                #     relation = phr.findRoleAndUpgrade(complement.second_level_role).getRelation()
                                complement.matched = True
                        # if complement is obligatory, then later it has to be resolved, for now is ellipsed
                        if not complement.matched and complement.isObligatory():
                            role = SemanticRole(complement.first_level_role, complement.second_level_role)
                            roles.append(role)
                # # if there was no relation detected, create new one
                # if relation == None:
                #     relation = SemanticRelation()

                # add roles to relation
                # remove unnecessary ellipsed roles -  not in current version
                for r in roles:
                    # if not (r.phrase == None and clause.containing_relation.getSecondLevelRole(r.second_level_role) != None):
                    #     r.relation = clause.containing_relation
                    #     clause.containing_relation.addNewRole(r)
                    r.relation = clause.containing_relation
                    clause.containing_relation.addNewRole(r)

                relations.append(clause.containing_relation)
        return relations

    # abstract method
    def matchesPhrase(self, phrase):
        return False


# general type of phrase - matching of given lemma
class GeneralPhrase(FrameNoun):

    def __init__(self, noun_str):
        FrameNoun.__init__(self);
        self.nouns = []
        for noun in noun_str.split(';'):
            self.nouns.append(noun.strip())

    # whether the phrase contains one of frame nouns
    def matchesPhrase(self, phrase):
        contains = False
        for token in phrase.tokens:
            if token.lemma in self.nouns:
                contains = True
        return contains

    def __str__(self):
        ret_str = 'nouns: ' + ','.join(self.nouns) + '\nrole: ' + str(self.role) + '\ncomplements: '
        for complement in self.complements:
            ret_str += str(complement) + ' '
        return ret_str.strip()


# class for named entities in text
class NamedEntity(FrameNoun):

    def __init__(self):
        FrameNoun.__init__(self)

    def matchesPhrase(self, phrase):
        # contains = False
        # for token in phrase.tokens:
        #     if token.value.endswith('_kA'):
        #         contains = True
        # return contains
        return Utils.isNamedEntity(phrase)


# class for numbers with number follow - price, percentage,...
class NumberEntity(FrameNoun):

    def __init__(self):
        FrameNoun.__init__(self)

    def matchesPhrase(self, phrase):
        # contains = False
        # for token in phrase.tokens:
        #     if PRICE_PATTERN.match(token.value):
        #         contains = True
        # return contains
        return Utils.isPriceEntity(phrase)
