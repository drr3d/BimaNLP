class Error(Exception):
   """Base class for other exceptions"""
   pass

class StopWordMustList(Error):
   """Raised when the input stopword value is not a list"""
   pass
