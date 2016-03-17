####
import difflib
import wikipedia
import sys
import re
import os
import urllib2
from pprint import pprint
import datetime
from nltk.tokenize import sent_tokenize
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.etree.ElementTree as ET
import os

def load_article_milestones():
 article_milestones=open('Full_Article_Milestones_FA.txt','r')
 print "Populating Article Milestones"
 for line_milestone in article_milestones:
  temp_date=line_milestone.split(';')[1].strip('\n')
  article_milestone_dict[line_milestone.split(';')[0]]=datetime.date(int(temp_date[0:4]),int(temp_date[4:6]),int(temp_date[6:len(temp_date)]))
  article_names_list.append(line_milestone.split(';')[0])
 print "Populating Done"


def get_relevant_edits(name):
 revisions_file=open('FA_Article_Revision_ids_NEWER.txt','r')
 relevant_edits=list()
 print "Getting the Relevant Edits for :", name
 for rev_line in revisions_file:
  article_name=rev_line.split(';')[0]
  flag=0
  if article_name==name:
   flag=1
   revid=rev_line.split(';')[1]
   parent_id=int(rev_line.split(';')[2])
   minor=rev_line.split(';')[3]
   user=rev_line.split(';')[4]
   time_stamp=rev_line.split(';')[5].strip('\n')
   size=rev_line.split(';')[6].strip('\n')
   rev_time_stamp=datetime.date(int(time_stamp[0:4]),int(time_stamp[5:7]),int(time_stamp[8:10]))
   if (rev_time_stamp<=article_milestone_dict[name]):
    relevant_edits.append(rev_line.strip('\n'))
  if flag==1 and article_name!=name:
   break
 print "Getting Relevant Edits Now Complete"  
 return relevant_edits
 
 

  
def segregate_discussions(name):
 file_revisions=open('FA_Article_Revision_ids_NEWER.txt','r')
 file_discussions=open('Comment_Text_Labels_Comprehensive_11.txt','r')
 print "Now segregating the discussions for :", name
 for line in file_discussions:
  article_name=line.split('\t')[1].strip('\n')
  flag=0
  if article_name==name:
   flag=1
   file_article_discussion=open(article_name+'_disc_FA.txt','a')
   file_article_discussion.write(line.strip('\n')+"\n")
   file_article_discussion.close()
  if article_name!=name and flag==1:
   break
 print "Segregating discussions now complete"
   
def segregate_discussions_periods(name,edit_list):
  print "Now Segregating the discussion periods for :", name
  for i in range(0,len(edit_list)-2):
   edit1=edit_list[i]
   edit2=edit_list[i+1]
   time_stamp_1=edit1.split(';')[5].strip('\n')
   edit1_ts=datetime.date(int(time_stamp_1[0:4]),int(time_stamp_1[5:7]),int(time_stamp_1[8:10]))
   time_stamp_2=edit2.split(';')[5].strip('\n')
   edit2_ts=datetime.date(int(time_stamp_2[0:4]),int(time_stamp_2[5:7]),int(time_stamp_2[8:10]))
   file_article_discussion=open(name+'_disc_FA.txt','r')
   for disc_line in file_article_discussion:
    ts_disc=str(disc_line.split('\t')[6].strip('\n'))
    month=int(time_stamp.split('/')[0])
    day=int(time_stamp.split('/')[1])
    year=int(time_stamp.split('/')[2].strip('\n').split(' ')[0])
    hour=int(time_stamp.split('/')[2].strip('\n').split(' ')[1].split(':')[0])
    minute=int(time_stamp.split('/')[2].strip('\n').split(' ')[1].split(':')[1])
    date_string=str(year)+'-'+str(month)+'-'+str(day)+' '+str(hour)+':'+str(minute)
    modified_ts=datetime.strptime(date_string,"%Y-%m-%d %H:%M")
    if i==1 and modified_ts<edit1_ts:
	 file_final_disc_periods=open(name+'_disc_periods_FA.txt','a')
	 file_final_disc_periods.write(str(disc_line.strip('\n'))+"~;"+str(i)+"\n")
	 file_final_disc_periods.close()
	elif modified_ts>=edit1_ts and modified_ts<edit2_ts:
	 file_final_disc_periods=open(name+'_disc_periods_FA.txt','a')
	 file_final_disc_periods.write(str(disc_line.strip('\n'))+"~;"+str(i)+"\n")
	 file_final_disc_periods.close()
  print "Segregating Discussion Periods now complete"  	 
	 
	
    	
   
 
def count_type_of_discussions(name):
 file_final_disc_periods=open(name+'_disc_periods_FA.txt','a')
#first determing the maximum periods
 max=0
 print "Now counting the type of discussions for :", name
 for disc_line in file_final_disc_periods:
  disc_period=int(disc_line.split('~;')[1].strip('\n'))
  if disc_period>max:
   max=disc_period
 file_final_disc_periods_1=open(name+'_disc_periods_FA.txt','a')   
 for period in range(1,max+1):
  for disc_line in file_final_disc_periods_1:
   disc_period=int(disc_line.split('~;')[1].strip('\n'))
   if disc_period==period: 
    for line_1 in file_labels:
     Article_Comment_Count+=1
     article_name=line_1.split('\t')[1]
     #print "Article_Name:",article_name
     labels_line=line_1.split('--')[1].split('~;')[0].strip('\n')
     labels=list(labels_line.split(';'))
     for x in range(0,len(labels)-1):
      if labels[x]=="ACKNOWLEDGEMENT":
 	   Acknowledgement+=1
      if labels[x]=="OTHERS":
 	   others+=1 
      if labels[x]=="SOURCES_AND_REFERENCES":
 	   sources_references+=1	 
      if labels[x]=="IMAGES":
 	   images+=1	 
      if labels[x]=="FONT_FORMAT":
 	   format+=1
      if labels[x]=="APPRECIATION":
        Appreciation+=1
      if labels[x]=="SUMMARY":
       Summary+=1
      if labels[x]=="SUGGESTION":
       Suggestion+=1
      if labels[x]=="CLARIFICATION":
       Clarification+=1	 
    Final_File_Normalized=open(name+'_CommentType_Counts_Comprehensive_Final_Normalized.txt','a')
    Final_File_Normalized.write(str(period)+";"+str(Acknowledgement/float(Article_Comment_Count))+";"+ str(others/float(Article_Comment_Count))+";"+str(sources_references/float(Article_Comment_Count))+";"+str(images/float(Article_Comment_Count))+";"+str(format/float(Article_Comment_Count))+";"+str(Appreciation/float(Article_Comment_Count))+";"+str(Summary/float(Article_Comment_Count))+";"+str(Suggestion/float(Article_Comment_Count))+";"+str(Clarification/float(Article_Comment_Count))+"\n")
    Final_File_Normalized.close() 
  
def get_edit_type_vector(edit_1,edit_2):
 editor_actions=list()
 editors=edit_2.strip().split(';~')[4]
#first we need to get the text for edit_1 and edit_2 using Mediawiki API
 article_name=edit_1.split(';')[0]
 add_sentence=0;delete_sentence=0;modify_sentence=0;add_link=0;add_reference=0;
 
 url1="http://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles="+article_name+"&rvstartid="+edit_1.split(';')[1]+"&rvendid="+edit_1.split(';')[1]+"&rvprop=content&format=xml"
 req1 = urllib2.Request(url1)
 response1 = urllib2.urlopen(req1)
 xml_file1=open(name+'_1_Rev.xml','a')
 xml_file1.write(response1.read())
 xml_file1.close()
 tree1 = ET.parse(name+'_1_Rev.xml')
 root1 = tree1.getroot()
 rev_text1= root1.findall('query')[0].find('pages').find('page').find('revisions').find('rev').text
 text_1=rev_text1.encode("utf-8").rstrip('\r\n').lstrip('\r\n').replace("\n","").replace("\r","")
 
 
 url2="http://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles="+article_name+"&rvstartid="+edit_2.split(';')[1]+"&rvendid="+edit_2.split(';')[1]+"&rvprop=content&format=xml"
 req2 = urllib2.Request(url2)
 response2 = urllib2.urlopen(req2)
 xml_file2=open(name+'_2_Rev.xml','a')
 xml_file2.write(response1.read())
 xml_file2.close()
 tree2 = ET.parse(name+'_2_Rev.xml')
 root2 = tree2.getroot()
 rev_text2= root2.findall('query')[0].find('pages').find('page').find('revisions').find('rev').text
 text_2=rev_text2.encode("utf-8").rstrip('\r\n').lstrip('\r\n').replace("\n","").replace("\r","")
 
 sent_tokenize_list1 = unicode(text_1.replace('"', '\\"'),errors='ignore')
 sent_tokenize_list2 = unicode(text_2.replace('"', '\\"'),errors='ignore')

 d = difflib.Differ()
 for line in d.compare(sent_tokenize_list1.splitlines(), sent_tokenize_list2.splitlines()):
  if line.startswith("+"):
   add_sentence=1
   if re.search(r'\[\[.*\]\]', line, re.M|re.I):
    add_link=1
   if re.search(r'<ref>.*</ref>', line, re.M|re.I):
    add_reference=1
  if line.startswith("-"):
   delete_sentence=1
  if line.startswith("?"):
   if re.search(r'\^', line, re.M|re.I):
    modify_sentence=1
 editor_actions.append(add_sentence)
 editor_actions.append(add_link)
 editor_actions.append(add_reference)
 editor_actions.append(delete_sentence)
 editor_actions.append(modify_sentence)
 return editor_actions
 
def  combine_discussion_edit_type_vectors(name):
 disc_file=open(name+'_CommentType_Counts_Comprehensive_Final_Normalized.txt','r') 
 print "Now combining the discussion and edit vectors for :", name
 for disc_line in disc_file:
  focal_period=int(disc_line.split(';')[0])
  edits_file=open(name+'_edits_vector_FA.txt','a')
  for edit_line in edits_file:
   period=int(edit_line.split(';')[0])
   if focal_period==period:
    disc_vector=[disc_line.split(';')[i] for i in range(1,len(disc_line.split(';'))-1)]
    edit_vector=[edit_line.split(';')[i] for i in range(1,len(edit_line.split(';'))-1)]
    final_file=open('Disc_Edit_Patterns_FA.txt','a')
    final_file.write("FA"+";"+str(str(name).replace(";",""))+";"+str(focal_period)+";"+str(';'.join(disc_vector))+";"+str(';'.join(edit_vector))+"\n")
    final_file.close()
 print " Combining Vector Finished"
	
  
 
 
  
  
 

#starts here
article_milestone_dict={}
article_names_list=list()
load_article_milestones() #first load the milestones in a dictionary

page_titles_file=open('Page_Titles_FA.txt','r')
for line in page_titles_file:
 a_name=line.strip('\n')
 edits_list=get_relevant_edits(a_name) # put the relevant edits in a list
 segregate_discussions(a_name) #segregate the discussions for an article.
 segregate_discussion_periods(a_name,edits_list) #segregate the discussions into various periods by the edits performed
 count_type_of_discussions(a_name) # count the type of discussions for each type of edit
 for i in range(0,len(edits_list)-2):
  edit1=edits_list[i]
  edit2=edits_list[i+1]
  vector=get_edit_type_vector(edit1,edit2)
  file_edits_vector=open(a_name+'_edits_vector_FA.txt','a')
  file_edits_vector.write(str(i)+";"+str(';'.join(vector))+"\n")
  file_edits_vector.close()
 combine_discussion_edit_type_vectors(a_name) #combine the discussion and edit type vectors

