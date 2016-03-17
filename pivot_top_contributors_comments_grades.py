file_input=open('Top_Contributors_Comments_Grades.txt','r')
editors=list()
for line in file_input:
 editor=line.split('\t')[0]
 editors.append(editor)
 
distinct_editors=set(editors)
Grades=['FA','GA','B','C']
for focal_editor in distinct_editors:
 counts_list={}
 for focal_grade in Grades:
  file_input=open('Top_Contributors_Comments_Grades.txt','r')
  for line in file_input:
   editor=line.split('\t')[0] 
   grade=line.split('\t')[1]
   count=line.split('\t')[2].strip('\n')
   if focal_editor==editor and focal_grade==grade:
    counts_list[grade]=count
 file_output=open('Final_Contribution_File.txt','a')
 file_output.write(str(focal_editor)+"\t")
 for final_grade in ['FA','GA','B','C']:
  if counts_list.has_key(final_grade): 
   file_output.write(str(counts_list[final_grade])+"\t")
  else:
   file_output.write(str(0)+"\t")
 file_output.write("\n")
 file_output.close()
