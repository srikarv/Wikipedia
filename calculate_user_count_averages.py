import numpy as np
for i in range(0,50):
 file=open('User_Participation_FA.txt','r')
 values=list()
 for line in file:
  if int(line.split(';')[1])==i and int(line.split(';')[2].strip('\n'))>0:
   values.append(int(line.split(';')[2].strip('\n')))
 file_avg=open('FA_User_Participation_Median.txt','a')
 if len(values)>0:
  file_avg.write(str(i+1)+";"+str(np.median(values))+"\n")
 else:
  file_avg.write(str(i+1)+";"+str(0.0)+"\n")
 file_avg.close()