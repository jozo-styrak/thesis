#!/usr/bin/env python
# -*- coding: utf-8 -*-
# adds <s> and </s> tags to delimit sentences
# removes empty spaces caused by errors in encodings
import sys

SENTENCE_DELIMITERS = ".!?"
DOTTED_ABBRS = ['mil', 'ml', 'b', 'tis']
ABBR_FOLLOWERS = ['Kč', ',', 'EUR', 'USD']

pre2_token = 'EOF'
pre1_token = 'EOF'

print "<s desamb=\"1\">"
for t in sys.stdin:
    token = t.strip()
    if len(token) != 0:
        if pre1_token in SENTENCE_DELIMITERS:
            # case for mBank and eBay
            if token[0].islower() and (len(token) == 1 or token[1].islower()):
                pass
            elif pre1_token is '.' and pre2_token in DOTTED_ABBRS and (token[0].islower() or token.decode("iso-8859-2").encode("utf-8") in ABBR_FOLLOWERS):
                pass # no end of sentence here!
            else:
                print "</s>"
                print "<s desamb=\"1\">"
        elif pre1_token in ['s.', 'b.'] and token[0].isupper():
            print "</s>"
            print "<s desamb=\"1\">"
        print token
        pre2_token = pre1_token
        pre1_token = token
print "</s>"