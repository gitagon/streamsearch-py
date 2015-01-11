streamsearch-py is a small framework to search for a given pattern in 
an input stream, supporting buffering to improve efficiency. 
In the default implementation the Knuth-Morris-Pratt (KMP) algorithm is used 
for pattern matching, but others may be used by subclassing MatcherBase.

Copyright 2014 @gitagon. For alternative licenses contact the author.

This file is part of streamsearch-py.
streamsearch-py is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

streamsearch-py is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with streamsearch-py.  If not, see <http://www.gnu.org/licenses/>.
