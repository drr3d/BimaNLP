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

"""
##################################################################################
No      POS     POS Description                     Example
-----------------------------------------------------------------------
1       OP      Open Parenthesis                    ({[
2       CP      Close  Parenthesis                  )}] 
3       GM      Slash                               /
4       ;       Semicolon                           ;
5       :       Colon                               :
6               Quotation                           ` 
7       .       Sentence Terminator                 . ! ?
8       ,       Comma                               ,
9       -       Cash                                -
10      ...     Ellipsis                          ...
11      ADJ     Adjective (kata sifat)              Cantik, cepat
12      ADV     Adverb(kata keterangan)             Sementara, nanti
13      NN      Common noun(nomina = kata benda)    Sepeda
14      NNP     Proper noun(nomina = kata benda)    Jakarta, Bandung
15      NNG     Genitive noun(nomina = kata benda)  Kursinya
16      VBI     Intransitive verb                   Datang
17      VBT     Transitive verb                     Menjual
18      IN      Preposition(Kata depan)             Ke, di, pada
19      MD      Modal                               Bisa
20      CC      Coor-Conjunction(kata penghubung)   Atau, tetapi, dan 
21      SC      Subor-Conjunction                   Jika, ketika 
22      DT      Determiner                          Ini, itu, para
23      UH      Interjection                        Wah, aduh, oi
24      CDO     Ordinal Numerals                    ketiga, keempat
25      CDC     Collective                          Numerals Berempat
26      CDP     Primary Numerals                    Tiga, empat
27      CDI     Irregular Numerals                  Beberapa
28      PRP     Personal Pronouns                   Saya, kamu   (pronoun=pronomina=kataganti) 
29      WP      WH-Pronouns                         Apa, siapa   (pronoun=pronomina=kataganti) 
30      PRN     Number Pronouns                     Kedua-duanya (pronoun=pronomina=kataganti) 
31      PRL     Locative Pronouns                   Sini, situ, sana
32      NEG     Negation                            Tidak, bukan
33      SYM     Symbols                             @#$%^&
34      RP      Particles                           Pun, kah
35      FW      Foreign Words                       Foreign, word
###################################################################################
"""
import sys, re
import patterns

from nltk.corpus.reader import TaggedCorpusReader
from nltk.tokenize import RegexpTokenizer
from nltk.tag import DefaultTagger
from nltk.tag.sequential import UnigramTagger,BigramTagger,TrigramTagger,RegexpTagger

from langutil.tokenizer import tokenize

class NGramTag():
    def __init__(self, corpusroot, corpusname):
        #gunakan custom wordlist corpus dgn method WordListCorpusReader
        #wordlist = WordListCorpusReader(corpus_root, ['wordlist.txt'])
        #gunakan custom wordlist corpus dgn method PlaintextCorpusReader
        #wordlist = PlaintextCorpusReader(corpus_root,'wordlist.txt')

        #nltk_old = [(3,0,1)]
        #nltk_current = [tuple([int(x) for x in nltk.__version__.split('.')])]

        reader = TaggedCorpusReader(corpusroot, corpusname)

        splitratio = 0.8
   
        self.reader_train = reader.tagged_sents()[:int(len(reader.tagged_sents())*splitratio)]
        self.test_sent = reader.tagged_sents()[int(len(reader.tagged_sents())*splitratio):] 

        print "split test ratio: ", int(len(reader.tagged_sents())*splitratio),"\n"
        print "reader_train len: ", len(self.reader_train)
        print "test_sent len: ", len(self.test_sent)
        
    def regexTokenizer(self, sent, pattern=None):
        if pattern:
            tok_pattern = pattern
        else:
            tok_pattern = '\w+|\$[\d\.]+|\S+'

        tokenizer = RegexpTokenizer(tok_pattern)
        
        return tokenizer.tokenize(sent)
    
    def wordTokenizer(self, sent, simple=False):
        if not simple:
            tok = tokenize()
            return tok.WordTokenize(sent)
        else:
            return [x.strip() for x in re.split('(\W+)?', text) if x.strip()]

    def tag(self, sent, tagregex=True, deftag='XX', verbose=False):
        kalimat = sent.encode('utf-8')

        ## :> --___<<IMPORTANT>>___--
        ##      Untuk beberapa hal default tagger harus dibiarkan 'XX'
        ##      dengan tujuan identifikasi Entitas
        backoff_tagger = DefaultTagger(deftag)

        if tagregex:
           text = self.regexTokenizer(kalimat.lower().strip())
           regexp_tagger = RegexpTagger(patterns.regex_patterns,backoff=backoff_tagger)
           unigram_tagger = UnigramTagger(self.reader_train, backoff=regexp_tagger)
        else:
           text = self.wordTokenizer(kalimat.lower().strip())
           unigram_tagger = UnigramTagger(self.reader_train, backoff=backoff_tagger)
           
        bigram_tagger = BigramTagger(self.reader_train, backoff=unigram_tagger)
        trigram_tagger = TrigramTagger(self.reader_train, backoff=bigram_tagger)
        
        """
        # Menggunakan dataset pan localization bahasa indonesia "UI-1M-tagged.txt"
        # kombinasi proses tagging diatas menghasilkan tingkat akurasi:
        #      dengan regextagger: < 77%
        #      tanpa regextagger : > 83%
        """
        if verbose:
           # Semakin besar dokumen, semakin lama proses perhitungan akurasi
           # disarankan hanya untuk testing
           print "Calculating Tagger Accuracy..."
           self.tagAccuracy = trigram_tagger.evaluate(self.test_sent)
           print "Accuracy is: %4.2f %%" % (100.0 * self.tagAccuracy)
        
        return trigram_tagger.tag(text)
