# -*- coding: utf-8 -*-
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
Main References:
Good-Turing Frequency Estimation Without Tears*
    The paper "Good–Turing frequency estimation without tears" is scanned from pp. 217–37 of the
    Journal of Quantitative Linguistics, vol. 2, 1995.
"""
import math

from scipy import stats
from numpy import log, exp, sqrt
from collections import defaultdict

class SimpleGoodTuring():
    """
    Simple Good-Turing adalah variant dari Good-Turing yang
     menggati penggunaan Nn dengan fitted function f(n)
           f(n) = a + b log(n)
    """

    # jumlah dari masing2 jumlah n
    # misal kata C(W1):1, C(W2):2, C(W3):1, C(W4):2, C(W5):3
    # makan CoC/FoF:{1:2, 2:2, 3:1}
    def __init__(self, lm, N):

        self.FreqofFreq = defaultdict(int)
        self.constructFoF(lm)
        
        self.N = N
        self.estimateUnseenProba()

    def constructFoF(self,lm):
        ## Construct FreqofFreq
        for k, v in lm.iteritems():
            # It is usual to let r be a frequency = v.count = self.FreqofFreq.keys()
            # and Nr=n be the frequecny of frequency = self.FreqofFreq.values()
            # akan menghasilkan table:
            #       r   n
            #       1   10
            #       2   2
            #       3   3
            # yang dapat dibaca r=1= jumlah kemunculan n=10=species yang berbeda
            #       atau gampangnya, ada 10 species/kata yang berbeda yang memiliki
            #       jumlah kemunculan 1 kali
            self.FreqofFreq[v]+=1

    def train(self,lm):
        Z = self.sgtZ()

        # Use Regression analysis to find the "line of best fit"
        #    log(Z) = a*log(r) + b to the pairs of values in the log r and log Z columns
        slope, intercept, r_value, p_value, std_err = stats.linregress(log(Z.keys()),log(Z.values()))
        if slope > -1.0:
            # Menurut Gale:
            # Thus if the estimate for the slope, b, is greater than -1,
            #   the method presented should be regarded as not applicable
            print 'Warning: slope is > -1.0'
            
        """ r* is called the 'adjusted number of observation'
                    which is how many times you should have seen that word(it is often a fraction) """
        rStar={}
        for r in self.sortedFoF:
            """
                The rule for choosing between the Turing estimate and the LGT estimate is to use the Turing estimates
                    so long as they are signiﬁcantly different from the LGT estimates.
                    Once we use an LGT estimate, then we continue to use them.

                Thus this is a rule that may have a few Turing estimates of r* ﬁrst, but then switches
                    to the LGT estimates.
            """

            # The simplest smooth is a line, and a downward sloping log-log line will satisfy the priors on r*
            # so long as the slope of the line b is less than -1. This is the proposed simple smooth,
            # and we call the associated Good-Turing estimate the Linear Good Turing (LGT) estimate
            # LGT = y
            y = float(r+1) * self.LineOBF(slope,float(r+1),intercept) / self.LineOBF(slope,float(r),intercept)

            """
                Since the values in the r column are not continuos, in theory the instruction
                of the preceding paragraph might be impossible to execute because the calculation
                of x could call for an Nr+1 value when the table contained no row with the corresponding
                value in the r column.

                In practice this is likely never to happen, because the switch to using y values will
                occur before gaps appear in the series of r values.
                
                If it did ever happen, the switch to using y values would have to occur at that point
            """
            if r+1 not in self.FreqofFreq:
                rStar[r]=y
                continue

            # Turing estimator = r* = x
            x = float(r+1) * (float(self.FreqofFreq[r+1])/float(self.FreqofFreq[r]))
            
            """
                Turing estimates are considered "signiﬁcantly different" from LGT estimates if their
                difference exceeds 1.65 times the standard deviation (the square root of the variance) of the Turing
                    estimate.
            """
            # The variance for the Turing estimate is approximately:
            VarOfTuringEstimate = float(r+1)**2 * \
                                  float(self.FreqofFreq[r+1])/float(self.FreqofFreq[r]**2) * \
                                       (1. + (float(self.FreqofFreq[r+1])/float(self.FreqofFreq[r])))
            
            SDevOfTuringEstimate = sqrt(VarOfTuringEstimate)
            threshold = 1.96
            if abs(x-y) > (threshold * SDevOfTuringEstimate):
                rStar[r]=x

            # For all subsequent rows insert the respective y value in the r* column
            rStar[r]=y

        # Let N' be the total of the products Nr * r* for the various rows of the table
        NProd = 0
        for k,v in rStar.iteritems():
            NProd+=self.FreqofFreq[k] * v

        """ For each row calculate the value (1-Po) * r*\N' and insert it in the p column """
        # SGTEstimate = p
        SGTEstimate={}
        for k, v in lm.iteritems():
            estimation = float(1.0 - self.p0) * float(rStar[v]/float(NProd))
            SGTEstimate[k]= log(0.0) if math.isnan(estimation) else log(estimation)

        """ each value SGTEstimate in this column is now the Simple Good-Turing Estimate
                for the population frequency of a species
                whose frequency in the sample is r """
        return SGTEstimate, self.p0

    def estimateUnseenProba(self):
        # A useful part of Good-Turing methodology is the estimate that
        #    the total probability of all unseen objects is N1/ N
        # p0 is our estimate of the total probability of all unseen species
        self.p0 = float(self.FreqofFreq[1])/float(self.N)

    def LineOBF(self,slope,i,intercept):
        # The formula for the best-fitting line (or regression line) is y = mx + b,
        # where m is the slope of the line and b is the y-intercept.
        return exp(slope * log(i)+ intercept)

    def sgtZ(self):
        Z={}
        # http://stackoverflow.com/questions/9001509/how-can-i-sort-a-dictionary-by-key
        """ Based on following work in Church and Gale[1991],
            we need to order the non-zero Nr by r
            """
        # Karena kita menggunakan dict() type pada FoF, dan semenjak dict() type itu unordered,
        #   dengan demikian tidak mungkin untuk mengakses dictionary by index, karena itu kita akan
        #   mengeluarkan key pada dictionary dengan sorted()
        self.sortedFoF=sorted(self.FreqofFreq.keys())
        
        for (idx, j) in enumerate(self.sortedFoF):
            if idx == 0:
                i = 0
            else:
                i = self.sortedFoF[idx-1]
                
            if idx == len(self.sortedFoF)-1:
                k = 2*j - i
            else:
                k = self.sortedFoF[idx+1]
            Z[j] = 2*self.FreqofFreq[j] / float(k-i)
        return Z
