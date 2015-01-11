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
from __builtin__ import bytearray

class BufferOffsetReader(StreamBuffer):

    def __init__(self, read_func, increment = 2048):
        """Generic implementation of StreamBuffer, don't expect performance 
        marvels!
        
        :read_func: 
            function reading from your stream with signature
            read(bytearray buffer, int offset, int count) -> int bytes_read
            with *buffer* the buffer to read to, *offset* the first index in
            buffer to read to and *count* the maximum number of bytes to read,
            but read **at least** one byte.  
        :increment: amount of bytes to increase buffer size with when running
            out of space
        """
        super(BufferOffsetReader, self).__init__()
        self._read = read_func  
        self._incr = increment  # buffer size increment
        self._size = 0           # size of buffer contents
        # buffer[0] == start of contents always
        self._buff = bytearray(increment) 

    def get_buffer(self):
        """ Returns a reference to the buffer array."""
        return self._buff
    
    def size(self):
        """ Size of buffer contents (not the buffer array length)."""
        return self._size
    
    def read(self):
        """ Reads from the input stream into the buffer array.
            Returns the number of bytes read (at least one) or a negative number 
            to indicate the stream is at end of file 
            or this object is in an inconsistent buffer state."""
        # assert space left in buffer
        rem = len(self._buff) - self._size
        if rem == 0: self._increase_buffer()
        elif rem < 0: return -1 # inconsistent buffer state
        
        result = -1
        try:
            result = self._read(self._buff, self._size, rem)
        except: 
            print "error in read()"
            raise
        
        if (result > 0): self._size += result
        return result
    
    def _increase_buffer(self):
        inc_buf = bytearray(len(self._buff)+self._incr)
        inc_buf[0:len(self._buff)] = self._buff
        self._buff = inc_buf


class BufferReader(BufferOffsetReader):
    """Convenience subclass to enable use of Python's frequent no-offset
    read functions. Just a thin wrapper to BufferOffsetReader to respect
    the offset at the expense of performance as it requires an extra buffer copy
    operation."""

    def f(self, buff, offs, maxi): 
        buf = bytearray(maxi)
        result = self._read_f(buf, maxi)
        if result > 0:
            buff[offs:offs+result] = buf[:result] # copy to offset
        return result

    def __init__(self, read_func, increment = 2048):
        """Generic implementation of StreamBuffer, don't expect performance 
        marvels!
        
        :read_func: 
            function reading from your stream with signature
            read(bytearray buffer, int count) -> int bytes_read
            with *buffer* the buffer to read to, and *count* the maximum number 
            of bytes to read.
            Must read **at least** one byte. Returns the number of bytes read,
            or a negative number to indicate end of stream or an error.
        :increment: amount of bytes to increase buffer size with when running
            out of space
        """
        super(BufferReader, self).__init__(self.f, increment)
        self._read_f = read_func


def main():
    pass

if __name__ == '__main__':
    main()

