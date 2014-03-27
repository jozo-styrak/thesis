# abstract class as ancestor for verb and noun matchers
# not much sense in this class, just as some interface
class FrameMatcher:

    # load frames of given type
    def loadFrames(self, frame_file):
        pass

    # try to match frames of given type on sentence phrases
    def matchFrames(self, sentence):
        pass