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

# http://stackoverflow.com/questions/8998979/what-is-the-difference-between-pos-tagging-and-shallow-parsing
import grammar
from nltk.chunk.regexp import RegexpParser
from nltk.tag import util
"""
##########################################################################################
################################## PHRASE RULE ##########################################
POS forming phrase

    Types of Phrases                                POS Tag
--------------------------      --------------------------------------------- 
Questioning Phrase (TP)         WP 
Numeric Phrases (BP)            CDO, CDP, CDI, CDC
Connection Phrases (KP)         SC, CC, NEG, IN, MD, RB
Noun(Kata benda) Phrases (NP)   NN, PRN,  PRP, PRL, NNG, NNP, FW, RP, UH
Verb(Kata kerja) Phrases (VP)   VINTR(Pasif)=> tidak butuh objek, VTRAN(Aktif) => membutuhkan objek
################################ END PHRASE RULE ########################################

################################# REGEX RULE ###########################################
Pattern		Matches
--------------------------------
T	    a word with tag T (where T may be a regexp).
x?	    an optional x
x+	    a sequence of 1 or more x's
x*	    a sequence of 0 or more x's
x|y	    x or y
.	    matches any character
(x)	    Treats x as a group
# x...	    Treats x... (to the end of the line) as a comment
\C	    matches character C (useful when Cis a special character like + or #)

Examples:
<NN>
		Matches "cow/NN"
		Matches <match>"green/NN"</match>
<VB.*>
		Matches "eating/VBG"
		Matches "ate/VBD"
<IN><DT><NN>
		Matches "on/IN the/DT car/NN"
<RB>?<VBD>
		Matches "ran/VBD"
		Matches "slowly/RB ate/VBD"
<\#><CD> # This is a comment...
		Matches "#/# 100/CD"
################################# END REGEX RULE ###########################################
###########################################################################################
"""

class TagChunker():
    grammar = grammar.chunk_grammar

    def treeDraw(self, wordchunk):
        """ Harus didahului dengan fungsi tagChunk() """
        wordchunk.draw()
        
    def treeChecker(self, wordchunk):
        """ Harus didahului dengan fungsi tagChunk() """
        for n in wordchunk:
            if isinstance(n, nltk.tree.Tree):
                return True #print n, "-", n.node
            else:
                return False

    def treePrint(self, wordchunk,draw=True):
        """ Harus didahului dengan fungsi tagChunk() """
        if draw:
            wordchunk.draw()
        else:
            for subtree in wordchunk.subtrees():
                print subtree
            
    def treeExtractor(self, wordchunk, rules):
        """ Harus didahului dengan fungsi tagChunk() """
        ## tambahkan didalam subtrees() filter=lambda t: t.node == 'NP'  untuk ambil spesifik leaves tag
        ## Extrak juga info yang berbentuk kalimat (memiliki predikat) <<== IMPORTANT ==>>
        sentences = []
        for subtree in wordchunk.subtrees(filter=rules):
            # print the noun phrase as a list of part-of-speech tagged words       
            sentences.append((" ".join(["%s" % word[0] for word in subtree.leaves()]),subtree.label()))
        return sentences

    def tagChunk(self, taggedword, loops=2):
        ## Cunking
        cp = RegexpParser(self.grammar, loop=loops)
        return cp.parse(taggedword)

    def tagTokenExtractor(self, wordtaggedlist):
        for z in wordtaggedlist:
            taggedtoken = util.str2tuple('/'.join(z))
            print taggedtoken[1]

    def tagTokenizer(self, wordChunk):
        """ Harus didahului dengan fungsi tagChunk() """
        # melihat frasa apa saja yang terdapat dalam kalimat
        for subtree in wordChunk.subtrees():
            if subtree.label().lower() != 's':
                print subtree.label()#, type(subtree)

    def delTag(self, taggertext, tagtoremove, minlen=1):
        # Menghapus spesifik tag pada kalimat
        text = filter(lambda x: x[1] not in tagtoremove and len(x[0]) > minlen, tagger(taggertext))
        text = ' '.join([z[0] for z in text])
        return text
