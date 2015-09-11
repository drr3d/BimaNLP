def ngrams(tok_sentence,n=1):
    if type(tok_sentence) != list:
        print "Harap masukkan tokenized sentence!!"
        return
    else:
        if len(tok_sentence) == 0:
            print "Panjang tokenized sentence tidak boleh 0!!"
            return
    
    n_gram=n
    n_gram_words=[]
    if n_gram <= len(kata):
        for z in range(len(kata)):
            ngram=[]
            if z+n_gram-1 < len(kata):
                for x in range(n_gram):
                    ngram.append(kata[z+x])
                    
                n_gram_words.append(ngram)
                #print ngram
    else:
        print ("Total N-Gram:%i tidak boleh melebihi Total Kata:%i"%(n_gram,len(kata)))
        return
    return n_gram_words

#ngram = ngrams(kata,11)
#print ngram
