#This script calculates the average number of comments in each period across all the articles belonging to a particular grade
for i in range(1,4169):
 article_list=list()
 count=0
 file_articles=open('Final_Page_Titles_C.txt','r')
 file_data=open('C_TS_Analysis_Days.txt','r')
 for line_data in file_data:
   section=int(line_data.split('~;')[7].strip('\n'))
   if section==i:
    article_list.append(line_data.split('~;')[1])
    count+=1
 final_article_count=len(set(article_list))
 if final_article_count!=0:
  final_average=count/float(32943)
  file_avg=open('C_TS_Averages_Days_1.txt','a')
  file_avg.write(str(i)+";"+str(final_average)+"\n")
  file_avg.close()  
 else:
  file_avg=open('C_TS_Averages_Days_1.txt','a')
  file_avg.write(str(i)+";"+str(0.0)+"\n")
  file_avg.close()  
  