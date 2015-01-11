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


from array import array

from streamsearch.matcher import Matcher
from streamsearch.buffer import StreamBuffer

class MatcherKMP(Matcher):
    """Knuth-Morris-Pratt implementation of Matcher.
    
    Helpful for implementation were:
    
    - the (German) wikipedia description for the algorithm.
    - the definition of border, prefix, etc. on W. Lang's page:
        http://www.iti.fh-flensburg.de/lang/algorithmen/pattern/kmp.htm
    - KMP algorithm reference:
        D. E. Knuth, J. H. Morris, V. R. Pratt: Fast Pattern Matching in Strings. 
        In: SIAM Journal of Computing. 6, 2, 323-350 (1977)
    
    :author: @gitagon
    """
    
    def __init__(self, patternW):
        super(MatcherKMP, self).__init__(patternW)
        x = 0
        x+=x
        tabinit = [0 for x in range(len(patternW)+1)] # use list comprehension
        self._tab = array('l', tabinit) # prefix table for the pattern
        self._patpos = 0
        self._compile()
    
    def _compile(self):
        pat = self._pat
        tab = self._tab
        n = len(pat)
        i = 0  # index of current position in pattern
        j = -1 # length of prefix under consideration
        tab[i] = j    # first table entry is always -1
        while i < n:  # do until the end of pattern has been reached
            while j >= 0 and (pat[j] != pat[i]):  
                j = tab[j]  # in case a proper prefix cannot be extended,
                            # look for a shorter one.
            
            # in this place EITHER of j=-1 OR w[i]=w[j] hold true
             
            i+=1            # for the next byte in pattern
            j+=1            # the computed prefix length (minimum: 0)
            tab[i] = j      # is entered into the prefix table
#             print i
    
    def _reset(self):
        self._patpos = 0
        
    def _set_state(self, txtpos, patpos):
        """For saving matcher state when running out of buffer."""
        self._pos = txtpos
        self._patpos = patpos
    
    def _get_state(self):
        """For restoring matcher state after a buffer fill."""
        return self._pos, self._patpos
    
    def match(self, input_buffer):
        """KMP implementation; 
        Only looks for matches in the input buffer starting at get_index(),
        without reading from the buffered stream. 
        Sets the found() predicate to false, initially. 
        Sets the found() predicate to true, the getIndex() value accordingly 
        and invokes match_event() on a full match.
        :input_buffer: 
            a StreamBuffer, the input buffer and its connected stream"""
        self._set_found(False);
        
#         print input_buffer
#         print isinstance(input_buffer, StreamBuffer)
        if not isinstance(input_buffer, StreamBuffer): 
            raise TypeError("input_buffer not a StreamBuffer")
        
        pat = self._pat
        tab = self._tab
        m = len(self._pat)
        txt = input_buffer.get_buffer()
        n = input_buffer.size()
        
        # input values:
        # - pattern pat of length m
        # - lookup array tab of length m+1 which was setup in compile()
        # - text txt of length n to be searched for a match
        # 
        # output reported via matchEvent():
        # all matches of pat in txt
        
        # k points at current position in text
        # j points at current position in pattern
        k, j = self._get_state()
#         k = self._pos    
#         j = 0

        while k < n:  # assert not at end of buffer
#             print "k, n, txt[k], pat[j]:", k, n, chr(txt[k]), chr(pat[j])
            while j >= 0 and txt[k] != pat[j]: # move pattern until
                # text and pattern match at position k,j using tab array
                j = tab[j] 
         
            k+=1        # move on in text
            j+=1        # and in pattern
         
            if j == m:  # if at end of pattern, report a match which started
                self.match_event(k - m) # m bytes earlier.
                self._set_state(k-m, j) # save state with match start position
                return # break out of loop
#                j = tab[j];      # move pattern if using a non-breaking loop

        self._set_state(k, j) # save state on match exit

