file_titles=open('Missing_Titles_C.txt','r')


for line_titles in file_titles:
 focal_title=line_titles.strip('\n')
 print "Now for article: ", focal_title
 file_articles=open('Full_Article_Milestones_C.txt','r')
 for line_articles in file_articles:
  title=line_articles.split(';')[0]
  mile_stone=line_articles.split(';')[1].strip('\n')
  if focal_title.translate(None,"-")==title:
   file_missing1=open('Missing_Milestones_C.txt','a')
   file_missing1.write(str(focal_title)+";"+str(mile_stone)+"\n")
   file_missing1.close()
   #break
  