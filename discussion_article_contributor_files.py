
page_list=open('Final_Page_Titles_B.txt','r')
for line in page_list:
 focal_article=line.strip('\n')
 print "Now for Article : ", focal_article
 article_contributors=list()
 article_contributors_file=open('Comprehensive_Contributors_B.txt','r')
 for line_article in article_contributors_file:
  article=line_article.split(';')[0] 
  if article==focal_article:
   for i in range(1,len(line_article.split(';'))-1):
    article_contributors.append(line_article.split(';')[i])
   break
 discussion_contributor_file=open('Discussion_Contributor_B.txt','r')
 discussion_contributors=list()
 for discussion_line in discussion_contributor_file:
  article_1=discussion_line.split(';')[0]
  if article_1==focal_article:
   discussion_contributors.append(discussion_line.split(';')[1].strip('\n'))
 only_disc=list(set(set(discussion_contributors)-set(article_contributors)))
 only_article=list(set(set(article_contributors)-set(discussion_contributors)))
 disc_and_article=list(set(set(article_contributors).intersection(set(discussion_contributors))))
 for od in only_disc:
  file_only_disc=open('Only_Discussion_B.txt','a')
  file_only_disc.write("B;"+str(focal_article)+";"+str(od)+"\n")
  file_only_disc.close()
 for oa in only_article:
  file_only_article=open('Only_Article_B.txt','a')
  file_only_article.write("B;"+str(focal_article)+";"+str(oa)+"\n")
  file_only_article.close()
 for da in disc_and_article:
  file_disc_article=open('Disc_Article_B.txt','a')
  file_disc_article.write("B;"+str(focal_article)+";"+str(da)+"\n")
  file_disc_article.close()
 