from lib.frames.frame_matcher import FrameMatcher
from lib.frames.noun_frames.frame_noun import GeneralPhrase, NamedEntity, NumberEntity, RecommendationEntity
from lib.frames.noun_frames.complement import Complement

# class handling matching of noun frames
class NounFrameMatcher(FrameMatcher):

    def __init__(self, frame_file):
        self.noun_frames = []
        self.loadFrames(frame_file)

    def loadFrames(self, frame_file):
        for line in frame_file.readlines():
            if not line.startswith('#') and len(line.strip()) > 0:
                if line.startswith('*'):  # new noun entry
                    if line.find('{ACTOR}') != -1:
                        self.noun_frames.append(NamedEntity())
                    elif line.find('{PRICE}') != -1:
                        self.noun_frames.append(NumberEntity())
                    elif line.find('{STATE}') != -1:
                        self.noun_frames.append(RecommendationEntity())
                    else:
                        self.noun_frames.append(GeneralPhrase(line[1:].strip()))

                elif line.startswith('+'):
                    # add role for given noun frame
                    self.noun_frames[len(self.noun_frames)-1].role = line.strip()[line.strip().find(':')+1:]
                else:
                    # line contains complement
                    self.noun_frames[len(self.noun_frames)-1].complements.append(Complement(line.strip()))

    # match loaded noun frames and complements on given clause - returns created relations
    def matchFrames(self, sentence):
        # relations = []
        for clause in sentence.clauses:
            for noun in self.noun_frames:
                # newer version: it is allowed to look for noun match only in sentences that:
                # 1. contain already verb frame
                # 2. doesn't contain verb
                # 3. noun frame is of named entity type (NER) or recommendation type
                if isinstance(noun, NamedEntity) or isinstance(noun, RecommendationEntity) or clause.containing_relation != None or not clause.containsVerbPhrase():
                    # for relation in noun.matchClauseTokens(clause):
                    # relations.append(relation)
                    noun.matchClauseTokens(clause)
                    noun.resetFrame()
        # return relations

    def printFrames(self):
        for noun in self.noun_frames:
            print noun