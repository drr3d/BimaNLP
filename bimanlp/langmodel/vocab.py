########################## This file is part of BimaNLP. ############################
# BimaNLP is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# BimaNLP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#####################################################################################

class SimpleVocab(object):
    # Pada dasarnya Vocab(vocabulary) berisi kumpulan seluruh kata pada suatu document
    #   kata yang masuk didalam vocab sudah bersifat distinct yang berarti tidak akan ada perulangan,
    #   e.g: doc = 'saya akan makan nasi dan akan makan telor'
    #           maka Vocab untuk doc diatas adalah
    #        Voc = 'saya', 'akan', 'makan', 'nasi', 'dan', 'telor'
    #        Idx =   0,      1,       2,       3,     4,      5
    
    # Isi Vocab:
    # word, 'count' of word, position 'index', sample_int
    def __init__(self, **kwargs):
        # http://stackoverflow.com/questions/1098549/proper-way-to-use-kwargs-in-python
        # http://stackoverflow.com/questions/8187082/how-can-you-set-class-attributes-from-variable-arguments-kwargs-in-python
        # http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
        self.__dict__.update(kwargs)
    
    def __str__(self):
        # http://stackoverflow.com/questions/1436703/difference-between-str-and-repr-in-python
        # http://stackoverflow.com/questions/3691101/what-is-the-purpose-of-str-and-repr-in-python
        # http://stackoverflow.com/questions/12448175/confused-about-str-in-python
        # http://stackoverflow.com/questions/22797580/how-to-replace-str-for-a-function 
        val = ['%s:%r' % (k, self.__dict__[k]) for k in sorted(self.__dict__)]
        return "%s(%s)" % (self.__class__.__name__, ', '.join(val))
