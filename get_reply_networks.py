file_articles=open('Final_Page_Titles_FA.txt','r')
for article in file_articles:
 focal_article=article.split(';')[1].strip('\n')
 focal_file=open(focal_article+'_discussion_FA.txt','r')
 editors_list=list()
 for line_focal in focal_file:
  editors_list.append(line_focal.split('~;')[5].strip('\n'))
 final_editors_list=set(editors_list)
 editor_dict={}
 k=1
 for item in final_editors_list:
  editor_dict[k]=item
  k+=1
 for key1 in range(1,k-1):
  for key2 in range(2,k):
   focal_file1=open(focal_article+'_discussion_FA.txt','r')
   for line_focal1 in focal_file1:
    Grade1=line_focal1.split('~;')[0]
	Article1=line_focal1.split('~;')[1]
	Thread_Title1=line_focal1.split('~;')[2]
	Comment_ID1=int(line_focal1.split('~;')[3])
	Parent_Comment_ID1=int(line_focal1.split('~;')[4])
	Signature1=line_focal1.split('~;')[5].strip('\n')
	focal_file2=open(focal_article+'_discussion_FA.txt','r')
	for line_focal2 in focal_file2:
	 Grade2=line_focal2.split('~;')[0]
	 Article2=line_focal2.split('~;')[1]
	 Thread_Title2=line_focal2.split('~;')[2]
	 Comment_ID2=int(line_focal2.split('~;')[3])
	 Parent_Comment_ID2=int(line_focal2.split('~;')[4])
	 Signature2=line_focal2.split('~;')[5].strip('\n')
	 if Thread_Title2==Thread_Title1 and Parent_Comment_ID2=Comment_ID1 and Signature1==editor_dict[key1] and Signature2==editor_dict[key2]:
	  final_network_file=open(focal_article+'_reply_network_FA.txt','a')
	  final_network_file.write(str(Signature1)+";"+str(Signature2)+"\n")
	  final_network_file.close()
	 else if Thread_Title2==Thread_Title1 and Parent_Comment_ID1=Comment_ID2 and Signature1==editor_dict[key1] and Signature2==editor_dict[key2]:
	  final_network_file=open(focal_article+'_reply_network_FA.txt','a')
	  final_network_file.write(str(Signature1)+";"+str(Signature2)+"\n")
	  final_network_file.close()	 
	  
	