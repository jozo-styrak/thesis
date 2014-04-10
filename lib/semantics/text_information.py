from lib.semantics.utils.utils import Utils

# grouping object for all the relations and roles in the text
# for now also doing coreference, ellipse and named entity resolution
class TextInformation:

    def __init__(self, relations, sentences):
        self.relations = relations
        self.sentences = sentences

    # wrapping output method
    def getTextInformation(self):

        # resolve <actor> roles
        self.resolveActorRoles()

        # apply constraints and remove invalid roles
        self.applyConstraints()

        # debug
        print '\n---------------------------------------------------'
        self.printRelations()
        print '---------------------------------------------------'

        # join relations within the same clause
        # self.preprocessRelations()

        # for now it returns just arrays with filtered phrases
        ret_objects = []

        # look over all relations
        for relation in self.relations:

            # check whether relation contains state/price information
            # what's the point?
            if relation.containsMainInformation():

                # first find agency
                # agency_role = relation.getSecondLevelRole('<actor_agency:1>')
                agency_roles = relation.getSecondLevelRoles('<actor_agency:1>')
                for agency_role in agency_roles:
                    self.findNamedEntityCoreferent(agency_role)

                    # ...then resolve stock role
                stock_roles = relation.getSecondLevelRoles('<actor_stock:1>')
                for stock_role in stock_roles:
                    self.findNamedEntityCoreferent(stock_role)

                # fill object with values from relation
                ret_objects.append(relation.getInformationObject())

        return ret_objects

    # resolve actor roles
    # currently just make them agencies
    def resolveActorRoles(self):
        for relation in self.relations:
            for role in relation.roles:
                if role.second_level_role == '<actor:1>':
                    role.second_level_role = '<actor_agency:1>'

    # apply constraints to all identified roles and delete invalid roles
    def applyConstraints(self):
        for sentence in self.sentences:
            Utils.applyConstraints(sentence)
        for relation in self.relations:
            for role in relation.roles:
                if role.invalid:
                    relation.roles.remove(role)

    # # returns candidate coreferents for given role type from text
    # # return type: Phrase
    # def getCandidateCoreferents(self, role):
    #     candidates = []
    #
    #
    #
    #     # create order of sentences
    #     sentence_order = []
    #     sentence_order.append(current)
    #     # previous sentences in reversed order
    #     for sentence in previous[::-1]:
    #         sentence_order.append(sentence)
    #     # next sentences in normal order
    #     for sentence in next:
    #         sentence_order.append(sentence)
    #
    #
    #     # get possible candidates from given order
    #     for sentence in sentence_order:
    #         for clause in sentence.clauses:
    #             for phrase in clause.phrases:
    #                 phrase_role = phrase.hasRole(role.second_level_role)
    #                 if phrase_role and phrase_role.filledWithNE():
    #                     candidates.append(phrase)
    #
    #     return candidates

    # new coreference resolution method
    # slightly changed algorithm & returns just one item
    def getCoreferent(self, role):
        coreferent_phrase = None

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
                if phrase_role and phrase_role.filledWithNE():
                    coreferent_phrase = clauses[i].phrases[j]
                j += 1
            i += 1

        return coreferent_phrase


    # wrapping method for resolution
    def findNamedEntityCoreferent(self, role):
        if role != None:
            if not role.filledWithNE():
                # new version, returns just one
                role.coreferent = self.getCoreferent(role)

    # debug method
    def printRelations(self):
        for relation in self.relations:
            print relation
