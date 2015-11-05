from langutil.tokenizer import tokenize
from langutil.stemmer import ChaosStemmer
from langmodel.modeler.markov import NGramModels

import langmodel.ngram as ngram

def TextTokenizer(sen):
    # Materi Syntatic proses:text tokenizing
    # http://blog.pantaw.com/syntatic-proses-text-tokenizing/
    stopwords= ['kah','lah','pun','jah','jeh','mu','ku','ke','di','tapi','saya','kamu','mereka','dia', \
          'kita','adalah','dan','jika','kalau','sama','yang', \
          'sekarang','nanti','besok','kemarin','kemaren','nya','na',\
          'at','apa','ini','itu','juga','ketika','namun',\
          'sebab','oleh','malah','memang']
        
    tok = tokenize()
    kata = tok.WordTokenize(sen,removepunct=False)
    if kata:
        print "kalimat setelah di tokenize: ", kata, "\n"
    return kata

def NgramModel(sen):
    # Materi Syntatic proses:N-Gram
    # http://blog.pantaw.com/syntatic-proses-n-grams/
    kata = TextTokenizer(sen)
    kata = ngram.ngrams(kata,n=2,njump=0)
    
    print "Jumlah sample: ", len(kata)
    for z in kata:
        print ' '.join(z)
    print "\n"

def stemm(toksen):
    # Materi Syntatic proses: Text Stemmer bahasa Indonesia dengan Python
    # http://blog.pantaw.com/syntatic-proses-text-stemmer-bahasa-indonesia-dengan-python/
    morph = ChaosStemmer('C:\\BimaNLP\\dataset\\','tb_katadasar.txt')
    
    for z in words:
        morph.stemm(z)
        #menyeimbangkan,menyerukan,mengatakan,berkelanjutan,pembelajaran,pengepulannya
        #print "Dirty guess word is: ",morph.getFoundGuessWord()
        #print "Detected Affix is: ", morph.getFoundSuffix(),"\n"
        print "Root kata untuk kata: ", z ," -> adalah: ", morph.getRootWord()
        print "Filtered guess word adalah:", morph.getFilteredGuessWord(),"\n"

def NGramLangModel():
    dataset=[['saya','suka','kamu'],
         ['kamu','suka','saya'],
         ['saya','tidak','suka','jika','kamu','pergi','dengan','dia']
         ]

    lms = NGramModels()
    models = lms.train(dataset,smooth='',separate=True)

    for k, v in models.iteritems():
        print k
        for key,val in v.iteritems():
            print key,val
        print "\n"
        
if __name__ == "__main__":
    kata1 = 'memakan nasi goreng dipinggir empang, memang !! sungguh  nikmat sekali.'
    kata2 = 'penghasilannya hanya cukup untuk memenuhi keseluruhan kebutuhan kedua buah hati kesayangannya'
    kata3 = 'ketiga burung kecil itu saling siul-menyiul bersahut-sahutan di pagi hari'

    ## Stemming hanya membutuhkan textTokenize
    #words = TextTokenizer(kata3.lower())#kata3.lower()
    #stemm(words)

    NGramLangModel()
