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

import re
import string

if __package__ is None:
   from os import sys, path
   sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
   from utils.errors import StopWordMustList
else:
   from utils.errors import StopWordMustList

class tokenize():
   def WordTokenize(self, sentence, stopword=None, removepunct=False):
       # Split kalimat kedalam kata-kata terpisah berdasar 'spasi'

       words = re.split(r'\s',sentence)

       if removepunct:
           # Buat translation table untuk digunakan di string.translate
           table = string.maketrans("","")

           # The method translate() returns a copy of the string in which all characters have been translated
           # using table (constructed with the maketrans() function in the string module),
           # optionally deleting all characters found in the string deletechars.
           words = [z.translate(table,string.punctuation).strip() for z in words]

       # Hapus seluruh empty char pada list
       words = filter(lambda x: x!='', words)

       # Hapus kata yang berada dalam stopwords
       if stopword!=None:
           try:
               if type(stopword)!=list:
                   raise StopWordMustList({"message":"Tipe stopword harus list", "stopword":type(stopword)})

               words = filter(lambda x: x not in stopword, words)
               
           except StopWordMustList as e:
               print e.args[0]["message"], " ,Get stopword type:", e.args[0]["stopword"]
               return
           except:
               print "Unexpected other error:", sys.exc_info()[0]
               return
       
       return words

   def CharTokenize(self,word):
      return list(word)
