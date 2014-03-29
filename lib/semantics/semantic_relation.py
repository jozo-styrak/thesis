# this goes for all the classes in semantics:
# i have to think about the necessity of grouping roles into relations
# currently the reason is to connect agent and patient, to resolve coreference

# class representing one relation among different entities
class SemanticRelation:

    def __init__(self):
        self.roles = []

    def addNewRole(self, role):
        self.roles.append(role)
        role.relation = self

    def __str__(self):
        ret = 'Relation:\n'
        for role in self.roles:
            ret += '\t' + str(role) + '\n'
        return ret
