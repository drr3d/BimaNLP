from bimanlp.langutil.tokenizer import tokenize
from bimanlp.langmodel.modeler.markov import NGramModels
from bimanlp.utils.loader import Loader

import os

MAIN_DIR = os.path.abspath(os.path.curdir)
DS_DIR = '/dataset/'

def NGramLangModel(verbose=False):
    txtdata='tb_kota_bywiki.txt'

    cl = Loader(MAIN_DIR+DS_DIR)
    f = cl.loadLarge(txtdata,lazy_load=True)
    w = cl.processRaw(f,to_lower=True)
    tokenized_sentence = cl.rawForLangmodel(w,punct_remove=True,to_token=True)

    lms = NGramModels(ngram=3, normalize_logprob=False)
    # njump parameter belum bisa digunakan untuk modkn optimizer
    models = lms.train(tokenized_sentence, optimizer='modkn',\
                       separate=True, njump=0, \
                       verbose=verbose)
    if verbose:
    	for k,v in models.iteritems():
    		for k2,v2 in v.iteritems():
    			print k2,v2
    print lms.perplexity
    print "##########################################################"

NGramLangModel(verbose=True)