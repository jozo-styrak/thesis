# does role need to have information about the referencing phrase/token??

# class representing semantic role which translates to verbalex roles
class SemanticRole:

    def __init__(self, first_lvl_role, second_lvl_role):
        self.first_level_role = first_lvl_role
        self.second_level_role = second_lvl_role
        # referring phrase
        self.phrase = None
        # containing relation
        self.relation = None

    def getRelation(self):
        return self.relation

    def isAgent(self):
        return self.first_level_role == 'AG'

    def isPatient(self):
        return self.first_level_role == 'PAT'

    def isEllipsed(self):
        return self.phrase == None

    def __str__(self):
        ret = 'Phrase \'' + str(self.phrase) + '\': ' if self.phrase != None else 'Ellipsed : '
        return ret + '{ ' + self.second_level_role + ' as ' + self.first_level_role + ' }'