from langutil.tokenizer import tokenize

stopwords= ['kah','lah','pun','jah','jeh','mu','ku','ke','di','tapi','saya','kamu','mereka','dia', \
          'kita','adalah','dan','jika','kalau','sama','yang', \
          'sekarang','nanti','besok','kemarin','kemaren','nya','na',\
          'at','apa','ini','itu','juga','ketika','namun',\
          'sebab','oleh','malah','memang']

def tutor1():
    kata = 'makan nasi goreng dipinggir empang, memang !! sungguh  nikmat sekali.'
    tok = tokenize()
    kata = tok.WordTokenize(kata)
    if kata:
        print kata
        
if __name__ == "__main__":
    tutor1()

