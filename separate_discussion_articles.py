file_discussion=open('Discussion_FA.txt','r')
file_articles=open('Final_Articles_FA.txt','r')
for line_articles in file_articles:
 focal_article=line_articles.split(';')[1].strip('\n')
 file_discussion=open('Discussion_FA.txt','r')
 for line_discussion in file_discussion:
  article=line_discussion.split(';')[1]
  if focal_article==article:
   file_separate=open(focal_article_'discussion.txt','a')
   file_separate.write(line_discussion.strip('\n')+"\n")
   file_separate.close()
