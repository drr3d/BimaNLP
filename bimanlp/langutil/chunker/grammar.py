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

########################################################################
# SMT pada grammar saya buat sebagai singkatan dari
#       => likely a SiMilar Token
# dimaksudkan jika suatu token masuk kedalam SMT, token-token tersebut
# memiliki kemungkinan membentuk suatu entitas atau makna tersendiri
# Ataupun bisa bertransformasi bentuk tag nya tergantung jenis kata yang
# mengawali dan mengakhiri
########################################################################

# Perlu diperhatikan, aturan peletakan chunk juga berpengaruh
# chuk parser akan memproses dari yang paling atas dahulu
chunk_grammar = r"""
  PREP: {<PREP><PREP>}     #PREP = Preposisi = kata depan
  TP: {<WP>}
  KP: {<KSUB><ADV>}        #KSUB = kata penghubung/conjunction
  NP: {<N><ADJ|VBI>}
      {<N><N><KKORD><N>}
      {<PREP>?<N><N>}
      }<PREP>{
      {<NUM><N>}
      #{<KP><ADJ>}
  VP: {<KP><VBT|VBI|V>}
      {<V><VBT>}
  SMT1: {<N><N>+}
        {<N><NP>}
  SMT2: {<XX>+}
  SMT3: {<PREP><N>}
  SMT4: {<SMT4>}
  SMT5: {<ADJ><NP|N>}
  SMT6: {<KKORD><XX>+}
  SMT7: {<N><XX>}
        {<XX><N>}
  SMT8: {<NP><N>}
  KET: {<PREP><NP|SMT8>}
       {<PREP><GOL><ADJ>}
  SBJ: {<NP>?<PRON|N|NP|XX|SMT2><PRED>}
       }<PRED>{
  SBJP: {<NP|N><KET><VPASIF|PRED>}
        }<VPASIF|PRED>{
        {<NP|N><VPASIF|PRED>}
        }<VPASIF|PRED>{
  OBJ: {<PRED><N|V|NP>}
       }<PRED>{
  PENJ: {<PREP><ADV|VBI>+}
        {<PREP><SMT5>}
  PRED: {<ADV|PREP><VBI|VBT|V>}
        {<VBT>+}
        {<KP><NP>}
        {<SMT1><ADJ>}
        }<SMT1>{
        {<VBT><SMT1>}
        }<SMT1>{
        {<VBT><NP>}
        }<NP>{
        {<PRON><ADJ>}
        }<PRON>{
        {<KP><ADJ>}
        {<PREP><ADV><ADJ>}
        {<ADV><ADV><ADJ>}
        {<ADV>?<VPASIF>}
"""
