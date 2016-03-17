file_1=open('FD_C_Comprehensive.txt','r')
file_2=open('Final_Page_Titles_C.txt','r')
file_3=open('Final_Article_Milestones.txt','r')
comp_list=list()
milestone_dict={}
complete_titles=list()
for line_1 in file_1:
 comp_list.append(line_1.split('~;')[1])

for line_2 in file_2:
 complete_titles.append(line_2.split(';')[1].strip('\n'))

missing_titles=list(set(complete_titles)-set(comp_list))

for line_3 in file_3:
 milestone_dict[line_3.split(';')[0]]=line_3.split(';')[1].strip('\n') 

for miss in missing_titles:
 if milestone_dict.has_key(miss):
  file_missing=open('Missing_Milestones_C.txt','a')
  file_missing.write(str(miss)+";"+str(milestone_dict[miss])+"\n") 
  file_missing.close()