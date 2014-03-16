#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

f = open(sys.argv[1].strip(),'r')
file_content = f.read().strip()

if file_content.find(sys.argv[2].strip()) != -1:
    print sys.argv[1], ' - MATCH FOUND!'
    print file_content
    print ""
else:
    print sys.argv[1], ' - NONE'