# this goes for all the classes in semantics:
# i have to think about the necessity of grouping roles into relations
# currently the reason is to connect agent and patient, to resolve coreference

# class representing one relation among different entities
class SemanticRelation:

    def __init__(self):
        self.roles = []

    # add new role to this relation
    def addNewRole(self, role):
        self.roles.append(role)
        role.relation = self

    # check whether this relation contains
    def containsMainInformation(self):
        contains = False
        for role in self.roles:
            if 'state' in role.second_level_role or 'price' in role.second_level_role:
                contains = True
        return contains

    # check whether any important role is omitted
    # for now, check organization roles
    def anyRoleOmitted(self):
        return self.isAgencyOmitted() or self.isStockOmitted()

    # check whether agency role is omitted
    def isAgencyOmitted(self):
        omitted = True
        for role in self.roles:
            if role.second_level_role == '<agency:1>' and role.isFilledWithNE():
                omitted = False
        return omitted

    # check whether stock role is omitted
    def isStockOmitted(self):
        omitted = True
        for role in self.roles:
            if role.second_level_role == '<stock:1>' and role.isFilledWithNE():
                omitted = False
        return omitted

    # return information object
    def getInformationObject(self):
        ret_str = 'who changed recommendation? ' + str(self.getAgencyRole().phrase) + ' {' + str(self.getAgencyRole().second_level_role) + '}\n'
        ret_str += 'to whom? ' + str(self.getStockRole().phrase) + ' {' + str(self.getStockRole().second_level_role) + '}\n'
        for recommendation in self.getRecommendationRoles():
            if recommendation.second_level_role == '<state_from:1>':
                ret_str += 'past recommendation ' + str(recommendation.phrase) + ' {' + str(recommendation.second_level_role) + '}\n'
            elif recommendation.second_level_role == '<state_to:1>':
                ret_str += 'current recommendation ' + str(recommendation.phrase) + ' {' + str(recommendation.second_level_role) + '}\n'
            else:
                ret_str += 'recommendation ' + str(recommendation.phrase) + ' {' + str(recommendation.second_level_role) + '}\n'
        for price in self.getPriceRoles():
            if price.second_level_role == '<price_from:1>':
                ret_str += 'past price ' + str(price.phrase) + ' {' + str(price.second_level_role) + '}\n'
            elif price.second_level_role == '<price_to:1>':
                ret_str += 'current price ' + str(price.phrase) + ' {' + str(price.second_level_role) + '}\n'
            else:
                ret_str += 'price ' + str(price.phrase) + ' {' + str(price.second_level_role) + '}\n'
        return ret_str

    # return agency
    def getAgencyRole(self):
        agency = None
        for role in self.roles:
            if 'agency' in role.second_level_role:
                agency = role
        return agency

    # return stock role
    def getStockRole(self):
        stock = None
        for role in self.roles:
            if 'stock' in role.second_level_role:
                stock = role
        return stock

    # return recommendation objects
    def getRecommendationRoles(self):
        recommendations = []
        for role in self.roles:
            if 'state' in role.second_level_role:
                recommendations.append(role)
        return recommendations

    # return recommendation objects
    def getPriceRoles(self):
        prices = []
        for role in self.roles:
            if 'price' in role.second_level_role:
                prices.append(role)
        return prices

    def __str__(self):
        ret = 'Relation:\n'
        for role in self.roles:
            ret += '\t' + str(role) + '\n'
        return ret
