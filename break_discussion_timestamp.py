from datetime import datetime,timedelta
page_titles=open('Final_Page_Titles_FA.txt','r')
for line_titles in page_titles:
 focal_title=str(line_titles.split(';')[1].strip('\n'))
 file=open('Discussions_FA.txt','r')
 print "Now for Title:", focal_title
 time_stamps_array=list()
 records_array=list()
 counter=0
 for line in file:
  title=str(line.split('~;')[1].strip('\n').strip('~;'))
  if title==focal_title:
   counter=1
   user=str(line.split('~;')[5].strip('\n'))
   #print "X:",x_opt
   time_stamp=str(line.split('~;')[6].strip('\n'))
   #print "Line:",line,"Time:", time_stamp
   month=int(time_stamp.split('/')[0])
   day=int(time_stamp.split('/')[1])
   year=int(time_stamp.split('/')[2].strip('\n').split(' ')[0])
   hour=int(time_stamp.split('/')[2].strip('\n').split(' ')[1].split(':')[0])
   minute=int(time_stamp.split('/')[2].strip('\n').split(' ')[1].split(':')[1])
   date_string=str(year)+'-'+str(month)+'-'+str(day)+' '+str(hour)+':'+str(minute)
   modified_ts=datetime.strptime(date_string,"%Y-%m-%d %H:%M")
   time_stamps_array.append(modified_ts)
   records_array.append(line.strip('\n'))
   #print "Length of TS Array:",len(time_stamps_array)," Length of records array:", len(records_array)
   #print  "Focal_Title:", focal_title, "Title:", title
   
  if counter==1 and title!=focal_title :
   print "Inside elif:"
   max_ts=max(time_stamps_array)
   min_ts=min(time_stamps_array)
   #print "Max_TS:",max_ts, "Min_TS:",min_ts
   difference=max_ts-min_ts
   difference_days=difference.days
   time_multiplier=difference_days/float(50.0)
   #print "Difference:", difference.seconds, "Time_Multiplier:", time_multiplier
   for element in records_array:
    ts=str(element.split('~;')[6])
    #print "TS:",ts
    month=int(ts.split('/')[0])
    day=int(ts.split('/')[1])
    year=int(ts.split('/')[2].strip('\n').split(' ')[0])
    hour=int(ts.split('/')[2].strip('\n').split(' ')[1].split(':')[0])
    minute=int(ts.split('/')[2].strip('\n').split(' ')[1].split(':')[1])
    date_string=str(year)+'-'+str(month)+'-'+str(day)+' '+str(hour)+':'+str(minute)
    ts_m=datetime.strptime(date_string,"%Y-%m-%d %H:%M")
    #print "TSM:", ts_m
    for i in range(0,50):
	 #print "Time Multplier Now :", i*time_multiplier
	 #print "TS:",ts_m,"Lower_Bound:", min_ts+timedelta(days=i*time_multiplier), "Upper_Bound:", min_ts+timedelta(days=(i+1)*time_multiplier)
	 if ts_m>=min_ts+timedelta(days=i*time_multiplier) and ts_m<min_ts+timedelta(days=(i+1)*time_multiplier):
	  #print "Inside Analysis"
	  file_ts=open('FA_TS_Analysis.txt','a')
	  file_ts.write(str(element)+"~;"+str(i+1)+"\n")
	  file_ts.close()
	  break
   break
   