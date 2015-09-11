import re
import string

stopwords= ['kah','lah','pun','jah','jeh','mu','ku','ke','di','tapi','saya','kamu','mereka','dia', \
          'kita','adalah','dan','jika','kalau','sama','yang', \
          'sekarang','nanti','besok','kemarin','kemaren','nya','na',\
          'at','apa','ini','itu','juga','ketika','namun',\
          'sebab','oleh','malah','memang']

class Error(Exception):
   """Base class for other exceptions"""
   pass

class StopWordMustList(Error):
   """Raised when the input stopword value is not a list"""
   pass

def WordTokenize(sentence,stopword=None,remove_punct=False):
    # Split kalimat kedalam kata-kata terpisah berdasar 'spasi'

    words = re.split(r'\s',sentence)

    if remove_punct:
        # Buat translation table untuk digunakan di string.translate
        table = string.maketrans("","")

        # The method translate() returns a copy of the string in which all characters have been translated
        # using table (constructed with the maketrans() function in the string module),
        # optionally deleting all characters found in the string deletechars.
        words = [z.translate(table,string.punctuation).strip() for z in words]

    # Hapus seluruh empty char pada list
    words = filter(lambda x: x!='', words)

    # Hapus kata yang berada dalam stopwords
    if stopword!=None:
        try:
            if type(stopword)!=list:
                raise StopWordMustList

            words = filter(lambda x: x not in stopword, words)
            
        except StopWordMustList:
            print "Tipe stopword harus list"
            return
        except:
            print "Unexpected other error:", sys.exc_info()[0]
            return
    
    return words

kata = 'makan nasi goreng dipinggir empang, memang !! sungguh  nikmat sekali.'
kata = WordTokenize(kata,'makan')
if kata:
    print kata
    

