import numpy as np

file_articles=open('Article_Titles_C.txt','r')
file=open('Character_Count.txt','r')
for line in file_articles:
 focal_article_name=line.strip('\n')
 file=open('Character_Count.txt','r')
 char_counts=list()
 print "Calculating the Skewness for :",focal_article_name
 for line_1 in file:
  article_name=line_1.split('\t')[0]
  character_count=int(line_1.split('\t')[1].strip('\n')) 
  if article_name==focal_article_name:
    char_counts.append(character_count)
    print "Character Count:",character_count
 if len(char_counts)!=0:
   file_final=open('Skewness_Character_Count_C.txt','a')
   file_final.write("FA"+";"+str(focal_article_name)+";"+str(np.mean(char_counts))+";"+str(np.median(char_counts))+"\n")
   file_final.close()
 else:
   file_final=open('Skewness_Character_Count_C.txt','a')
   file_final.write("FA"+";"+str(focal_article_name)+";"+str(0)+";"+str(0)+"\n")
   file_final.close()
  
   