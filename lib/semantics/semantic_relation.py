# class representing one relation among different entities
class SemanticRelation:

    def __init__(self):
        self.roles = []
        # one relation = one clause... at least for now
        self.containing_clause = None

    # add new role to this relation
    def addNewRole(self, role):
        self.roles.append(role)
        role.relation = self

    # check whether this relation contains
    def containsMainInformation(self):
        contains_pat = False
        contains_attr = False
        for role in self.roles:
            if 'state' in role.second_level_role or 'price' in role.second_level_role:
                contains_attr = True
            elif 'actor_stock' in role.second_level_role:
                contains_pat = True
        return contains_pat and contains_attr

    # check whether given role is filled with named entity
    # for actor roles
    def filledWithNE(self, role_name):
        omitted = True
        for role in self.roles:
            if role.second_level_role == role_name and role.filledWithNE():
                omitted = False
        return not omitted

    # return role by second level id
    def getSecondLevelRole(self, role_name):
        role = None
        for r in self.roles:
            if role_name == r.second_level_role:
                role = r
        return role

    # return role by second level id
    def getSecondLevelRoles(self, role_name):
        roles = []
        for r in self.roles:
            if role_name == r.second_level_role:
                roles.append(r)
        return roles

    # whether relation already has ellisped role
    def hasEllipsedRole(self, role_name):
        has = False
        roles = self.getSecondLevelRoles(role_name)
        for role in roles:
            if role.phrase == None:
                has = True
        return has

    # return roles with specific base
    def getRolesWithBase(self, base_str):
        roles = []
        for role in self.roles:
            if base_str in role.second_level_role:
                roles.append(role)
        return roles

    # check whether relation contains any specific relevant information
    def containsSpecificInformation(self):
        suitable = False
        for price in self.getRolesWithBase('price'):
            if '_' in price.second_level_role:
                suitable = True
        if suitable:
            return suitable
        else:
            for recommendation in self.getRolesWithBase('state'):
                if '_' in recommendation.second_level_role:
                    suitable = True
            return suitable

    def __str__(self):
        ret = 'Relation:\n'
        for role in self.roles:
            ret += '\t' + str(role) + '\n'
        return ret
