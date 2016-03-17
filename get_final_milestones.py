file_titles=open('Final_Page_Titles_GA.txt','r')
for line_title in file_titles:
 focal_title=line_title.split(';')[1].strip('\n')
 print "Now for Title: ", focal_title
 file_milestones=open('Full_Article_Milestones.txt','r')
 for line_milestone in file_milestones:
  article=line_milestone.split(';')[0]
  milestone=line_milestone.split(';')[1].strip('\n')
  if focal_title==article:
   file_final_milestones=open('Final_Article_Milestones_GA.txt','a')
   file_final_milestones.write(str(focal_title)+";"+str(milestone)+"\n")
   file_final_milestones.close()
   break
