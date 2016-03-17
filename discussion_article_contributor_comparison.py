
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
 only_disc=set(set(discussion_contributors)-set(article_contributors))
 only_article=set(set(article_contributors)-set(discussion_contributors))
 disc_and_article=set(set(article_contributors).intersection(set(discussion_contributors)))
 if len(article_contributors)!=0:
  disc_percent=len(disc_and_article)/float(len(article_contributors))
 else:
  disc_percent=0.0
 if len(discussion_contributors)!=0:
  article_percent=len(disc_and_article)/float(len(discussion_contributors))
 else:
  article_percent=0.0
 if len(only_disc)!=0:
  article_disc=len(only_article)/float(len(only_disc))
 else:
  article_disc=0.0
 print "Disc_Percent: ",disc_percent,"Article_Percent: ",article_percent, "Article_Disc: ",article_disc
 file_comparison=open('B_Article_Contributor_Comparison.txt','a')
 file_comparison.write("B"+";"+str(focal_article)+";"+str(article_percent)+";"+str(disc_percent)+";"+str(article_disc)+"\n")
 file_comparison.close()