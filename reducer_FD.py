from operator import itemgetter
import sys
import random
import numpy
import pickle
import difflib
import sys
import re
import os
from pprint import pprint
import datetime
from nltk.tokenize import sent_tokenize
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.etree.ElementTree as ET
import os

current_user = None
current_list=list()
for i in range(0,9):
 current_list.append(0)
user = None
sequence_array=[1,4,7,10,13,16,19,22,25]
# input comes from STDIN
for line in sys.stdin:
 line = line.strip()
 print line
 user=line.split('~;')[0];edit_list_temp=line.split('~;')[1].strip('\n')
 edit_list=list()
 for i in sequence_array:
  edit_list.append(int(edit_list_temp[i]))
  #print int(edit_list_temp[i])
 if current_user == user:
  for i in range(0,9):
   current_list[i]+=edit_list[i]
 else:
  if current_user:
   sum_list=0
   for i in range(0,9):
    sum_list+=current_list[i]
   for i in range(0,9):
    current_list[i]=float(current_list[i]/float(sum_list))
   print '%s\t%s' % (current_user, current_list)
  current_list = edit_list
  current_user = user

# do not forget to output the last word if needed!
if current_user == user:
    print '%s\t%s' % (current_user, current_list)

