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


from streamsearch.buffer import StreamBuffer
from __builtin__ import TypeError

class Matcher(object):
    """To continue search after a match move position right after current match
    with set_index(match_pos+pattern_length).
    """
    def __init__(self, w):
        super(Matcher, self).__init__()
        self._pat = w;
        self._pos = 0;
        self._hit = False;

    def set_index(self, index):
        """Sets the index to start search at. 
        Returns the same object for method chaining."""
        self._pos = index
        return self
    
    def get_index(self):
        """The index of the first byte of the match, if found() returns true."""
        return self._pos
    
    def _set_found(self, found):
        self._hit = found
        
    def _reset(self):
        """Resets any internal matcher state so match() would re-start matching
        from the beginning of the pattern, starting in buffer at get_index()."""
        pass
        
    def found(self):
        """Predicate telling if a match was found. 
        If true, get_index() tells the index of the first byte of the match."""
        return self._hit
    
    def find(self, input_buffer):
        """Resets the found() predicate to false and starts search, reading from
        input stream if running out of buffer contents till the end of stream.
        If a match has been found, get_index() returns the index of the first
        matching byte in input buffer.
        :input_buffer:
            a StreamBuffer, the input buffer and its connected stream
        TODO"""
        if not isinstance(input_buffer, StreamBuffer): 
            raise TypeError("input_buffer not a StreamBuffer")
        buff = input_buffer.get_buffer()
        if self._pos < 0 or self._pos >= len(buff):
            raise IndexError('index not in buffer')
        
        self._set_found(False)
        #self._reset()
        while True:
#             print "matching"
            self.match(input_buffer)
            if self.found(): break
            r = input_buffer.read()
#             print "read:", r
            if r < 0: break # end of input stream?
    
    # 'abstract' class and thus can be AFTER use in find():
    def match(self, input_buffer):
        """Only looks for matches in the input buffer starting at get_index(),
        without reading from the buffered stream. 
        Sets the found() predicate to false, initially. 
        Sets the found() predicate to true, the getIndex() value accordingly 
        and invokes match_event() on a full match.
        :input_buffer: 
            a StreamBuffer, the input buffer and its connected stream"""
        raise NotImplementedError()
    
    def match_event(self, matchStart):
        """Override this to receive a match event, but don't forget to invoke
        super(..).match_event(matchStart) for not breaking class integrity. 
        :matchStart:
            first byte of match"""
        self._set_found(True)
        self._pos = matchStart
