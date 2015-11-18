######################################################################
#                           Original Author                          #
#                           --Josef Novak--                          #
# https://github.com/AdolfVonKleist/SimpleLM                         #
# https://groups.google.com/forum/embed/#!topic/nltk-dev/0hk4EjNxF4k #
#                                                                    #
# All credit of this module should return to the original author     #
#      mentioned above!!                                             #
######################################################################
from collections import defaultdict
from math import log,exp
import re,sys

class NGramStack( ):
    """
      A stack object designed to pop and push word 
      tokens onto an N-gram stack of fixed max-length.
    """
    
    def __init__( self, order=3 ):
        #Maximum span for N-grams in this model.
        self.o = order 
        #The actual stack
        self.s     = []

    def push( self, word ):
        """ 
           Push a word onto the stack.
           Pop off the bottom word if the
           stack size becomes too large.
        """
        self.s.append(word)
        if len(self.s)>self.o:
            self.s.pop(0)
        return self.s[:]

    def pop( self ):
        self.s.pop(0)
        return self.s[:]

    def clear( self ):
        """
           Empty all the words from the stack.
        """
        self.s = []
        
class ModifiedKneserNey:
    def __init__( self, order=3, sb="<s>", se="</s>" ):
        self.sb        = sb
        self.se        = se
        self.order     = order
        self.ngrams    = NGramStack(order=order)
        self.denominators = [ defaultdict(float) for i in xrange(order-1) ]
        self.numerators   = [ defaultdict(float) for i in xrange(order-1) ]
        #Modified Kneser-Ney requires that we track the individual N_i
        # in contrast to Kneser-Ney, which just requires the sum-total.
        self.nonZeros     = [ defaultdict(lambda: defaultdict(float)) for i in xrange(order-1) ]
        self.CoC          = [ [ 0.0 for j in xrange(4) ] for i in xrange(order) ]
        self.discounts    = [ [ 0.0 for j in xrange(3) ] for i in xrange(order-1) ]
        self.UD = 0.
        self.UN = defaultdict(float)

    def _compute_counts_of_counts( self ):
        """
          Compute counts-of-counts (CoC) or frequenc-of-frequency(FoF)
          for each N-gram order.
          Only CoC/FoF<=4 are relevant to the computation of
          either ModKNFix or KNFix.
        """

        for k in self.UN:
            if self.UN[k] <= 4:
                self.CoC[0][int(self.UN[k]-1)] += 1.

        for i,dic in enumerate(self.numerators):
            for k in dic:
                if dic[k]<=4:
                    self.CoC[i+1][int(dic[k]-1)] += 1.
        return

    def _compute_discounts( self ):
        """
          Compute the discount parameters. Note that unigram counts
          are not discounted in either FixKN or FixModKN.

          ---------------------------------
          Fixed Modified Kneser-Ney: FixModKN
          ---------------------------------
          This is the solution proposed by Chen&Goodman '98

             Y    = N_1 / (N_1 + 2*N_2)
             D_1  = 1 - 2*Y * (N_2 / N_1)
             D_2  = 2 - 3*Y * (N_3 / N_2)
             D_3+ = 3 - 4*Y * (N_4 / N_3)

          where N_i again refers to the number of N-grams that appear
          exactly 'i' times in the training data.  The D_i refer to the
          counts-of-counts for the current N-gram.  That is, if the 
          current N-gram, 'a b c' was seen exactly two times in the 
          training corpus, then discount D_2 would be applied.

        """

        for o in xrange(self.order-1):
            Y = self.CoC[o+1][0] / (self.CoC[o+1][0]+2*self.CoC[o+1][1])
            #Compute all the D_i based on the formula
            for i in xrange(3):
                if self.CoC[o+1][i]>0:
                    self.discounts[o][i] = (i+1) - (i+2)*Y * (self.CoC[o+1][i+1]/self.CoC[o+1][i])
                else:
                    self.discounts[o][i] = (i+1)

        return 

    def _get_discount( self, order, ngram ):
        """
          Compute the discount mass for this N-gram, based on 
           the precomputed D_i and individual N_i.
        """

        c  = [0.0, 0.0, 0.0]
                    
        for key in self.nonZeros[order][ngram]:
            if int(self.nonZeros[order][ngram][key])==1:
                c[0] += 1.
            elif int(self.nonZeros[order][ngram][key])==2:
                c[1] += 1.
            else:
                c[2] += 1.

        #Compute the discount mass by summing over the D_i*N_i 
        d = sum([ self.discounts[order][i]*c[i] for i in xrange(len(c)) ])
        return d

    def kneser_ney_discounting( self, vect ):
        """
          Iterate through the training data using a FIFO stack or 
           'window' of max-length equal to the specified N-gram order.

          Each time a new word is pushed onto the N-gram stack call
           the _kn_recurse() subroutine to increment the N-gram 
           contexts in the current window / on the stack. 

          If pushing a word onto the stack makes len(stack)>max-order, 
           then the word at the bottom (stack[0]) is popped off.
        """
        for sent in vect:
            #Push a sentence-begin token onto the stack
            self.ngrams.push(self.sb)

            for word in sent:
                #Get the current 'window' of N-grams
                ngram = self.ngrams.push(word)

                #Now count all N-grams in the current window
                #These will be of span <= self.order
                self._kn_recurse( ngram, len(ngram)-2 )

            #Now push the sentence-end token onto the stack
            ngram = self.ngrams.push(self.se)
            self._kn_recurse( ngram, len(ngram)-2 )

            #Clear the stack for the next sentence
            self.ngrams.clear()
        
        self._compute_counts_of_counts ( )
        self._compute_discounts( )

        return

    def _kn_recurse( self, ngram_stack, i ):
        """
         Kneser-Ney discount calculation recursion.
        """
        if i==-1 and ngram_stack[0]==self.sb:
            return

        o     = len(ngram_stack)
        numer = " ".join(ngram_stack[o-(i+2):])
        denom = " ".join(ngram_stack[o-(i+2):o-1])
        self.numerators[  i][numer] += 1.
        self.denominators[i][denom] += 1.
 
        #For Modified Kneser-Ney we need to track 
        # individual nonZeros based on their suffixes
        self.nonZeros[i][denom][ngram_stack[-1]] += 1.
        if self.numerators[i][numer]==1.:
            if i>0:
                self._kn_recurse( ngram_stack, i-1 )
            else:
                #The <s> (sentence-begin) token is
                # NOT counted as a unigram event
                if not ngram_stack[-1]==self.sb:
                    self.UN[ngram_stack[-1]] += 1.
                    self.UD += 1.
        return

    def _compute_interpolated_prob( self, ngram ):
        """
          Compute the interpolated probability for the input ngram.
          Cribbing the notation from the SRILM webpages,

             a_z    = An N-gram where a is the first word, z is the 
                       last word, and "_" represents 0 or more words in between.
             p(a_z) = The estimated conditional probability of the 
                       nth word z given the first n-1 words (a_) of an N-gram.
             a_     = The n-1 word prefix of the N-gram a_z.
             _z     = The n-1 word suffix of the N-gram a_z.

          Then we have, 
             f(a_z) = g(a_z) + bow(a_) p(_z)
             p(a_z) = (c(a_z) > 0) ? f(a_z) : bow(a_) p(_z)

          The ARPA format is generated by writing, for each N-gram
          with 1 < order < max_order:
             p(a_z)    a_z   bow(a_z)

          and for the maximum order:
             p(a_z)    a_z

          special care must be taken for certain N-grams containing
           the <s> (sentence-begin) and </s> (sentence-end) tokens.  
          See the implementation for details on how to do this correctly.

          The formulation is based on the seminal Chen&Goodman '98 paper.
        """
        probability = 0.0
        ngram_stack = ngram.split(" ")
        probs       = [ 1e-99 for i in xrange(len(ngram_stack)) ]
        o           = len(ngram_stack)

        if not ngram_stack[-1]==self.sb:
            probs[0] = self.UN[ngram_stack[-1]] / self.UD

        for i in xrange(o-1):
            dID = " ".join(ngram_stack[o-(i+2):o-1])
            nID = " ".join(ngram_stack[o-(i+2):])
            if dID in self.denominators[i]:
                count = int(self.numerators[i][nID])
                d_i   = min(count, 3)
                probs[i+1] = (count-self.discounts[i][d_i-1])/self.denominators[i][dID]

                #This break-down takes the following form:
                #  probs[i+1]:  The interpolated N-gram probability, p(a_z)
                #  d:           The discount mass for a_: \Sum_i D_i*N_i
                #  lmda:        The un-normalized 'back-off' weight, bow(a_)
                #  probs[i]:    The next lower-order, interpolated N-gram 
                #               probability corresponding to p(_z)
                #ModKN discount
                d = self._get_discount( i, dID )
                lmda        = d / self.denominators[i][dID]
                probs[i+1]  = probs[i+1] + lmda * probs[i]
                probability = probs[i+1]

        if probability == 0.0:
            #If we still have nothing, return the unigram probability
            probability = probs[0]

        return probability

    def train( self ):
        """
             \1-grams:
             p(a_z)  a_z  bow(a_z)    
             \2-grams:
             p(a_z)  a_z  bow(a_z)
             \N-grams:
             p(a_z)  a_z
        """
        #Handle the Unigrams
        self.mKNeyEstimate={}
        d    = self._get_discount( 0, self.sb )
        #ModKN discount
        lmda = d / self.denominators[0][self.sb]
        first=-99.00000
        #self.mKNeyEstimate[self.sb]=(("proba",first),("bow",log(lmda, 10.)),("count",1.),("n",1))
        self.mKNeyEstimate[self.sb]=(first, log(lmda, 10.), 1, 1)
        for key in sorted(self.UN.iterkeys()):
            if key==self.se:
                self.mKNeyEstimate[key]=(log(self.UN[key]/self.UD, 10.), 0.0, self.UN[key], 1)
                continue

            d    = self._get_discount( 0, key )
            #ModKN discount
            lmda = d / self.denominators[0][key]
            
            self.mKNeyEstimate[key]=(log(self.UN[key]/self.UD, 10.),log(lmda, 10.),self.UN[key],1)
        
        #Handle the middle-order N-grams
        for o in xrange(0,self.order-2):
            for key in sorted(self.numerators[o].iterkeys()):
                if key.endswith(self.se):
                    #No back-off prob for N-grams ending in </s>
                    prob = self._compute_interpolated_prob( key )
                    self.mKNeyEstimate[key]=(log(prob, 10.),0.0,self.numerators[o][key],2)
                    continue
                d = self._get_discount( o+1, key )
                #Compute the back-off weight
                #ModKN discount
                lmda  = d / self.denominators[o+1][key]
                #Compute the interpolated N-gram probability
                prob = self._compute_interpolated_prob( key )
                self.mKNeyEstimate[key]=(log(prob, 10.),log(lmda, 10.),self.numerators[o][key],2)

        #Handle the N-order N-grams
        for key in sorted(self.numerators[self.order-2].iterkeys()):
            #Compute the interpolated N-gram probability
            prob = self._compute_interpolated_prob( key )
            self.mKNeyEstimate[key]=(log(prob, 10.),0.0,self.numerators[self.order-2][key],3)
        return
