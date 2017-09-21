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

regex_patterns = [
            (r'^-?[0-9]+(.[0-9]+)?$', 'NUM'),
            (r'(\bdi)\w+', 'VPASIF'),
            (r'(\bter)\w+', 'VBI'),
            (r'(\bber)\w+', 'VBI'),
            (r'(?:di)\w+(?:kan)', 'VPASIF'),
            (r'(?:ber)\w+(?:kan)', 'VBI'),
            (r'(?:ke)\w+(?:an)', 'VBI'),
            (r'(?:diper)\w+(?:kan)', 'VPASIF'),
            (r'(\bme)\w+', 'VBT'),
            (r'(\bmemper)\w+', 'VBT'),
            (r'(?:me)\w+(?:kan)', 'VBT'), #untuk ekstrak kata di dalam confix:'(?<=me)\w+(?=kan)'
            (r'(?:me)\w+(?:i)', 'VBT'),
            (r'(?:memper)\w+(?:kan)', 'VBT'),
            (r'(?:memper)\w+(?:i)', 'VBT'),
            (r'[.,;?():]', 'KKORD'),
            (r'\b(\w+)-(\w+)\b', 'REDUPL'), #https://id.wikibooks.org/wiki/Bahasa_Indonesia/Kata_ulang
            (r'"(.*?)"', 'SMT4'), # Find word between double quotes (["])(?:(?=(\\?))\2.)*?\1
            (r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}\b', 'MAILADDR')
            ]
