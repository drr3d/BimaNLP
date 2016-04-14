########################## This file is part of BimaNLP. ############################
# BimaNLP is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# BimaNLP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#####################################################################################

####################################################### ATURAN IMBUHAN ##############################################################
#####################################################################################################################################
##prefixes(awalan):pe-, di-, se-, ke-, me-, ber-, mem-, men-, pem-, pen-, per-,  ter-, meng-, meny-, peng-, peny-, menge-,  penge- 
##suffixes(akhiran):-i, -an, -kan,  -lah, -kah, -nya
##confixes:ber - an, per - an, pem - an, pen - an, ke - an, pe - an, se - nya,  peng - an, peny - an, penge - an
##infixes(sisipan):el, em, er
##combining forms: antar-, para-, eka-, kau-, ku-, oto-, -pun, -ku, -mu, -nya

## untuk kata dasar yg memiliki huruf awal 's' dan menggunakan prefix meny- otomatis huruf awal 's'-nya hilang
##      contoh meny- + sapu = menyapu, meny- + sambung = menyambung, meny- + sesal = menyesal
## logic awal untuk membedakan prefix men- dan meny- : jika huruf setelah prefix men- adalah 'y', maka dipastikan
##      kata tersebut menggunakan prefix meny-
## aturan diatas juga berlaku untuk prefix ataupun jika ada di confix pen- dan peny-

## untuk kata dasar yg memiliki huruf awal 't' dan menggunakan prefix men- otomatis huruf awal 't' nya hilang
##      contoh men- + tinju = meninju, men- + tari = menari

## untuk kata dasar yg memiliki huruf awal 'k' dan menggunakan prefix penge- otomatis huruf awal 'k' nya hilang
##      contoh penge- + kepak = pengepakan, penge- + kepul = pengepul
## untuk kata dasar yg memiliki huruf awal 'k' dan menggunakan prefix menge- otomatis huruf awal 'k' nya hilang
##      contoh menge- + kesal = mengesalkan, menge- + kesah = mengesah

## untuk kata dasar yg memiliki huruf awal 'p' dan menggunakan prefix pem- otomatis huruf awal 'p' nya hilang
##      contoh pem- + perkosa = pemerkosa, pem- + panah = pemanah, pem- + proses = pemroses

## beberapa imbuhan special lainnya: mem.per, ber.ke
## beberapa kata masih sulit seperti: pengasapan -> berhubung dikamus jg ada kata kasap, dalam konteks ini harusnya
##      yang diperoleh adalah asap sebagai rootnya
#####################################################################################################################################

import string, re,sys
from collections import defaultdict
from tokenizer import tokenize
from collections import OrderedDict

if __package__ is None:
   from os import path
   sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
   from utils.autovivified import AutoVivification
else:
   from utils.autovivified import AutoVivification
   
class ChaosStemmer:
  ###### Define class attribute ######
  # As per 2015-10-03, kita rubah struktur storage dari prefix, suffix, infix dan vokal
  #      dari dict(list) => dict(tupple)
  # Why? please visit: http://stackoverflow.com/questions/1708510/python-list-vs-tuple-when-to-use-each
  prefix = {2:('pe', 'di', 'se', 'ke', 'me','be','si','te'), 3:('ber', 'mem', 'men', 'pem', 'pen', 'per',  'ter', 'nyo','pel','bel'),
            4:('meng', 'meny', 'peng', 'peny'), 5:('menge',  'penge')}
  suffix = {1:('i'), 2:('an','in','ku','mu'), 3:('kan','lah', 'kah', 'nya','pun')}
  infix = {2:('el', 'em', 'er')}
  vokal = ('a','i','u','e','o')
  
  foundsuffix = defaultdict(list)
  guessword = []

  foundedRootWord=''
  hasSpecial = False
  
  
  def __init__(self, langdbfolder, datasetname, forcefindinfix=False):
    #### Define instance attribute ####
    self.languageDBFolder = langdbfolder
    self.datasetName = datasetname

  def isInWordlistCsv(self, word):
    ## disini saya tidak peduli dengan urutan kata, pada dataset "kamus kata dasar"
    ## dan seluruh kata dasar pada kamus unique(tidak ada duplikasi)
    ## dan fungsi ini akan sering sekali dipakai, karena itu saya lebih memilih menggunakan
    ##   set() dari pada list()
    #wordlist = [line.strip() for line in open(self.languageDBFolder + self.datasetName)]
    wordlist = set(open(self.languageDBFolder + self.datasetName).read().splitlines())
    if word in wordlist:
      return True
    else:
      return False

  def getFoundSuffix(self):
    # List dari seluruh kemungkinan affix yang terobservasi pada proses pengecekan affix
    # --- list akan tereset apabila kata memiliki spesial affix ---
    # --- karena itu jika ingin tetap memiliki seluruh sample,
    # ---   buat saja satu lagi attribute yang tidak akan tereset ---
    return self.foundsuffix

  def getFoundGuessWord(self):
    # Berisikan seluruh kemungkinan guessword, akan tetapi belum teruji
    # untuk setiap samplenya, apakah sample ada dalam "kamus kata dasar" apa tidak
    return self.guessword

  def getFilteredGuessWord(self):
    # Berisikan seluruh kemungkinan guessword, sudah teruji
    # untuk setiap samplenya, apakah sample ada dalam "kamus kata dasar" apa tidak
    # OrderedDict.fromkeys() => digunakan untuk menghapus duplikasi pada list
    return list(OrderedDict.fromkeys(filter(lambda x: self.isInWordlistCsv(x) is True and len(x) > 1, self.getFoundGuessWord())))

  def getRootWord(self):
    # Berisi root word
    return self.foundedRootWord

  ##################################################################################
  ######################## START AFFIX GETTER REGION ###############################
  def findPrefix(self,wordtofind):
    for k,v in self.prefix.iteritems():
      for prefixChr in v:
        if wordtofind[0:len(prefixChr)] == prefixChr:
          if prefixChr not in self.foundsuffix['prefix']:
              self.foundsuffix['prefix'].append(prefixChr)

  def findSuffix(self,wordtofind):
    for k,v in self.suffix.iteritems():
      for suffixChr in v:
        if wordtofind[-len(suffixChr):] == suffixChr:
          if suffixChr not in self.foundsuffix['suffix']:
            self.foundsuffix['suffix'].append(suffixChr)

  def findInfix(self,wordtofind):
    for k,v in self.infix.iteritems():
      for infixChr in v:
        if re.search(r''+infixChr+'',wordtofind):
          if infixChr not in self.foundsuffix['infix']:
            self.foundsuffix['infix'].append(infixChr)
  ######################## END AFFIX GETTER REGION ##################################
  ###################################################################################
            
  def initAffix(self,wordtofind,whattofind):
    newword = ''
    if whattofind == 1: #Proses prefix
      self.findPrefix(wordtofind)
    elif whattofind == 2: #Proses suffix
      self.findSuffix(wordtofind)
    elif whattofind == 3: #Proses infix
      self.findInfix(wordtofind)


  def specialAffixFormer(self, wordtoprocess):    
    naffix=''
    if 'prefix' in self.foundsuffix:
      # Transformasi affix
      if 'meny' in self.foundsuffix['prefix']:
        self.hasSpecial=True
        naffix = 's'
      elif 'meng' in self.foundsuffix['prefix']:
        self.hasSpecial=True
        naffix = 'k'
      elif 'peny' in self.foundsuffix['prefix']:
        self.hasSpecial=True
        naffix = 's'
      elif 'men' in self.foundsuffix['prefix']:
        self.hasSpecial=True
        naffix = 't'
      elif 'mem' in self.foundsuffix['prefix']:
        self.hasSpecial=True
        naffix = 'p'
      elif 'penge' in self.foundsuffix['prefix']:
        self.hasSpecial=True
        naffix = 'k'
      elif 'peng' in self.foundsuffix['prefix']:
        self.hasSpecial=True
        naffix = 'k'
      elif 'pem' in self.foundsuffix['prefix']:
        self.hasSpecial=True
        naffix = 'p'
      elif 'pen' in self.foundsuffix['prefix']:
        self.hasSpecial=True
        naffix = 't'
      elif 'ter' in self.foundsuffix['prefix']:
        self.hasSpecial=True
        naffix = 'r'
      elif 'nyo' in self.foundsuffix['prefix']:
        self.hasSpecial=True
        naffix = 'co'
        
    # Cek apakah huruf pertama pada kata adalah vokal
    if wordtoprocess[:1] in self.vokal:
      procword=''
      if self.hasSpecial:
        ## Routine disini mungkin harus dirubah, pertimbangkan procword menjadi list
        ## untuk mengatasi kata dengan spesial affix seperti:
        ##      mengodekan => root word yang betul adalah "kode"
        ##      tetapi karena "ode" juga terdapat pada dataset, "kode" jadi tidak tertangkap
        #print wordtoprocess 
        if self.isInWordlistCsv(naffix+wordtoprocess): #<= karena ini kepengurusan root nya jadi kurus, harusnya urus
          procword = naffix+wordtoprocess
        else:
           if self.isInWordlistCsv(wordtoprocess):
              procword = wordtoprocess

        if not procword and self.isInWordlistCsv(naffix+wordtoprocess):
          procword = naffix+wordtoprocess

        # Benar-benar default untuk kata yang memiliki spesial affix,
        # apapun itu, jika proses diatas tidak menghasilkan apapun,
        # spesial affix harus ditambahkan dengan char naffix
        if not procword:
          procword = naffix+wordtoprocess 
      else:
        procword = wordtoprocess
    else:
      if self.isInWordlistCsv(naffix+wordtoprocess):
          procword = naffix+wordtoprocess
      else:
        procword = wordtoprocess

    if len(procword)>=3:
       procword=procword
    else:
       procword=''
    
    return procword

  def affixGetter(self,wordtofind):
    wordsBySuffixforPrefix=[]
    getTrue=0

    for k, v in self.foundsuffix.iteritems():
      if k == 'prefix':
        if 'suffix' in self.foundsuffix:
          # ada suffix, berarti kata berupa confix
          for z in self.foundsuffix['suffix']:
            # Beberapa transformasi suffix tambahan yang akan menambah kamus guessword
            if z == 'i' or z == 'ku' or z == 'mu' or z == 'in' or z == 'nya' \
               or z == 'an' or z == 'kah' or z == 'lah' or z == 'pun':              
              wordsBySuffixforPrefix.append(wordtofind)
              self.guessword.append(wordtofind)
            if wordtofind[:-len(z)] > 1:
               #print wordtofind,wordtofind[:-len(z)]
               wordsBySuffixforPrefix.append(wordtofind[:-len(z)])
               self.guessword.append(wordtofind[:-len(z)])
          
        # Jika kata memiliki affix: prefix dan suffix yang disebut dengan affix: confix
        if wordsBySuffixforPrefix!=[]:
          for affix in v:
            for z in range(len(wordsBySuffixforPrefix)):
              if wordsBySuffixforPrefix[z][len(affix):] not in self.guessword:
                # Beberapa transformasi prefix tambahan yang akan menambah kamus guessword
                # hal ini dibutuhkan karena ada beberapa kata dasar yang ternyata memiliki awalan
                # yang terdapat pada affix
                # contoh: ketok, kerok, pesawat
                procword = self.specialAffixFormer(wordsBySuffixforPrefix[z][len(affix):])
                if affix == 'pe' or affix == 'se' or affix == 'be' or affix == 'me' \
                   or affix == 'si' or affix == 'ke' or affix == 'te':
                  if affix+procword not in self.guessword and affix+procword != wordtofind:
                    self.guessword.append(affix+procword)
                if len(procword) > 1 and procword != wordtofind:
                   self.guessword.append(procword)
        else:
          for affix in v:
            # Kata hanya affix: prefix
            if wordtofind[len(affix):] not in self.guessword:
              procword = self.specialAffixFormer(wordtofind[len(affix):])
              if len(procword) > 1 and procword != wordtofind:
                 self.guessword.append(procword)
              
      elif k == 'suffix' and 'prefix' not in self.foundsuffix:          
        # Kata hanya affix: suffix
        for z in self.foundsuffix['suffix']:
          if wordtofind[:-len(z)] not in self.guessword:
            # Beberapa transformasi suffix tambahan yang akan menambah kamus guessword
            if z == 'i' or z == 'ku' or z == 'mu' or z == 'in' or z == 'nya' \
               or z == 'an' or z == 'kah' or z == 'lah' or z == 'pun':
              self.guessword.append(wordtofind)
            if len(wordtofind[:-len(z)]) > 1 and wordtofind[:-len(z)] not in self.guessword:
               self.guessword.append(wordtofind[:-len(z)])
 
    for z in self.guessword: 
      procword = self.specialAffixFormer(z)
      if self.isInWordlistCsv(z):
        getTrue=1
        # Masukkan sampel jika terdapat dalam kamus kata dasar
        self.foundedRootWord = z
        break
      else:
         if self.isInWordlistCsv(procword):
            getTrue=1
            # Masukkan sampel jika terdapat dalam kamus kata dasar
            self.foundedRootWord = procword
            break

    if getTrue==0:
      for z in self.foundsuffix['prefix']:
        for y in self.guessword:
          procword = self.specialAffixFormer(z+y)
          if self.isInWordlistCsv(procword):
            # Masukkan sampel jika terdapat dalam kamus kata dasar
            self.foundedRootWord = procword
            break
         
  def redupChecker(self, wordtoprocess):
     # Pengecekan reduplikasi kata seperti: bermalas-malasan, bersiul-siulan
     # pada dasarnya kita cukup mengembalikan kata pertama saja untuk diproses
     # mencari root wordnya
     """
         kenapa search string menggunakan 'in'?
         please reffer to: http://stackoverflow.com/questions/4901523/whats-a-faster-operation-re-match-search-or-str-find
     """
     if "-" in wordtoprocess:
        firstWord = wordtoprocess.split('-',1)[0]
     else:
        firstWord=wordtoprocess
     
     return firstWord 
  
  def stemm(self,wordtofind):
    # Clear any kind of class attribute
    self.foundsuffix = defaultdict(list)
    self.guessword = []
    self.foundedRootWord=''
    self.hasSpecial=False

    # Paling awal, pengecekan reduplikasi pada kata
    wordtofind = self.redupChecker(wordtofind)
    
    # Cek dahulu, apakah kata yang diinput sudah berbentuk kata dasar
    if self.isInWordlistCsv(wordtofind)==True:
      self.foundedRootWord=wordtofind

    def processes(wordinprocess):
      for i in range(1,4):
        if i ==3:
          # self.affixGetter() => akan mentransformasi kata input sesuai dengan parameter affix yang ditemukan 
          self.affixGetter(wordinprocess)
          
          # kalau belum ketemu root word, baru cari kemungkinan infix
          if self.foundedRootWord =='':
             if 'meny' not in self.foundsuffix['prefix'] :
               # kata yang di proses di infix, harus sudah bersih dari prefix dan suffix
               if 'suffix' in self.foundsuffix:
                 for z in self.foundsuffix['suffix']:
                   for y in range(len(self.guessword)):
                     #self.guessword[y] = self.guessword[y]+z
                     self.initAffix(self.guessword[y]+z,i)
                     if 'infix' in self.foundsuffix:
                       for x in self.foundsuffix['infix']:
                         if self.isInWordlistCsv(self.guessword[y].replace(x,'')+z)==True and len(self.guessword[y].replace(x,'')+z) >1:
                           self.foundedRootWord=self.guessword[y].replace(x,'')+z
                           break
                         
               else:
                 if len(self.guessword) > 0:
                   for y in range(len(self.guessword)):  
                     self.initAffix(self.guessword[y],i)
                     if 'infix' in self.foundsuffix:
                       for x in self.foundsuffix['infix']:
                         # harus diingat bahwa infix tidak mungkin berada diawal
                         try:
                            infixIndex =  self.guessword[y].index(x)
                         except ValueError:
                            pass

                         if infixIndex !=0 :
                            if self.isInWordlistCsv(self.guessword[y].replace(x,''))==True and len(self.guessword[y].replace(x,'')) >1:
                              self.foundedRootWord=self.guessword[y].replace(x,'')
                              break
                 else:
                   self.initAffix(wordinprocess,i)
                   if 'infix' in self.foundsuffix:
                     for x in self.foundsuffix['infix']:
                       if self.isInWordlistCsv(wordinprocess.replace(x,''))==True and len(wordinprocess.replace(x,'')) >1: 
                         self.foundedRootWord=wordinprocess.replace(x,'')
                         break
            
        else:
          self.initAffix(wordinprocess,i)
          
        i+=1

    # Sebetulnya kita dapat mencari tau seberapa dalam affix yang ada pada suatu kata
    # dengan melihat beberapa banyak perbedaan karakter awal pada suatu affix,
    # karena setiap spesial affix pada bahasa Indonesia pasti memili karakter awal yang berbeda.
    # Hal ini saya simpulkan karena sejauh apa yang sudah saya lakukan, 
    # saya belum menemukan untuk setiap kata berimbuhan pada spesial affix,
    # setiap affix vektornya memiliki karakter awal yang sama
    #   Contoh: memperhalus
    #           terdiri dari prefix: 'm'em- dan 'p'er-
    #@@@@@@@@@@@@@@ CONTOH @@@@@@@@@@@@@@@
    #> Berapa banya cara untuk menyususun suatu prefix dari kata diatas(memperhalus),
    #   dimana diketahui ada 4 prefix yang berbeda(me,mem)(pe,per),
    #	dan 2 grup prefix dasar yang harus dipilih dengan memperhatikan posisi, dimana setiap grup hanya boleh dipilih 1
    # grup1:
    #    me, mem => permutasi(2,1) = 2!/(2-1)!=2
    # grup2:
    #    pe, per => permutasi(2,1) = 2!/(2-1)!=2
    # maka kita akan mendapatkan 4 kali jumlah perulangan dalam pembentukan prefix gabungan
    # tentu saja jumlah akhir perulangan harus ditambahkan hasil banyaknya suffix gabungan dan infix    
    ###############################################################################################
    # Jika ternyata ada kata berimbuhan yang memiliki spesial affix, misal saja untuk
    # kondisi gabungan prefix yang sama, maka asumsi ini tidak bisa digunakan
    ttlloop=1
    while not self.foundedRootWord:
      if ttlloop>=5:
        print "Word: ", wordtofind, " -> Causing potential infinite loop"
        break
      ttlloop+=1
      processes(wordtofind)

      if not self.foundedRootWord:
        if self.guessword!=[]:
          totaltolerance=0
          for z in self.guessword:
            if self.isInWordlistCsv(z)==True:
              self.foundedRootWord=z
              break
            else:
              self.foundsuffix=defaultdict(list)
              processes(z)
              if not self.foundedRootWord:
                totaltolerance+=1
                self.guessword.remove(z)

            if totaltolerance == len(self.guessword) or totaltolerance > len(self.guessword):
              self.foundedRootWord="none"
              break
        else:
          self.foundedRootWord="none"
          break

      if self.foundedRootWord=="none" and len(self.getFoundGuessWord())>0:
        self.foundedRootWord='' 
        for z in self.getFoundGuessWord():
          self.foundsuffix=defaultdict(list)
          processes(z)

          if not self.foundedRootWord:
            self.guessword.remove(z)
          else:
             if self.isInWordlistCsv(self.foundedRootWord)==False:
                self.foundedRootWord=''
                self.guessword.remove(z)
             else:
                break
            
        if not self.foundedRootWord or self.foundedRootWord=='none':
           self.foundedRootWord='none'
           break
            
      
############################33##### FOR TESTING PURPOSE ONLY #########################3##############
def stemm_test():
  #from functools import partial
  
  morph = ChaosStemmer('C:\\BimaNLP\\dataset\\','tb_katadasar.txt')
  
  f = open('C:\\BimaNLP\\dataset\\tb_kataberimbuhan.txt')
  kata = f.readlines()
  tok = tokenize()
  kata = tok.WordTokenize(''.join(kata))
  ttl = len(kata)
  print "Checking stemmer algoritm againts '", ttl, "' word with affix"
  print "#############################################################################################3"
  i=0
  unresolvedword=[]
  #multipleguessword = defaultdict(partial(defaultdict, list))
  multipleguessword = AutoVivification()
  for z in kata:
    i+=1
    print i, " Getting rootword for word: ",z
    morph.stemm(z)
    rootword=morph.getRootWord()
    filterguessword=morph.getFilteredGuessWord()
    print "\t","and rootword is: ",rootword
    if rootword=='none':
      if z not in unresolvedword:
        unresolvedword.append(z)

    if len(filterguessword)>1 or len(filterguessword)<1:
      if rootword!='none':
        multipleguessword[z][rootword] = filterguessword

  if unresolvedword!=[]:
    print "Get total unresolved word: ", len(unresolvedword)
    print "Member of unresolved word: ", unresolvedword
    print "\n"

  print "#############################################################################################3"
  if filterguessword!=[]:
    print "Get total of multiple guessword: ", len(multipleguessword)
    print "Member of multiple guessword: "
    for k,v in multipleguessword.iteritems():
       print k," => ", v

#stemm_test()
#################################################################################################3####
