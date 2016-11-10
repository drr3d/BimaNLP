from numpy import log
class MLE():
    def train(self, n, N, ls=False, V=0):
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

        ###################################### 2015-11-07 #########################################
        ## Simpan probabilitas dalam log() format, untuk mencegah numerical computation error
        ##      ketika berhadapan dengan probabilitas yang sangat rendah
        ## https://people.duke.edu/~rnau/411log.htm
        ## http://timvieira.github.io/blog/post/2014/02/11/exp-normalize-trick/
        ###########################################################################################
        return log(float(n)/float(N)) #<= log-probabilities