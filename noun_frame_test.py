from lib import set_output_parser
from lib.frames.noun_frames.noun_frame_matcher import NounFrameMatcher

set_output_file = open('data/set_output_03.txt', 'r')
sentences = set_output_parser.parse(set_output_file)

f = open('frames/noun.frames.data', 'r')
matcher = NounFrameMatcher(f)

for sentence in sentences:
    matcher.matchFrames(sentence)

matcher.printFrames()