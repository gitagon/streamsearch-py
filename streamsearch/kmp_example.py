#!/usr/bin/env python

# Copyright 2014-2015 @gitagon. For alternative licenses contact the author.
# 
# This file is part of streamsearch-py.
# streamsearch-py is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# streamsearch-py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with streamsearch-py.  If not, see <http://www.gnu.org/licenses/>.


from streamsearch.matcher_kmp import MatcherKMP
from streamsearch.buffer_reader import BufferReader

class StringReader():
    """for testing"""
    def __init__(self, string):
        self.s = string
        self.i = 0

    def read(self, buf, cnt):
        if self.i >= len(self.s): return -1
        r = self.s[self.i]
        buf[0] = r
        result = 1
        print "read @%s" % self.i, chr(r), "->", result
        self.i+=1
        return result
    
def main():
    """for testing."""
    
    w = bytearray("abbab")
    print "pattern of length %i:" % len(w), w
    s = bytearray("aabbaabbabababbbc")
    print "text:", s
    m = MatcherKMP(w)
    r = StringReader(s)
    b = BufferReader(r.read, 200)
    m.find(b)
    print "found:%s, pos=%s " % (m.found(), m.get_index())
    

if __name__ == '__main__':
    main()

