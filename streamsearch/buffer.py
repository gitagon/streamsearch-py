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


class StreamBuffer(object):

    def __init__(self):
        super(StreamBuffer, self).__init__()

    def get_buffer(self):
        """ Returns the buffer array (possibly just a shallow reference)."""
        raise NotImplementedError()
    
    def size(self):
        """ Size of buffer contents (not the buffer array length)."""
        raise NotImplementedError()
    
    def read(self):
        """ Reads from the input stream into the buffer array.
            Returns the number of bytes read (at least one) or a negative number 
            to indicate the stream is at end of file 
            or this object is in an inconsistent buffer state."""
        raise NotImplementedError()
