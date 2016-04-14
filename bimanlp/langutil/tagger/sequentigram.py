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
import sys
import patterns
from nltk.corpus.reader import TaggedCorpusReader
from nltk.tokenize import RegexpTokenizer
from nltk.tag import DefaultTagger
from nltk.tag.sequential import UnigramTagger,BigramTagger,TrigramTagger,RegexpTagger

class NGramTag():
    def __init__(self, corpusroot, corpusname):
        #gunakan custom wordlist corpus dgn method WordListCorpusReader
        #wordlist = WordListCorpusReader(corpus_root, ['wordlist.txt'])
        #gunakan custom wordlist corpus dgn method PlaintextCorpusReader
        #wordlist = PlaintextCorpusReader(corpus_root,'wordlist.txt')

        reader = TaggedCorpusReader(corpusroot, corpusname)
   
        self.reader_train = reader.tagged_sents()
        self.test_sent = reader.tagged_sents()[1000:] 
        
    def regexTokenizer(self, sent):
        ## Text tokenize
        tok_patterns = r'''(?x)      # set flag to allow verbose regexps
              ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
            | \b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}\b
            | "(.*?)"   
            | \w+(-\w+)*            # words with optional internal hyphens
            | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
            | \.\.\.                # ellipsis
            | [][.,;"'?():-_`]      # these are separate tokens
        '''
        #([A-Z]\w+){1,} => cari kata yg depannya huruf kapital

        tokenizer = RegexpTokenizer(tok_patterns)
        
        return tokenizer.tokenize(sent)
    
    def tag(self, sent, tagregex=True, deftag='XX', verbose=False):
        kalimat = sent.encode('utf-8')

        text = self.regexTokenizer(kalimat.lower().strip())

        ## :> --___<<IMPORTANT>>___--
        ##      Untuk beberapa hal default tagger harus dibiarkan 'XX'
        ##      dengan tujuan identifikasi Entitas
        backoff_tagger = DefaultTagger(deftag)

        if tagregex:
           regexp_tagger = RegexpTagger(patterns.regex_patterns,backoff=backoff_tagger)
           unigram_tagger = UnigramTagger(self.reader_train, backoff=regexp_tagger)
        else:
           unigram_tagger = UnigramTagger(self.reader_train, backoff=backoff_tagger)
           
        bigram_tagger = BigramTagger(self.reader_train, backoff=unigram_tagger)
        trigram_tagger = TrigramTagger(self.reader_train, backoff=bigram_tagger)
        
        """
        # Menggunakan dataset pan localization bahasa indonesia "UI-1M-tagged.txt"
        # kombinasi proses tagging diatas menghasilkan tingkat akurasi:
        #      dengan regextagger: 77%
        #      tanpa regextagger : > 90%
        """
        if verbose:
           # Semakin besar dokumen, semakin lama proses perhitungan akurasi
           # disarankan hanya untuk testing
           print ("Calculating Tagger Accuracy...")
           self.tagAccuracy = trigram_tagger.evaluate(self.test_sent)
           print ("Accuracy is: %s" % (self.tagAccuracy))
        
        return trigram_tagger.tag(text)
