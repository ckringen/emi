#!/usr/bin/env python

import sys
import unicodedata

def sanitize(c):
    category = unicodedata.category(c)[0]
    if category == 'C': # remove control characters
        return ' '
    if category == 'Z': # replace all spaces by normal ones
        return ' '
    return c

#sys.setdefaultencoding("utf-8")
for line in sys.stdin:
    #try:
        line = line.decode('utf-8', 'ignore')
        line = unicodedata.normalize('NFC', line)
        line = u"".join(map(sanitize, line))
        sys.stdout.write("%s\n" % line.encode('utf-8'))
    #except:
    #    pass

