import json
from lib.semantics.utils.utils import Utils
from lib.semantics.utils.role_resolver import RoleResolver

# class for generating output
class OutputWrapper:

    def __init__(self, text_wrapper):
        # referencing text wrapper
        self.text_wrapper = text_wrapper
        # output object in form of a hash map
        # also, every object is also a hash map
        self.output_objects = {}

    # create output objects from relations in text wrapper
    def createOutputObjects(self):

        # for each relevant relation
        for relation in self.text_wrapper.relations:

            # relevancy of output
            if relation.containsMainInformation() and relation.containsSpecificInformation():

                # for each stock in relation
                for stock_str in self.getStocks(relation):

                    # try to match this stock_str on some already used
                    stock_key = stock_str
                    same_named = self.getSameNamedEntity(stock_str, self.output_objects.keys())
                    if same_named != None:
                        stock_key = same_named

                    # temp holder object
                    current = {}
                    in_hashmap = False
                    if stock_key in self.output_objects.keys():
                        in_hashmap = True
                        current = self.output_objects[stock_key]

                    # # add name or abbreviation title
                    # if Utils.isStockAbbreviation(stock_str):
                    #     if not 'stock abbreviation' in current.keys():
                    #         current['stock abbreviation'] = stock_str
                    # elif not 'stock name' in current.keys():
                    #     current['stock name'] = stock_str
                    #
                    # # add price change
                    # price_change = Utils.extractPriceChange(stock_str)
                    # if price_change != None:
                    #     current['price change'] = price_change
                    entity_parts = Utils.getEntityParts(stock_str)
                    if 'name' in entity_parts.keys() and not 'stock name' in current.keys():
                        current['stock name'] = entity_parts['name']
                    if 'abbreviation' in entity_parts.keys() and not 'stock abbreviation' in current.keys():
                        current['stock abbreviation'] = entity_parts['abbreviation']
                    if 'price change' in entity_parts.keys() and not 'price change' in current.keys():
                        current['price change'] = entity_parts['price change']

                    # resolve agencies
                    agencies = self.getAgencies(relation)

                    # if there is no agency mentioned, just add to main object
                    if len(agencies) == 0:

                        # recommendation attributes
                        for recommendation in relation.getRolesWithBase('state'):
                            if recommendation.second_level_role == '<state_past:1>' and not 'past recommendation' in current.keys():
                                current['past recommendation'] = Utils.getRecommendationString(recommendation.phrase)
                            elif recommendation.second_level_role == '<state_current:1>' and not 'current recommendation' in current.keys():
                                current['current recommendation'] = Utils.getRecommendationString(recommendation.phrase)

                    # agency mentioned
                    else:

                        # create agencies attribute array
                        if not 'agencies' in current.keys():
                            current['agencies'] = {}

                        # for each agency
                        for agency_key in agencies:

                            # add agency attr.
                            if not agency_key in current['agencies'].keys():
                                current['agencies'][agency_key] = {}
                                current['agencies'][agency_key]['agency name'] = agency_key

                            # agency recommendations
                            for recommendation in relation.getRolesWithBase('state'):
                                if recommendation.second_level_role == '<state_past:1>': #and not 'past recommendation' in current['agencies'][agency_key].keys():
                                    current['agencies'][agency_key]['past recommendation'] = Utils.getRecommendationString(recommendation.phrase)
                                elif recommendation.second_level_role == '<state_current:1>': #and not 'current recommendation' in current['agencies'][agency_key].keys():
                                    current['agencies'][agency_key]['current recommendation'] = Utils.getRecommendationString(recommendation.phrase)

                            # agency prices
                            for price in relation.getRolesWithBase('price'):
                                if price.second_level_role == '<price_past:1>' and not 'past price' in current['agencies'][agency_key].keys():
                                    current['agencies'][agency_key]['past price'] = Utils.getNumberEntityString(price.phrase)
                                elif price.second_level_role == '<price_current:1>' and not 'current price' in current['agencies'][agency_key].keys():
                                    current['agencies'][agency_key]['current price'] = Utils.getNumberEntityString(price.phrase)
                                elif price.second_level_role == '<price_change:1>' and not 'price change' in current['agencies'][agency_key].keys():
                                    current['agencies'][agency_key]['price change'] = Utils.getNumberEntityString(price.phrase)

                    # prices in general
                    for price in relation.getRolesWithBase('price'):
                        if price.second_level_role == '<price_past:1>' and not 'past price' in current.keys() and len(agencies) == 0:
                            current['past price'] = Utils.getNumberEntityString(price.phrase)
                        elif price.second_level_role == '<price_current:1>' and not 'current price' in current.keys() and len(agencies) == 0:
                            current['current price'] = Utils.getNumberEntityString(price.phrase)
                        elif price.second_level_role == '<price_change:1>' and not 'price change' in current.keys() and len(agencies) == 0:
                            current['price change'] = Utils.getNumberEntityString(price.phrase)

                    # add created new object to hashmap, if contains recommendation value
                    if not in_hashmap: #and self.addedRecommendation(current):
                        self.output_objects[stock_key] = current

        # filter output objects
        self.filterOutputObjects()

    # return agency identificators
    def getAgencies(self, relation):
        agencies = []
        agencies_phrases = relation.getSecondLevelRoles('<actor_agency:1>')
        # collect all agency phrases from given relation
        for candidate in agencies_phrases:
            if candidate.coreferent != None and Utils.isNamedEntity(candidate.coreferent) and not candidate.coreferent in agencies_phrases:
                # get named entities from given phrase
                for entity_str in Utils.getNamedEntities(candidate.coreferent):
                    # is it relevant agency string? Dfens against bugs and wrong parses
                    if RoleResolver.isRelevantAgencyEntity(entity_str) and not entity_str.replace('_', ' ') in agencies:
                        agencies.append(entity_str.replace('_', ' '))
        return agencies

    # remove output that does not contain relevant information
    def filterOutputObjects(self):
        keys = []
        for key in self.output_objects.keys():
            if not self.addedRecommendation(self.output_objects[key]):
                keys.append(key)
        for key in keys:
            self.output_objects.pop(key, None)

    # return stock identificators
    def getStocks(self, relation):
        stocks = []
        stocks_phrases = relation.getSecondLevelRoles('<actor_stock:1>')
        # collect all stock phrases from given relation
        for candidate in stocks_phrases:
            if candidate.coreferent != None and Utils.isNamedEntity(candidate.coreferent) and not candidate.coreferent in stocks_phrases:
                # get named entities from given phrase
                for entity_str in Utils.getNamedEntities(candidate.coreferent):
                    if not entity_str.replace('_', ' ') in stocks:
                        stocks.append(entity_str.replace('_', ' '))
        return stocks

    # looks through the set of keys
    # if matches one of them, information from its relation will be added to given output object
    def getSameNamedEntity(self, value, keys):
        return_key = None
        # exact match
        if value in keys:
            return_key = value
        # substring match
        elif self.isSubstring(value, keys) != None:
            return_key = self.isSubstring(value, keys)
        # there are just two stock values in whole text, one of them is full name (and added) and the second is abreviation
        else:
            # the new value is a abbreviation
            if Utils.isStockAbbreviation(value):

                # get all stock roles from text
                stock_strs = []
                for relation in self.text_wrapper.relations:
                    for role in relation.roles:
                        if role.second_level_role == '<actor_stock:1>' and role.filledWithNE() and role.coreferent != None and not Utils.getNamedEntityString(role.coreferent) in stock_strs:
                            stock_strs.append(Utils.getNamedEntityString(role.coreferent))
                # primitive check
                if len(stock_strs) == 2 and len(keys) == 1 and not Utils.isStockAbbreviation(keys[0]):
                    return_key = keys[0]

        return return_key

    # check if value is subset of some key or vice versa
    def isSubstring(self, value, keys):
        matching_key = None
        for key in keys:
            if value in key or key in value:
                matching_key = key
        return matching_key

    # check, whether newly create hashmap output object contains recommendation value
    def addedRecommendation(self, output_object):
        return 'current recommendation' in str(output_object)

    # output objects
    def renderOutput(self):
        for output_object in self.output_objects.itervalues():
            print 'Output information:'
            for key in output_object.keys():
                if key != 'agencies':
                    print '\t' + key + ' : ' + output_object[key]
                else:
                    for agency_key in output_object[key].keys():
                        for sub_key in output_object[key][agency_key].keys():
                            print '\t\t' + sub_key + ' : ' + output_object[key][agency_key][sub_key]

    def renderJSON(self):
        for key in self.output_objects.keys():
            # needed conversion for agencies keys
            json_obj = {}
            for k in self.output_objects[key].keys():
                if k != 'agencies':
                    json_obj[k] = self.output_objects[key][k]
                else:
                    json_obj['agencies'] = []
                    for agency in self.output_objects[key]['agencies'].keys():
                        json_obj['agencies'].append(self.output_objects[key]['agencies'][agency])
            print json.dumps(json_obj, ensure_ascii=False)