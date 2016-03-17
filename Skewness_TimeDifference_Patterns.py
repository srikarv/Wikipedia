import numpy as np

file_articles=open('Final_Page_Titles.txt','r')

for line in file_articles:
 focal_grade=line.split(';')[0]
 focal_article_name=line.split(';')[1].strip('\n')
 file=open('Time_Stamp_Patterns.txt','r')
 char_counts=list()
 print "Calculating the Skewness for :",focal_article_name
 for line_1 in file:
  #print line_1
  grade=line_1.split(';')[0]
  article_name=line_1.split(';')[1]
  character_count=int(line_1.split(';')[2].strip('\n')) 
  if article_name==focal_article_name:
    char_counts.append(character_count)
    #print "Character Count:",character_count
 if len(char_counts)!=0:
   file_final=open('Time_Reply_Skewness.txt','a')
   file_final.write(str(focal_grade)+";"+str(focal_article_name)+";"+str(np.mean(char_counts))+";"+str(np.median(char_counts))+";"+str(float(np.median(char_counts)/float(np.mean(char_counts))))+"\n")
   file_final.close()
 else:
   file_final=open('Time_Reply_Skewness.txt','a')
   file_final.write(str(focal_grade)+";"+str(focal_article_name)+";"+str(0)+";"+str(0)+"\n")
   file_final.close()
  
   