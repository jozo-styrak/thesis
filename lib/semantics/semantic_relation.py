from lib.semantics.utils.utils import Utils

# this goes for all the classes in semantics:
# i have to think about the necessity of grouping roles into relations
# currently the reason is to connect agent and patient, to resolve coreference

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

    # return roles with specific base
    def getRolesWithBase(self, base_str):
        roles = []
        for role in self.roles:
            if base_str in role.second_level_role:
                roles.append(role)
        return roles

    # return information object
    def getInformationObject(self):
        ret_str = ''
        if self.isOutputSuitable():

            if self.getSecondLevelRole('<actor_agency:1>') != None and self.getSecondLevelRole('<actor_agency:1>').coreferent != None:
                ret_str += 'who changed recommendation/price? \n\t' + Utils.getNamedEntityString(self.getSecondLevelRole('<actor_agency:1>').coreferent) + ' / ' + str(self.getSecondLevelRole('<actor_agency:1>').coreferent) + ' {' + str(self.getSecondLevelRole('<actor_agency:1>').second_level_role) + '}\n'

            if self.getSecondLevelRole('<actor_stock:1>') != None and self.getSecondLevelRole('<actor_stock:1>').coreferent != None:
                ret_str += 'to whom? \n\t' + Utils.getNamedEntityString(self.getSecondLevelRole('<actor_stock:1>').coreferent) + ' / ' + str(self.getSecondLevelRole('<actor_stock:1>').coreferent) + ' {' + str(self.getSecondLevelRole('<actor_stock:1>').second_level_role) + '}\n'

            for recommendation in self.getRolesWithBase('state'):
                if recommendation.second_level_role == '<state_past:1>':
                    ret_str += 'past recommendation \n\t' + Utils.getRecommendationString(recommendation.phrase) + ' / ' + str(recommendation.phrase) + ' {' + str(recommendation.second_level_role) + '}\n'
                elif recommendation.second_level_role == '<state_current:1>':
                    ret_str += 'current recommendation \n\t' + Utils.getRecommendationString(recommendation.phrase) + ' / ' + str(recommendation.phrase) + ' {' + str(recommendation.second_level_role) + '}\n'

            for price in self.getRolesWithBase('price'):
                if price.second_level_role == '<price_past:1>':
                    ret_str += 'past price \n\t' + Utils.getNumberEntityString(price.phrase) + ' / ' + str(price.phrase) + ' {' + str(price.second_level_role) + '}\n'
                elif price.second_level_role == '<price_current:1>':
                    ret_str += 'current price \n\t' + Utils.getNumberEntityString(price.phrase) + ' / ' + str(price.phrase) + ' {' + str(price.second_level_role) + '}\n'
                elif price.second_level_role == '<price_change:1>':
                    ret_str += 'price change \n\t' + Utils.getNumberEntityString(price.phrase) + ' / ' + str(price.phrase)  + ' {' + str(price.second_level_role) + '}\n'

        return ret_str

    # check whether relation contains output information
    def isOutputSuitable(self):
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
