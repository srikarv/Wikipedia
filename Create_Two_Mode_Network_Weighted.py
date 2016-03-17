import time
import datetime
import os
from datetime import date

file_timestamps=open('Full_Article_Milestones.txt','r')
for line_ts in file_timestamps:
 focal_article_title=line_ts.split(';')[0]
 print "Creating the Network for : ",focal_article_title
 focal_ts=line_ts.split(';')[1].strip('\n')
 focal_year=int(focal_ts[0:4])
 print "Focal_Year: ", focal_year
 focal_month=int(focal_ts[4:6])
 print "Focal_Month: ", focal_month
 focal_day=int(focal_ts[6:8])
 print "Focal_Day: ",focal_day
 focal_date=datetime.date(focal_year,focal_month,focal_day)
 print "Focal Date : ",focal_date
 file_weights=open('Article_Contributor_Combination_TimeStamp.txt','r')
 editors_list=list()
 articles_list=list()
 for line_weights in file_weights:
  time_stamp=line_weights.split('\t')[3]
  article_title=line_weights.split('\t')[1]
  #print "Line_Weights: ",line_weights
  year=int(time_stamp.split('-')[0])
  #print "Year: ",year
  month=int(time_stamp.split('-')[1])
  #print "Month: ", month
  day=int(time_stamp.split('-')[2])
  #print "Day: ", day
  date_ts=datetime.date(year,month,day)
  #print "Date_TS: ", date_ts
  if focal_date>date_ts:
   file_local=open(focal_article_title+'_local_file.txt','a')
   file_local.write(line_weights.strip('\n')+"\n")
   file_local.close()
 file_editors=open('Unique_Editors.txt','r')
 file_articles=open('Unique_Articles.txt','r')
 
 editors_list_dict={}
 articles_list_dict={}
 
 k=1
 for line_articles in file_articles:
  articles_list_dict[k]=line_articles.strip('\n')
  k+=1
 
 article_count=k-1
 for line_editors in file_editors:
  editors_list_dict[k]=line_editors.strip('\n')
  k+=1
 
 editor_count=k-article_count-1
 
 file_network=open('Two_Mode_Wikipedia_Discussion_Network_Weighted_'+focal_article_title+'.NET','a') 
 file_network.write("*Vertices "+str(k)+"\n")
 for article in range(1,article_count+1):
   file_network.write(str(article)+"\""+str(articles_list_dict[article])+"\"\n")
 file_network.close()
 
 file_network=open('Two_Mode_Wikipedia_Discussion_Network_Weighted_'+focal_article_title+'.NET','a') 
 for editor in range(article_count+1,k):
   file_network.write(str(editor)+" \""+str(editors_list_dict[editor])+"\"\n")
 file_network.write("*Edges \n")
 file_network.close()
 inv_article_dict={v: k for k, v in articles_list_dict.items()}
 inv_editor_dict={v: k for k, v in editors_list_dict.items()}
 file_combination=open(focal_article_title+'_local_file.txt','r')
 for line_combination in file_combination:
  focal_article=line_combination.split('\t')[1]
  focal_editor=line_combination.split('\t')[2]
  focal_weight=int(line_combination.split('\t')[4].strip('\n'))
  if inv_article_dict.has_key(focal_article) and inv_editor_dict.has_key(focal_editor):
   file_network=open('Two_Mode_Wikipedia_Discussion_Network_Weighted_'+focal_article_title+'.NET','a')
   file_network.write(str(inv_article_dict[focal_article])+" "+str(inv_editor_dict[focal_editor])+" "+str(focal_weight)+"\n")
   file_network.close()
 file_combination.close()
