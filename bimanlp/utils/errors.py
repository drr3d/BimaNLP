class Error(Exception):
   """Base class for other exceptions"""
   pass

class StopWordMustList(Error):
   """Raised when the input stopword value is not a list"""
   pass

class NGramErr(Error):
   """Raised For Error in N-Grams Modeling"""
   pass
