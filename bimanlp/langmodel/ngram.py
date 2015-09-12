if __package__ is None:
   from os import sys, path
   sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
   from utils.errors import NGramErr
else:
   from utils.errors import NGramErr
   
def ngrams(tok_sentence,n=1,n_jump=0):
    n_gram=n # var berisi jumlah n pada N-Gram, default 1(Uni-Gram)
    n_gram_words=[]
    kata = tok_sentence # var dengan type list berisi tokenize sentence
    
    try:
        if type(tok_sentence) != list:
            raise NGramErr({"message":"Harap masukkan tokenized sentence!!", "tokenize":type(tok_sentence)})
        else:
            if len(tok_sentence) == 0:
                raise NGramErr({"message":"Panjang tokenized sentence tidak boleh 0!!", "tokenize":len(tok_sentence)})

            if n_gram >= len(kata):
                print "Len N-Gram: %i => Len Sentence: %i"%( n_gram, len(kata))
                raise NGramErr({"message":"Total N-Gram tidak boleh melebihi Total Kata", \
                                "tokenize":len(tok_sentence)})

    except NGramErr as e:
        print e.args[0]["message"]
        return
    except:
        print "Unexpected other error:", sys.exc_info()[0]
        return
    else:
        try:
            ################# Mulai proses mengelompokkan kata kedalam N-Gram ################
            for z in range(len(kata)):
                ngram=[]
                if z+n_gram-1 < len(kata): # Jangan sampai loop melebihi total len(kata)
                    for x in range(n_gram):
                        if x > 0:
                            # Untuk mendapat model yang lebih bervariasi, 
                            # kita tambahkan n_jump parameter
                            if z+n_gram-1+n_jump< len(kata):
                                if kata[z+x+n_jump] not in ngram:
                                    # Cegah sample yang berulang pada kumpulan sample
                                    ngram.append(kata[z+x+n_jump])
                            else:
                                if kata[0] not in ngram:
                                    ngram.append(kata[0])
                        else:
                            if kata[z+x] not in ngram:
                                ngram.append(kata[z+x])

                    # Ada beberapa kasus ketika kita menerapkan jump parameter (biasanya jika jump param cukup besar)
                    # terdapat sample yang tidak masuk ke karakteristik populasi N-Gram yang kita inginkan
                    # karena itu kita harus menyaring ulang seluruh sample populasi
                    if len(ngram) == n_gram and ngram not in n_gram_words:
                        n_gram_words.append(ngram)
            ################ Akhir proses mengelompokkan kata kedalam N-Gram #################
        except:
            print "Unexpected other error:", sys.exc_info()[0]
            return
    return n_gram_words

