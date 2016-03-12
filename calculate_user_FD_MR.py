# CMSC 12300 - Computer Science with Applications 3
# Borja Sotomayor, 2013
#

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

from mrjob.job import MRJob


class MRCalculateUserFD(MRJob):

    def __init__(self, args):
	 lines = [line1.strip() for line1 in sys.stdin]
	 temp_list=list()
	 for i in range(0,len(lines)-1):
	  temp_list.append(lines[i].replace('"', '\\"').strip('\n'))
	  temp_list.append(lines[i+1].replace('"', '\\"').strip('\n'))
	 args=temp_list
	 MRJob.__init__(self, args)
         yield self,args
    def mapper(self, _, lines):
	  editor_actions_binary=list()
	  editor_actions=list()
	  add_sentence_binary=0;delete_sentence_binary=0;modify_sentence_binary=0;add_link_binary=0;delete_link_binary=0;modify_link_binary=0;add_reference_binary=0;delete_reference_binary=0;modify_reference_binary=0;
	  add_sentence=0;delete_sentence=0;modify_sentence=0;add_link=0;delete_link=0;modify_link=0;add_reference=0;delete_reference=0;modify_reference=0;   
	  text1=lines[0].replace('"', '\\"').strip('\n')
	  text2=lines[1].replace('"', '\\"').strip('\n')
	  print "Line 1:", lines
	  print "Line 2:", text2
	  user1=text1.split(';~')[4]
	  user2=text2.split(';~')[4]
	  sent_tokenize_list1 = unicode(text1.split(';~')[7].replace('"', '\\"'),errors='ignore')
	  sent_tokenize_list2 = unicode(text2.split(';~')[7].replace('"', '\\"'),errors='ignore')
	  d = difflib.Differ()
	  for line in d.compare(sent_tokenize_list1.splitlines(), sent_tokenize_list2.splitlines()):
  	    if line.startswith("+"):
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
	  yield(user2,editor_actions)
    def combiner(self, user, editor_actions):
	 consolidated_list=list()
	 if sum(editor_actions)!=0:
	  for i in range(0,9):
	   consolidated_list.append(float(sum(editor_actions[i])/sum(editor_actions)))
	 else:
	  for i in range(0,9):
	   consolidated_list.append(0.0)
	 yield (user2,consolidated_list)
    def reducer(self,user2,consolidated_list):
	 file_user_FD=open('User_FD_GA_Temp_2_MapReduce.txt','a')
	 file_user_FD.write(str(user2)+"~;")
	 for item in consolidated_list:
	  file_user_FD.write(str(item)+"~")
	 file_user_FD.close()
    def steps(self):
     return [self.mr(mapper=self.mapper, combiner=self.combiner,reducer=self.reducer)]

if __name__ == '__main__':
#First load the article milestones into a dictionary
 article_milestones=open('Full_Article_Milestones_GA_2.txt','r')
 article_milestone_dict={}
 article_names_list=list()
 for line_milestone in article_milestones:
  temp_date=line_milestone.split(';')[1].strip('\n')
  print "Date:",temp_date
  article_milestone_dict[line_milestone.split(';')[0]]=datetime.date(int(temp_date[0:4]),int(temp_date[4:6]),int(temp_date[6:len(temp_date)]))
  article_names_list.append(line_milestone.split(';')[0])
 MRCalculateUserFD.run()

