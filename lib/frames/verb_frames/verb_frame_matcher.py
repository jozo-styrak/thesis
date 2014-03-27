from lib.frames.verb_frames.frame import Frame
from lib.frames.verb_frames.frame_verb import FrameVerb
from lib.frames.verb_frames.slots import VerbSlot, CommonSlot
from lib.frames.frame_matcher import FrameMatcher

# class wrapping all the verb frames
class VerbFrameMatcher(FrameMatcher):
    
    def __init__(self, frame_file):
        self.verbs = []
        self.loadVerbFrames(frame_file)

    # loading frames from frame file - already opened file
    def loadVerbFrames(self, frame_file):
        for line in frame_file.readlines():
            if not line.startswith('#') and len(line.strip()) > 0:
                if line.startswith('*'):  # new verb entry
                    self.verbs.append(FrameVerb(line[1:].strip()))
                else:
                    # line contains slot tokens separated by +++
                    slots = []
                    for slot_str in line.strip().split('+++'):
                        if slot_str == 'VERB':
                            slots.append(VerbSlot())
                        else:
                            # create phrase slot
                            identificator = slot_str[:slot_str.find('(')]
                            attributes = slot_str[slot_str.find('(')+1:-1]
                            slots.append(CommonSlot(identificator, attributes))
                    self.verbs[len(self.verbs)-1].frames.append(Frame(slots))

    # try all verbal frames for given sentence
    def matchFrames(self, sentence):
        relations = []  # buffer for extracted relations for given sentence
        for clause in sentence.clauses:
            for verb in self.verbs:
                # match given verb for given clause from sentence
                for relation in verb.matchClause(clause):
                    relations.append(relation)
                verb.resetFrames()
        return relations

    # returns semantic information from given text
    def getTextInformation(self, sentences):
        pass

    def printFrames(self):
        for verb in self.verbs:
            print verb