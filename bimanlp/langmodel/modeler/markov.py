# -*- coding: utf-8 -*-
from os import sys, path

if __package__ is None:
    sys.path.append("C:\\BimaNLP\\bimanlp")
    from langmodel.vocab import SimpleVocab
    from langmodel import ngram
    from langutil.tokenizer import tokenize
else:
    from langmodel.vocab import SimpleVocab
    from langmodel import ngram
    from langutil.tokenizer import tokenize

def constructVocab(vect, totalword, nforgram, separate=True, njump=0):
    # kata masuk sudah ditokenize
    # kalo buat N-Gram brarti: ['saya sedang', 'sedang makan',...,'warung depan']
    freqDist=dict()
    total_word=totalword

    dataset=[]
    jumpdataset=[]

    ############################### 2015-11-07 ################################
    ## Dipisah, supaya penggunaan jump parameter tidak mempengaruhi
    ## jumlah dari keseluruhan kata, hanya akan mempengaruhi frekuensi sample
    ###########################################################################
    def scale(voc):
        for z in xrange(len(voc)):
            for y in xrange(len(voc[z])):
                # Untuk menangani bentuk Selain bigram, karena itu kita menggunakan format ini
                freqDist.setdefault(' '.join(voc[z][y]),0)
                
                # C(Wi) => rekam jumlah kemunculan suatu kata
                freqDist[' '.join(voc[z][y])]+=1
                
    for z in vect:
        # Semua yang masuk ke language model ngram, harus melalui proses tokenize->ngram
        if separate:
            if '<s>' not in z: z.insert(0,'<s>')
            if '</s>' not in z: z.insert(len(z),'</s>')
        dataset.append(ngram.ngrams(z,n=nforgram))
        if njump>0:
           jumpdataset.append(ngram.ngrams(z,n=nforgram,njump=njump)) 

    scale(dataset)
    
    if totalword==0:
        # self.total_word = N = Jumlah(C) seluruh kata/sample pada kalimat/ruang sample
        total_word = sum(freqDist.values())

    if jumpdataset:
        scale(jumpdataset)

    print ("Vocab size for N=%i is:%i, with Total Word(corpus length):%i" % (nforgram,len(freqDist),total_word))
    return freqDist,total_word
        
class NGramModels:
    """
    Secara default NgramModel akan membentuk Bigram, karena Unigram dipertimbangkan terlalu noise
        kenapa terlalu banyak noise? karena unigram tidak menggunakan data histori
    """
    vocab={}
    finalmodel={}
    min_count = 0
    total_word = 0
    
    def __init__(self, ngram=2):
        self.nforgram = ngram
        
    def MLE(self,n,N,ls=False,V=0):
        """ Estimasi nilai Probabilitas suatu Kata """
        ### Bisa dibilang juga, ini adalah proses training NGram LM dengan metoda MLE ###
        
        # Compute Maximum Likelihood Estimates for individual n-gram probabilities
        # Problem using this as estimator: Weak when counts(N) are low or Unknown word is present
        
        # n = Jumlah(C) dari suatu kata/sample
        # N = Jumlah(C) seluruh kata/sample pada kalimat/ruang sample
        # ls = Laplace Smoothing
        # V = Ukuran dari Vocabulary
        """ Pada dasarnya smoothing digunakan untuk mengatasi permasalahan
            Data Sparsity, indikasi dari data sparsity ditandai dengan munculnya
            nilai 0 pada probabilitas.
        """
        n = n+1 if ls else n
        N = N+V if ls else N

        return round(float(n)/float(N),4)

    def train(self,vect,smooth=None,separate=True):
        """
        In the study of probability, given at least two random variables X, Y, ...,that are defined on a probability space S,       
        the joint probability distribution for X, Y, ... is a probability distribution
            that gives the probability that each of X, Y, ... falls in any particular range
            or discrete set of values specified for that variable

        #####################################################################################################################
            #############################################################################################################
        demikian jika diberikan kalimat S: "saya sedang makan nasi goreng di warung depan"
        berarti p(w1,w2,...,wn) disebut sebagai distribusi probabilitas(dimana w1,w2,...wn sebagai random variables), 
            kata (w1,w2,...,wn), over the kalimat S
        """
        tok = tokenize()
        for i in range(1,self.nforgram+1):            
            self.nforgram=i
            self.raw_vocab,self.total_word = constructVocab(vect, self.total_word, \
                                                            nforgram=self.nforgram, separate=separate)

            for k, v in self.raw_vocab.iteritems():
                # Hitung:
                # P(Wi) = C(Wi) / N <= untuk UniGram <= dicari melalui MLE
                if i==1:
                    # Unigram do not use history
                    """ WARNING!!! Kalau menggunakan SGT smoothing, MLE tidak digunakan """
                    if smooth=='ls':
                        V=len(self.raw_vocab) #<= gunakan jika menggunakan laplace smoothing
                        self.vocab[k] = SimpleVocab(count=v, estimator=self.MLE(v,self.total_word,ls=True,V=V))
                    else:
                        self.vocab[k] = SimpleVocab(count=v, estimator=self.MLE(v,self.total_word))
                elif i ==2:
                    """
                    Perlu diingat motivasi dibalik NGram LM adalah:
                    begin with the task of computing P(w|h), the probability of a word w given some history h
                    """
                    # P(Wi, Wj) = C(Wi, Wj) / N <= untuk BiGram <= dicari melalui MLE
                    #   tetapi yang perlu kita cari adalah P(Wj | Wi) == conditional distribution untuk
                    #       seberapa kemungkinan kata Wj muncul diberikan kata Wi sebelumnya
                    # P(Wj | Wi) = P(Wi, Wj) / P(Wi) = C(Wi, Wj) / C(Wi)
                    #       C(Wi)=> adalah unigram count
                    CWi = self.finalmodel[i-1][tok.WordTokenize(k)[0]].count
                    if smooth=='ls':
                        V=len(self.raw_vocab) #<= gunakan jika menggunakan laplace smoothing
                        self.vocab[k] = SimpleVocab(count=v, estimator=self.MLE(v,CWi,ls=True,V=V))
                    else:
                        self.vocab[k] = SimpleVocab(count=v, estimator=self.MLE(v,CWi))
                elif i ==3:
                    #######################################################################################
                    # P(Wi, Wj, Wk) = C (Wi, Wj, Wk) / N <= untuk Trigram
                    #   tetapi yang perlu kita cari adalah P(Wk | Wi, Wj) == conditional distribution untuk
                    #       seberapa kemungkinan kata Wk muncul diberikan kata Wi,Wj sebelumnya
                    CWi = self.finalmodel[i-1][' '.join(tok.WordTokenize(k)[:-1])].count
                    if smooth=='ls':
                        V=len(self.raw_vocab) #<= gunakan jika menggunakan laplace smoothing
                        self.vocab[k] = SimpleVocab(count=v, estimator=self.MLE(v,CWi,ls=True,V=V))
                    else:
                        self.vocab[k] = SimpleVocab(count=v, estimator=self.MLE(v,CWi))

            self.finalmodel[i]=self.vocab                
            self.vocab={}
            del self.raw_vocab
        
        return self.finalmodel
