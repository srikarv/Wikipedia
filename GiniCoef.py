'''
Created on July 24, 2011
@author: Dilum Bandara
@version: 0.1
@license: Apache License v2.0

   Copyright 2012 H. M. N. Dilum Bandara, Colorado State University

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

#import matplotlib.pyplot as plt


def GRLC(values):
    '''
    Calculate Gini index, Gini coefficient, Robin Hood index, and points of 
    Lorenz curve based on the instructions given in 
    www.peterrosenmai.com/lorenz-curve-graphing-tool-and-gini-coefficient-calculator
    Lorenz curve values as given as lists of x & y points [[x1, x2], [y1, y2]]
    @param values: List of values
    @return: [Gini index, Gini coefficient, Robin Hood index, [Lorenz curve]] 
    '''
    n = len(values)
    assert(n > 0), 'Empty list of values'
    sortedValues = sorted(values) #Sort smallest to largest

    #Find cumulative totals
    cumm = [0]
    for i in range(n):
        cumm.append(sum(sortedValues[0:(i + 1)]))

    #Calculate Lorenz points
    LorenzPoints = [[], []]
    sumYs = 0           #Some of all y values
    robinHoodIdx = -1   #Robin Hood index max(x_i, y_i)
    for i in range(1, n + 2):
        x = 100.0 * (i - 1)/n
        y = 100.0 * (cumm[i - 1]/float(cumm[n]))
        LorenzPoints[0].append(x)
        LorenzPoints[1].append(y)
        sumYs += y
        maxX_Y = x - y
        if maxX_Y > robinHoodIdx: robinHoodIdx = maxX_Y   
    
    giniIdx = 100 + (100 - 2 * sumYs)/n #Gini index 

    return [giniIdx, giniIdx/100, robinHoodIdx, LorenzPoints]


#Example
file_articles=open('Distinct_Articles.txt','r')

for article in file_articles:
 article_name=article.split('\t')[1].strip('\n')
 Grade=article.split('\t')[0].strip('\n').strip()
 contribution_counts=list()
 print "Article:", article_name, "Grade:", Grade
 i=1
 file_1=open('Contributor_Counts_1600Articles.txt','r')
 for line in file_1:
  Grade_1=line.split('\t')[0].strip()
  Title=line.split('\t')[1].strip()
  contributor=line.split('\t')[2].strip()
  cnt=int(line.split('\t')[3].strip('\n'))
  #print "Grade:" ,Grade, "\tTitle:", Title, "\tcontributor:", contributor, "\tCount:", count , "\n"
  if article_name==Title and cnt!=0:
   #print "Inside If"
   contribution_counts.append(i)
   contribution_counts.append(cnt)
   i+=1
 if len(contribution_counts)>0:
  result=GRLC(contribution_counts)
  gini_index=result[0]
  gini_coefficient=result[1]
  RobinHood_index=result[2]
  print "Gini Index:", gini_index
  file_gini=open('Gini_RobinHood_1600Articles.txt','a')
  file_gini.write(str(Grade)+";"+str(article_name)+";"+str(gini_index)+";"+str(gini_coefficient)+";"+str(RobinHood_index)+"\n")
  file_gini.close()

#result = GRLC(sample1)
#result = GRLC(sample2)
#print 'Gini Index', result[0]  
#print 'Gini Coefficient', result[1]
#print 'Robin Hood Index', result[2]
#print 'Lorenz curve points', result[3]

#Plot
#plt.plot(result[3][0], result[3][1], [0, 100], [0, 100], '--')
#plt.xlabel('% of pupulation')
#plt.ylabel('% of values')
#plt.show()
