from lib.frames.frame import Frame
from lib.frames.frame_verb import FrameVerb
from lib.frames.slots import VerbSlot, CommonSlot

# class wrapping all the verb frames
class FrameMatcher:
    
    def __init__(self, frame_file):
        self.verbs = []
        self.loadFrames(frame_file)

    # loading frames from frame file - already opened file
    def loadFrames(self, frame_file):
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
        matches = False
        for clause in sentence.clauses:
            for verb in self.verbs:
                # match given verb for given clause from sentence
                if len(verb.matchClause(clause)) > 0:  # if at least one match was found, return True
                    matches = True
                verb.resetFrames()
        return matches

    def printFrames(self):
        for verb in self.verbs:
            print verb