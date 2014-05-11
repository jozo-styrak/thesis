from lib.semantics.utils.utils import Utils
from lib.semantics.utils.role_resolver import RoleResolver
from lib.sentence.phrases import NPhrase

# grouping object for all the relations and roles in the text
# for now also doing coreference, ellipse and named entity resolution
class TextWrapper:

    def __init__(self, sentences):
        self.relations = []
        self.sentences = sentences

    # collects relations into relation list from given sentences
    def fetchRelations(self):
        for sentence in self.sentences:
            for clause in sentence.clauses:
                if clause.containing_relation != None:
                    self.relations.append(clause.containing_relation)

    # match sentences with given frame matcher object
    def matchSentences(self, frame_matcher):
        for sentence in self.sentences:
            frame_matcher.matchFrames(sentence)


    # preprocess relation
    # resolve roles, apply constraints, resolve coreferents,...
    def processRelations(self):

        # create relations list
        self.fetchRelations()

        # resolve <actor> roles
        RoleResolver.resolveActorRoles(self.relations, self.sentences)

        # apply constraints and remove invalid roles
        self.applyConstraints()

        # debug
        print '\n---------------------------------------------------'
        self.printRelations()
        print '---------------------------------------------------'

        # look over all relations
        for relation in self.relations:

            # check whether relation contains state/price information
            # what's the point?
            if relation.containsMainInformation():

                # first find agency
                # agency_role = relation.getSecondLevelRole('<actor_agency:1>')
                agency_roles = relation.getSecondLevelRoles('<actor_agency:1>')
                for agency_role in self.orderRoles(agency_roles):
                    self.findNamedEntityCoreferent(agency_role)

                    # ...then resolve stock role
                stock_roles = relation.getSecondLevelRoles('<actor_stock:1>')
                for stock_role in self.orderRoles(stock_roles):
                    self.findNamedEntityCoreferent(stock_role)

    # resolve actor roles
    # currently just make them agencies
    # unused method
    def setActorRoles(self):
        for relation in self.relations:
            for role in relation.roles:
                if role.second_level_role == '<actor:1>':
                    role.second_level_role = '<actor_agency:1>'


    # apply constraints to all identified roles and delete invalid roles
    def applyConstraints(self):
        # apply role constraints
        for sentence in self.sentences:
            Utils.applyConstraints(sentence)
        # remove invalid roles
        for relation in self.relations:
            updated_roles = []
            for role in relation.roles:
                if not role.invalid:
                    updated_roles.append(role)
            relation.roles = updated_roles

    # new coreference resolution method
    # slightly changed algorithm & returns just one item
    def getCoreferent(self, role):
        coreferent_phrase = None
        # for coord purposes
        coreferent_clause = None

        # get number of phrase - if coreferent is coordination, it will be choosen based on number
        phrase_number = role.phrase.getNumberCategory() if role.phrase != None else 0

        # sequentially add clauses to the list order
        clauses = []
        clause_found = False
        for sentence in self.sentences:
            for clause in sentence.clauses:
                # found containing clause
                if clause == role.getRelation().containing_clause:
                    clause_found = True
                    # if clause was just found and the antecedent is not a pronoun, search also current clause
                    if role.phrase == None or  (role.phrase != None and not 'k3yR' in role.phrase.tokens[0].tag):
                        clauses.insert(0, clause)
                # clause wasn't found yet, add clause at the beginning
                elif not clause_found:
                    clauses.insert(0, clause)
                # clause was found, add clause at the end
                else:
                    clauses.append(clause)

        # find coreferent
        i = 0
        while i < len(clauses) and coreferent_phrase == None:
            j = 0
            while j < len(clauses[i].phrases) and coreferent_phrase == None:
                phrase_role = clauses[i].phrases[j].hasRole(role.second_level_role)
                # newer version - search also base roles
                if not phrase_role:
                    phrase_role = clauses[i].phrases[j].hasBaseRole(role.second_level_role)
                    # update role
                    if phrase_role:
                        phrase_role.second_level_role = role.second_level_role
                if phrase_role and phrase_role.filledWithNE():
                    coreferent_phrase = clauses[i].phrases[j]
                    coreferent_clause = clauses[i]
                j += 1
            i += 1

        # if phrase is coordination and antecedent wants just one entity
        if phrase_number == 1 and isinstance(coreferent_phrase, NPhrase) and coreferent_phrase.is_coordination:
            sub_phrases = coreferent_clause.getDependentPhrases(coreferent_phrase)
            new_coreferent = None
            i = len(sub_phrases) - 1
            # find the latest NE in given coordination
            while i >= 0 and new_coreferent == None:
                if Utils.isNamedEntity(sub_phrases[i]):
                    new_coreferent = sub_phrases[i]
                i = i - 1
            if new_coreferent != None:
                coreferent_phrase = new_coreferent

        return coreferent_phrase


    # wrapping method for resolution
    def findNamedEntityCoreferent(self, role):
        if role != None:
            if not role.filledWithNE():
                # new version, returns just one
                role.coreferent = self.getCoreferent(role)

    # order roles, so that ellipsed role is at the end
    def orderRoles(self, roles):
        new_order = []
        ellipsed = []  # at the moment there should be just one, but just in case
        for role in roles:
            if role.coreferent != None:
                new_order.append(role)
            else:
                ellipsed.append(role)
        for role in ellipsed:
            new_order.append(role)
        return new_order

    # debug method
    def printRelations(self):
        for relation in self.relations:
            print relation

    # debug method
    def printActors(self):
        print '---------------------------- ACTOR ROLES ---------------------------------'
        for relation in self.relations:
            for role in relation.roles:
                if role.second_level_role.startswith('<actor') and role.filledWithNE():
                    print role
