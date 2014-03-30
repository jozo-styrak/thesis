# grouping object for all the relations and roles in the text
# for now also doing coreference, ellipse and named entity resolution
class TextInformation:

    def __init__(self, relations, sentences):
        self.relations = relations
        self.sentences = sentences

    # wrapping output method
    def getTextInformation(self):

        # for now it returns just arrays with filtered phrases
        ret_objects = []

        # look over all relations
        for relation in self.relations:

            # check whether relation contains state/price information
            if relation.containsMainInformation():

                # check whether agens or patient is omitted
                if not relation.anyRoleOmitted():

                    # fill object with values from relation
                    ret_objects.append(relation.getInformationObject())

                else:

                    # resolution
                    pass

        return ret_objects





