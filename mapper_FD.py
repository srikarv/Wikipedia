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

editor_actions_binary=list()
editor_actions=list()
add_sentence_binary=0;delete_sentence_binary=0;modify_sentence_binary=0;add_link_binary=0;delete_link_binary=0;modify_link_binary=0;add_reference_binary=0;delete_reference_binary=0;modify_reference_binary=0;
add_sentence=0;delete_sentence=0;modify_sentence=0;add_link=0;delete_link=0;modify_link=0;add_reference=0;delete_reference=0;modify_reference=0;   
lines=list()
for line in sys.stdin:
 lines.append(line)
#print len(lines)
text1=lines[0].replace('"', '\\"').strip('\n')
text2=lines[1].replace('"', '\\"').strip('\n')
#print "Text 1:", text1
#print "Text 2:", text2
user1=text1.split(';~')[4].strip()
user2=text2.split(';~')[4].strip()
sent_tokenize_list1 = unicode(text1.split(';~')[7].replace('"', '\\"'),errors='ignore')
sent_tokenize_list2 = unicode(text2.split(';~')[7].replace('"', '\\"'),errors='ignore')
d = difflib.Differ()
for line in d.compare(sent_tokenize_list1.splitlines(), sent_tokenize_list2.splitlines()):
  if line.startswith("+"):
 #  print "Inside Plus"
   if re.search(r'\[\[.*\]\]', line, re.M|re.I)==False and re.search(r'<ref>.*</ref>', line, re.M|re.I)==False:
    add_sentence_binary=1
    add_sentence=+1
   else:
    if line[1:].startswith('\[\[') and line[1:].endswith('\]\]') and line[1:].count('\[\[')==1 and line[1:].count('\]\]')==1:
     add_link_binary=1
     add_link+=1
    elif line[1:].startswith('<ref>') and line[1:].endswith('</ref>') and line[1:].count('<ref>')==1 and line[1:].count('</ref>')==1:
     add_reference_binary=1
     add_reference+=1
    elif re.search(r'<ref>.*</ref>', line, re.M|re.I) and re.search(r'\[\[.*\]\]', line, re.M|re.I):
     add_reference_binary=1
     add_reference+=1
     add_link_binary=1
     add_link+=1
     add_sentence_binary=1
     add_sentence=+1
    elif re.search(r'<ref>.*</ref>', line, re.M|re.I):
     add_reference_binary=1
     add_reference+=1
     add_sentence_binary=1
     add_sentence=+1
    elif re.search(r'\[\[.*\]\]', line, re.M|re.I):
     add_link_binary=1
     add_link+=1
     add_sentence_binary=1
     add_sentence=+1
  elif line.startswith("-"):
  # print "Inside Minus"
   if re.search(r'\[\[.*\]\]', line, re.M|re.I)==False and re.search(r'<ref>.*</ref>', line, re.M|re.I)==False:
    delete_sentence_binary=1
    delete_sentence=+1
   else:
    if line[1:].startswith('\[\[') and line[1:].endswith('\]\]') and line[1:].count('\[\[')==1 and line[1:].count('\]\]')==1 :
     delete_link_binary=1
     delete_link+=1
    elif line[1:].startswith('<ref>') and line[1:].endswith('</ref>') and line[1:].count('<ref>')==1 and line[1:].count('</ref>')==1 :
     delete_reference_binary=1
     delete_reference+=1
    elif re.search(r'<ref>.*</ref>', line, re.M|re.I) and re.search(r'\[\[.*\]\]', line, re.M|re.I):
     delete_reference_binary=1
     delete_reference+=1
     delete_link_binary=1
     delete_link+=1
     delete_sentence_binary=1
     delete_sentence=+1
    elif re.search(r'<ref>.*</ref>', line, re.M|re.I):
     delete_reference_binary=1
     delete_reference+=1
     delete_sentence_binary=1
     delete_sentence=+1
    elif re.search(r'\[\[.*\]\]', line, re.M|re.I):
     delete_link_binary=1
     delete_link+=1
     delete_sentence_binary=1
     delete_sentence=+1
  elif line.startswith("?"):
   #print "Inside Question Mark"
   search_list=list(line.split(' '))
   for element in search_list:
    if element!=' ':
	   ele_length=len(element)
	   start_index=line.find(element)
	   substring=prev_line[start_index:start_index+ele_length]
	   if re.search(r'\[\[.*\]\]', substring, re.M|re.I)==False and re.search(r'<ref>.*</ref>', substring, re.M|re.I)==False:
	    modify_sentence_binary=1
	    modify_sentence=+1
	   else:
	    if substring[1:].startswith('\[\[') and substring[1:].endswith('\]\]') and substring[1:].count('\[\[')==1 and substring[1:].count('\]\]')==1 :
	     modify_link_binary=1
	     modify_link+=1
	    elif substring[1:].startswith('<ref>') and substring[1:].endswith('</ref>') and substring[1:].count('<ref>')==1 and substring[1:].count('</ref>')==1 :
	     modify_reference_binary=1
	     modify_reference+=1
	    elif re.search(r'<ref>.*</ref>', substring, re.M|re.I) and re.search(r'\[\[.*\]\]', substring, re.M|re.I):
	     modify_reference_binary=1
	     modify_reference+=1
	     modify_link_binary=1
	     modify_link+=1
	     modify_sentence_binary=1
	     modify_sentence=+1
	    elif re.search(r'<ref>.*</ref>', substring, re.M|re.I):
	     modify_reference_binary=1
	     modify_reference+=1
	     modify_sentence_binary=1
	     modify_sentence=+1
	    elif re.search(r'\[\[.*\]\]', substring, re.M|re.I):
	     modify_link_binary=1
	     modify_link+=1
	     modify_sentence_binary=1
	     modify_sentence=+1
  prev_line=line
  		
editor_actions.append(add_sentence)
editor_actions.append(delete_sentence)
editor_actions.append(modify_sentence)
editor_actions.append(add_link)
editor_actions.append(delete_link)
editor_actions.append(modify_link)
editor_actions.append(add_reference)
editor_actions.append(delete_reference)
editor_actions.append(modify_reference)
print '%s~;%s' % (user2, editor_actions)

