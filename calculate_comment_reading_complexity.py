import numpy as np
file_page_titles=open('All_Articles.txt','r')
for line_title in file_page_titles:
 focal_article=line_title.split(';')[1].strip('\n')
 RC=list()
 print "Now for Article : ", focal_article
 file_input=open('Comprehensive_Comments_Final_C.txt','r')
 for line_input in file_input:
   page_title=line_input.split('~;')[1]
   comment=line_input.split('~;')[2].strip('\n')
   if focal_article==page_title:
    character_count=0
    word_count=0
    sentence_count=0
    Reading_Complexity=0
    for character in line_input:
     if character==' ':
      word_count+=1
     if character=='.':
      sentence_count+=1
     character_count+=1
    if word_count!=0 and sentence_count!=0:	
     Reading_Complexity=(float)(4.71*(character_count/float(word_count))+0.5*(word_count/float(sentence_count))-21.43)
    else:
     Reading_Complexity=0
    RC.append(Reading_Complexity)
 file_output=open('C_Comment_Reading_Complexity.txt','a')
 file_output.write(str(focal_article)+";"+str(np.mean(RC))+";"+str(np.median(RC))+"\n")
 file_output.close()
 RC=list()