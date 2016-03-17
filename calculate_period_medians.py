from numpy import *
for i in range(1,51):
 file_articles=open('Final_Page_Titles_C.txt','r')
 values=list()
 for line_article in file_articles:
  count=0
  focal_article=line_article.split(';')[1].strip('\n')
  file_data=open('C_TS_Analysis.txt','r')
  for line_data in file_data:
    section=int(line_data.split('~;')[7].strip('\n'))
    article=line_data.split('~;')[1]
    if section==i and  focal_article==article:
     count+=1
  values.append(count)
 file_avg=open('C_TS_Median.txt','a')
 file_avg.write(str(i)+";"+str(median(values))+"\n")
 file_avg.close()  