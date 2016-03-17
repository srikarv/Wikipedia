file_page_titles=open('Final_Page_Titles_FA.txt',r')
for line_title in file_page_titles:
 focal_grade=line_title.split(';')[0]
 focal_article=line_title.split(';')[1].strip('\n')
 file_input=open(focal_article'_plain_text.txt','r')
 character_count=0
 word_count=0
 sentence_count=0
 Reading_Complexity=0
 for line_input in file_input:
  for character in line_input:
   if (character==' ')
    word_count++
   if (character=='.')
    sentence_count++
   character_count+=1
 Reading_Complexity=(float)(4.71*(character_count/float(word_count))+0.5*(word_count/float(sentence_count))-21.43)
 file_output=open('FA_word_count_RC.txt','a')
 file_output.write(str(focal_grade)+";"+str(focal_article)+";"+str(character_count)+";"+str(word_count)+";"+str(Reading_Complexity)+"\n")
 file_output.close()
 