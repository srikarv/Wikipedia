# -*- coding: utf-8 -*-
import difflib
import wikipedia
import sys
import re
import os
import urllib2
from pprint import pprint
import datetime
#from difflib_data import *
from nltk.tokenize import sent_tokenize
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.etree.ElementTree as ET
import os

#First load the article milestones into a dictionary
article_milestones=open('Full_Article_Milestones_GA.txt','r')
article_milestone_dict={}
article_names_list=list()
for line_milestone in article_milestones:
 #print line_milestone
 temp_date=line_milestone.split(';')[1].strip('\n')
 article_milestone_dict[line_milestone.split(';')[0]]=datetime.date(int(temp_date[0:4]),int(temp_date[4:6]),int(temp_date[6:len(temp_date)]))
 article_names_list.append(line_milestone.split(';')[0])
#Now download the xml files and parse them 
for name in article_names_list:
 revisions_file=open('GA_Article_Revision_ids_NEWER.txt','r')
 print "Now getting the revisions for :", name
 flag=0
 for rev_line in revisions_file:
  article_name=rev_line.split(';')[0]
  if article_name==name:
   #print "Found"
   flag=1
   revid=rev_line.split(';')[1]
   parent_id=int(rev_line.split(';')[2])
   minor=rev_line.split(';')[3]
   user=rev_line.split(';')[4]
   time_stamp=rev_line.split(';')[5].strip('\n')
   size=rev_line.split(';')[6].strip('\n')
   rev_time_stamp=datetime.date(int(time_stamp[0:4]),int(time_stamp[5:7]),int(time_stamp[8:10]))
   #print "Rev_Time_Stamp:",rev_time_stamp
   #print "Article_Milestone:",article_milestone_dict[name]
#start the xml file download and write it to a file
   if (rev_time_stamp<=article_milestone_dict[name]):
    print "Now for Article:",name
    url="http://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles="+name+"&rvstartid="+revid+"&rvendid="+revid+"&rvprop=content&format=xml"
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    xml_file=open(name+'_1_Rev_GA.xml','a')
    xml_file.write(response.read())
    xml_file.close()
    tree = ET.parse(name+'_1_Rev_GA.xml')
    root = tree.getroot()
    rev_text= root.findall('query')[0].find('pages').find('page').find('revisions').find('rev').text
    if rev_text:
	 file_revision_info=open(name+'_rev_text_GA.txt','a')
	 file_revision_info.write(str(name)+";~"+str(revid)+";~"+str(parent_id)+";~"+str(minor)+";~"+str(user)+";~"+str(time_stamp)+";~"+str(size)+";~"+str(rev_text.encode("utf-8").rstrip('\r\n').lstrip('\r\n').replace("\n","").replace("\r",""))+"\n")
	 file_revision_info.close()
    if os.path.exists(name+'_1_Rev_GA.xml'):
      os.remove(name+'_1_Rev_GA.xml')
  if flag==1 and article_name!=name:
    break   