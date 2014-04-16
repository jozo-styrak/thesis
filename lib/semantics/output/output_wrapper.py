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
            if relation.containsMainInformation() and relation.isOutputSuitable():

                # for each stock in relation
                for stock_key in self.getStocks(relation):

                    # if there is no object with given key, create a new one
                    # before this method should be same-name-resolving
                    if not stock_key in self.output_objects.keys():
                        self.output_objects[stock_key] = {}

                    # add stock attribute
                    if not 'stock' in self.output_objects[stock_key].keys():
                        self.output_objects[stock_key]['stock'] = stock_key

                    # resolve agencies
                    agencies = self.getAgencies(relation)

                    # if there is no agency mentioned, just add to main object
                    if len(agencies) == 0:

                        # recommendation attributes
                        for recommendation in relation.getRolesWithBase('state'):
                            if recommendation.second_level_role == '<state_past:1>' and not 'past recommendation' in self.output_objects[stock_key].keys():
                                self.output_objects[stock_key]['past recommendation'] = Utils.getRecommendationString(recommendation.phrase)
                            elif recommendation.second_level_role == '<state_current:1>' and not 'current recommendation' in self.output_objects[stock_key].keys():
                                self.output_objects[stock_key]['current recommendation'] = Utils.getRecommendationString(recommendation.phrase)

                    else:

                        # create agencies attribute array
                        if not 'agencies' in self.output_objects[stock_key].keys():
                            self.output_objects[stock_key]['agencies'] = {}

                        # for each agency
                        for agency_key in agencies:

                            # add agency attr.
                            if not agency_key in self.output_objects[stock_key]['agencies'].keys():
                                self.output_objects[stock_key]['agencies'][agency_key] = {}
                                self.output_objects[stock_key]['agencies'][agency_key]['agency'] = agency_key

                            # agency recommendations
                            for recommendation in relation.getRolesWithBase('state'):
                                if recommendation.second_level_role == '<state_past:1>': #and not 'past recommendation' in self.output_objects[stock_key]['agencies'][agency_key].keys():
                                    self.output_objects[stock_key]['agencies'][agency_key]['past recommendation'] = Utils.getRecommendationString(recommendation.phrase)
                                elif recommendation.second_level_role == '<state_current:1>': #and not 'current recommendation' in self.output_objects[stock_key]['agencies'][agency_key].keys():
                                    self.output_objects[stock_key]['agencies'][agency_key]['current recommendation'] = Utils.getRecommendationString(recommendation.phrase)

                            # price set by agency
                            price = relation.getSecondLevelRole('<price_current:1>')
                            if price != None and not 'current price' in self.output_objects[stock_key]['agencies'][agency_key].keys():
                                self.output_objects[stock_key]['agencies'][agency_key]['current price'] = Utils.getNumberEntityString(price.phrase)

                            # price set by agency
                            price = relation.getSecondLevelRole('<price_past:1>')
                            if price != None and not 'past price' in self.output_objects[stock_key]['agencies'][agency_key].keys():
                                self.output_objects[stock_key]['agencies'][agency_key]['past price'] = Utils.getNumberEntityString(price.phrase)

                    # prices in general
                    for price in relation.getRolesWithBase('price'):
                        if price.second_level_role == '<price_past:1>' and not 'past price' in self.output_objects[stock_key].keys() and len(agencies) == 0:
                            self.output_objects[stock_key]['past price'] = Utils.getNumberEntityString(price.phrase)
                        elif price.second_level_role == '<price_current:1>' and not 'current price' in self.output_objects[stock_key].keys() and len(agencies) == 0:
                            self.output_objects[stock_key]['current price'] = Utils.getNumberEntityString(price.phrase)
                        elif price.second_level_role == '<price_change:1>' and not 'price change' in self.output_objects[stock_key].keys():
                            self.output_objects[stock_key]['price change'] = Utils.getNumberEntityString(price.phrase)

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

    # output objects
    def renderOutput(self):
        for output_object in self.output_objects.itervalues():
            print '\nOutput information:'
            for key in output_object.keys():
                if key != 'agencies':
                    print '\t' + key + ' : ' + output_object[key]
                else:
                    for agency_key in output_object[key].keys():
                        for sub_key in output_object[key][agency_key].keys():
                            print '\t\t' + sub_key + ' : ' + output_object[key][agency_key][sub_key]


    def renderJSON(self):
        for output_object in self.output_objects.itervalues():
            print output_object