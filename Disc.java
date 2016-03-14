
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class Disc {
	String path = ".";
	File folder = new File(path);
	File[] listOfFiles = folder.listFiles(); 
	ArrayList<String> file_list= new ArrayList<String>();
	private String SIGNATURE_PATTERNS="\\[\\[User([ ])*\\:([ ])*|\\[\\[Special:Contributions\\/";
	private String REAL_SIGNATURE_PATTERN1="\\[\\[User ?\\: ?.([a-zA-z0-9]|[-_#;:,./<>@$&*()!~?{} ]|\\[|\\]|\\/|\")*.\\|";
	private String REAL_SIGNATURE_PATTERN2="\\[\\[Special:Contributions\\/ ?.[a-zA-z0-9-_./ ]*.\\|";
	private String SIGNATURE_AND_TIME_STAMP_PATTERN1=SIGNATURE_PATTERNS+".*."+REAL_SIGNATURE_PATTERN1;
	private String SIGNATURE_AND_TIME_STAMP_PATTERN2=SIGNATURE_PATTERNS+".*."+REAL_SIGNATURE_PATTERN2;
	private String TIME_STAMP_PATTERNS="([01]?[0-9]|2[0-3]):[0-5][0-9]" + "," +" " +"[0-9]([0-9])?" + " " + "(January|February|March|April|May|June|July|August|September|October|November|December)"+ " "+ "20[0-1][0-9]" +" " +"\\(UTC\\)";
	private String DISCUSSION_THREAD_TOPIC_PATTERNS="^ {0,20}\\={2,10}[ |\t]{0,20}.([a-zA-z0-9]|[-_#;:,./<>@$&*()!~?{} ]|\\[|\\]|\\/|\\'|\"|\\|)*.[ |\t]{0,20}\\={2,10}";
	private String INDENDATION_MATCHING_PATTERNS="^[ ]*([\\:|\\*|\\#])*.([a-zA-z0-9]|[-_#;,./<>@$&*()!~?{} ]|\\[|\\]|\\/|\"|\')*";
	private Pattern real_signature_pattern1=Pattern.compile(REAL_SIGNATURE_PATTERN1);
	private Pattern real_signature_pattern2=Pattern.compile(REAL_SIGNATURE_PATTERN2);
	private Pattern signature_and_time_stamp_pattern1=Pattern.compile(SIGNATURE_AND_TIME_STAMP_PATTERN1);
	private Pattern signature_and_time_stamp_pattern2=Pattern.compile(SIGNATURE_AND_TIME_STAMP_PATTERN2);
	private Pattern signature_pattern=Pattern.compile(SIGNATURE_PATTERNS);
	private Pattern indendation_pattern=Pattern.compile(INDENDATION_MATCHING_PATTERNS);
	
	private Pattern Time_Stamp_pattern = Pattern.compile(TIME_STAMP_PATTERNS);
	private Pattern Discussion_Thread_pattern=Pattern.compile(DISCUSSION_THREAD_TOPIC_PATTERNS);
	String time_stamp=null;
	String signature=null;
	public static void main(String[] args) throws FileNotFoundException{
		//create an instance
		Disc dpp = new Disc();
		
		//call run example
		dpp.runExample();
	}
public void runExample() throws FileNotFoundException {
		
		//get the list of file to be parsed
		get_file_List();
		
		//display the list of files obtained
		//display_file_list();
		
		//parse each document
		parseDocument();
		
		//Iterate through the list and print the data
		//printData(); // not in use for now
		
	}

private void parseDocument() throws FileNotFoundException {
	int file_count=0;
	for(int l=0;l<file_list.size();l++)
	{
		System.out.println("File Number:" +l);
        String Article_name=file_list.get(l).substring(0, file_list.get(l).length()-4);
		//String Article_name="Action_of_11_November_2008";
        System.out.println("Article_Name :"+Article_name);
    long comment_id=0,parent_comment_id=0;  
	String topic_thread=null;	// make the topic thread null at the beginning of every topic
	file_count++;
	try {
		FileInputStream fstream = new FileInputStream(file_list.get(l));//needs to be changed as per the file input
		//FileInputStream fstream = new FileInputStream("Action_of_11_November_2008.xml");
		//output stream
		//FileWriter f_output_stream = new FileWriter("output_comments_comprehensive_C.sql",true);
		//BufferedWriter output = new BufferedWriter(f_output_stream);
		//input stream
		DataInputStream in = new DataInputStream(fstream);
		BufferedReader br = new BufferedReader(new InputStreamReader(in));
		String strLine;
		int k=0;
		int new_topic_indicator = 0;
		 long prev_comment_id=0;// we use the parent_id and comment_id to store the indentation level
		 long prev_parent_id=0;
		 long prev_indendation_level=0;
		 long [][] indent_array=new long[5000][3]; // we store the parent_id,comment_id and indendation_level in that order
		 int line_num=0;
		while ((strLine = br.readLine()) != null)   {		
			k++;
			String Line=null;
			String Signature=null;
			String Time_Stamp=null;
			String Real_Signature=null;
			int signature_index=0;
			//output stream
			FileWriter f_output_stream = new FileWriter("output_comments_comprehensive_C_5.txt",true); // this is the output file
			BufferedWriter output = new BufferedWriter(f_output_stream);
			// ignore empty lines
			if(strLine.trim().length()==0){
				continue;
			}
			//System.out.println("StrLine" +strLine);
			//matching the discussion thread, Reading whether the line is a topic or not
			Matcher discussion_topic_matcher=Discussion_Thread_pattern.matcher(strLine);			
			if(discussion_topic_matcher.find())
			{
				topic_thread=discussion_topic_matcher.group();
				 topic_thread=topic_thread.replace("\'","");
				 topic_thread=topic_thread.replace("\\,","");
				 topic_thread=topic_thread.replace("\\;","");
				 topic_thread=topic_thread.replace("\\:","");
				 topic_thread=topic_thread.replace("\\.","");
				 topic_thread=topic_thread.replace("\\@","");
				 topic_thread=topic_thread.replace("\\$","");
				 topic_thread=topic_thread.replace("\\^","");
				 topic_thread=topic_thread.replace("\\&","");
				 topic_thread=topic_thread.replace("\\*","");
				 topic_thread=topic_thread.replace("\\(","");
				 topic_thread=topic_thread.replace("\\)","");
				 topic_thread=topic_thread.replace("\\[","");
				 topic_thread=topic_thread.replace("\\]","");
				 topic_thread=topic_thread.replace("\\{","");
				 topic_thread=topic_thread.replace("\\}","");
				 topic_thread=topic_thread.replace("\\?","");
				 topic_thread=topic_thread.replace("\\<","");
				 topic_thread=topic_thread.replace("\\>","");
				comment_id=0;
				parent_comment_id=0;
				new_topic_indicator=1;
				line_num=0;
				for(int h=0;h<5000;h++)
				{
					indent_array[h][0]=0;
					indent_array[h][1]=0;
					indent_array[h][2]=0;
				}
				continue;
			}
			//if the line is not a topic then continue and match the signature
			Matcher signature_matcher = signature_pattern.matcher(strLine);
			if (signature_matcher.find()== false) // if signature is not found continue to the next line 
			{
				//System.out.println("No Signature Found");
				continue;
			}
			//if it is a signature, find the index
			for (int j=0;j<signature_matcher.groupCount()+1;j++)
			{
				if(signature_matcher.start(j)!=-1)
				{
					signature_index++;
				}
			}
			
       		if (signature_index==1)
			{
				signature_index--;
			}
       		//System.out.println("Signature_index Group Count "+signature_matcher.groupCount());
			if(signature_matcher.start(signature_index)>2)
			{
			//System.out.println("Signature Index:"+signature_matcher.start(signature_index)+"StrLineLength:"+strLine.length());
			 Matcher Time_Stamp_matcher = Time_Stamp_pattern.matcher(strLine.substring(signature_matcher.start(signature_index), strLine.length()));
			 if (Time_Stamp_matcher.find() == false) // if time stamp is not found continue to the next line *** Needs Correction
			 {
				continue;
			 }
			 Line=strLine.substring(0, signature_matcher.start(signature_index)-2);
			 Line=Line.replace("\'","");
			 Line=Line.replace("\\,","");
			 Line=Line.replace("\\;","");
			 Line=Line.replace("\\:","");
			 Line=Line.replace("\\.","");
			 Line=Line.replace("\\@","");
			 Line=Line.replace("\\$","");
			 Line=Line.replace("\\^","");
			 Line=Line.replace("\\&","");
			 Line=Line.replace("\\*","");
			 Line=Line.replace("\\(","");
			 Line=Line.replace("\\)","");
			 Line=Line.replace("\\[","");
			 Line=Line.replace("\\]","");
			 Line=Line.replace("\\{","");
			 Line=Line.replace("\\}","");
			 Line=Line.replace("\\?","");
			 Line=Line.replace("\\<","");
			 Line=Line.replace("\\>","");
			 Signature=strLine.substring(signature_matcher.start(), signature_matcher.start()+Time_Stamp_matcher.start()-1);
			 //System.out.println("Signature"+Signature);
			 Matcher signature_and_time_stamp_matcher1=signature_and_time_stamp_pattern1.matcher(Signature);
			 // matching the first pattern of signatures
			 Matcher real_signature_matcher1 = real_signature_pattern1.matcher(Signature);
			 if(real_signature_matcher1.find())
			 {
				 //System.out.println("Signature 1 Match found");
				Real_Signature=Signature.substring(real_signature_matcher1.start()+7, real_signature_matcher1.end()-1);
				Real_Signature=Real_Signature.replace("\'","");
				 Real_Signature=Real_Signature.replace("\\,","");
				 Real_Signature=Real_Signature.replace("\\;","");
				 Real_Signature=Real_Signature.replace("\\:","");
				 Real_Signature=Real_Signature.replace("\\.","");
				 Real_Signature=Real_Signature.replace("\\@","");
				 Real_Signature=Real_Signature.replace("\\$","");
				 Real_Signature=Real_Signature.replace("\\^","");
				 Real_Signature=Real_Signature.replace("\\&","");
				 Real_Signature=Real_Signature.replace("\\*","");
				 Real_Signature=Real_Signature.replace("\\(","");
				 Real_Signature=Real_Signature.replace("\\)","");
				 Real_Signature=Real_Signature.replace("\\[","");
				 Real_Signature=Real_Signature.replace("\\]","");
				 Real_Signature=Real_Signature.replace("\\{","");
				 Real_Signature=Real_Signature.replace("\\}","");
				 Real_Signature=Real_Signature.replace("\\?","");
				 Real_Signature=Real_Signature.replace("\\<","");
				 Real_Signature=Real_Signature.replace("\\>","");
				//System.out.println("Real Signature :"+Real_Signature);
			 }
			 //matching the second pattern of signatures
			 else
			 {
			  Matcher real_signature_matcher2 = real_signature_pattern2.matcher(Signature);
			  if(real_signature_matcher2.find())
			  {
				  //System.out.println("Signature 2 Match Found");
				 Real_Signature=Signature.substring(real_signature_matcher2.start()+24, real_signature_matcher2.end()-1);
				 Real_Signature=Real_Signature.replace("\'","");
				 Real_Signature=Real_Signature.replace("\\,","");
				 Real_Signature=Real_Signature.replace("\\;","");
				 Real_Signature=Real_Signature.replace("\\:","");
				 Real_Signature=Real_Signature.replace("\\.","");
				 Real_Signature=Real_Signature.replace("\\@","");
				 Real_Signature=Real_Signature.replace("\\$","");
				 Real_Signature=Real_Signature.replace("\\^","");
				 Real_Signature=Real_Signature.replace("\\&","");
				 Real_Signature=Real_Signature.replace("\\*","");
				 Real_Signature=Real_Signature.replace("\\(","");
				 Real_Signature=Real_Signature.replace("\\)","");
				 Real_Signature=Real_Signature.replace("\\[","");
				 Real_Signature=Real_Signature.replace("\\]","");
				 Real_Signature=Real_Signature.replace("\\{","");
				 Real_Signature=Real_Signature.replace("\\}","");
				 Real_Signature=Real_Signature.replace("\\?","");
				 Real_Signature=Real_Signature.replace("\\<","");
				 Real_Signature=Real_Signature.replace("\\>","");
				 //System.out.println("Real Signature :"+Real_Signature);
			  }
			 }
			 
			 //now get the time stamp
			 Time_Stamp=strLine.substring(signature_matcher.start(signature_index)+Time_Stamp_matcher.start(),strLine.lastIndexOf("UTC")-2);
			 Time_Stamp=Time_Stamp.replace("\'","");
			 Time_Stamp=Time_Stamp.replace("\\,","");
			 Time_Stamp=Time_Stamp.replace("\\;","");
			 Time_Stamp=Time_Stamp.replace("\\:","");
			 Time_Stamp=Time_Stamp.replace("\\.","");
			 Time_Stamp=Time_Stamp.replace("\\@","");
			 Time_Stamp=Time_Stamp.replace("\\$","");
			 Time_Stamp=Time_Stamp.replace("\\^","");
			 Time_Stamp=Time_Stamp.replace("\\&","");
			 Time_Stamp=Time_Stamp.replace("\\*","");
			 Time_Stamp=Time_Stamp.replace("\\(","");
			 Time_Stamp=Time_Stamp.replace("\\)","");
			 Time_Stamp=Time_Stamp.replace("\\[","");
			 Time_Stamp=Time_Stamp.replace("\\]","");
			 Time_Stamp=Time_Stamp.replace("\\{","");
			 Time_Stamp=Time_Stamp.replace("\\}","");
			 Time_Stamp=Time_Stamp.replace("\\?","");
			 Time_Stamp=Time_Stamp.replace("\\<","");
			 Time_Stamp=Time_Stamp.replace("\\>","");
			 //start getting the indendation level of the comment
			 int indendation_level=0;	
			 Matcher indendation_matcher=indendation_pattern.matcher(Line);
			 if(indendation_matcher.find()) // setting the parent and comment ids as per the indendation levels
			 {				 
				 for (int i=0;i<indendation_matcher.end()-1;i++)
				 {
					 if(Line.charAt(i)==':'||Line.charAt(i)=='#'||Line.charAt(i)=='*')
					 {
						 indendation_level++;	 
					 }
				 }				 
			 }
			
			 	
			 // if it is a new topic, then parent and comment id should be 0
			 if(new_topic_indicator==1)
			 {
				 parent_comment_id=0;comment_id=0;
				 prev_comment_id=0;
				 prev_parent_id=0;
				 //System.out.println("New Topic Indicator");
				 //System.out.println("Real Signature Now  " +Real_Signature);
				 //System.out.println ("Line Now"+Line);
				 //output.write("Insert into Wiki_Comments value("+"\'FA\',\'"+Article_name+"\',\'"+topic_thread+"\',"+comment_id+","+parent_comment_id+",\'"+Line+"\',\'"+Real_Signature+"\',\'"+Time_Stamp+"\'"+");");
				 //output.write("FA;"+Article_name+";"+topic_thread+";"+comment_id+";"+parent_comment_id+";"+Line+";"+Real_Signature+";"+Time_Stamp+";");
				 output.write("C~"+Article_name+"~"+topic_thread+"~"+comment_id+"~"+parent_comment_id+"~"+Line+"~"+Real_Signature+"~"+Time_Stamp+"~");
				 output.write("\n");
				 output.close();
				 comment_id++;
				 new_topic_indicator=0;
				 prev_indendation_level=0;
				 indent_array[line_num][0]=0;
				 indent_array[line_num][1]=0;
				 indent_array[line_num][2]=0;
				 line_num++;
				 
				  continue;
			 }
			 // A topic may have 2 or 3 comments without indendation level. If it has the same indent as the first comment, parent and comment will be 0 again
			 else if(indendation_level==0)
			 {
				 parent_comment_id=0;comment_id=0;
				 prev_comment_id=0;
				 prev_parent_id=0;
				 
				 //System.out.println("0 Indendation Level");
				 //output.write("Insert into Wiki_Comments value("+"\'FA\',\'"+Article_name+"\',\'"+topic_thread+"\',"+comment_id+","+parent_comment_id+",\'"+Line+"\',\'"+Real_Signature+"\',\'"+Time_Stamp+"\'"+");");
				 output.write("C~"+Article_name+"~"+topic_thread+"~"+comment_id+"~"+parent_comment_id+"~"+Line+"~"+Real_Signature+"~"+Time_Stamp+"~");
				 output.write("\n");
				 output.close();
				 comment_id++;
				 prev_indendation_level=0;
				 indent_array[line_num][0]=0;
				 indent_array[line_num][1]=0;
				 indent_array[line_num][2]=0;
				 line_num++;
				 continue;
			 }
			 else if(prev_parent_id==0 && prev_comment_id==0 && indendation_level!=0)
			 {
				 parent_comment_id=0;comment_id=1;
				 prev_comment_id=1;
				 prev_parent_id=0;
				 //System.out.println("Parent and comment 0");
				 //output.write("Insert into Wiki_Comments value("+"\'FA\',\'"+Article_name+"\',\'"+topic_thread+"\',"+comment_id+","+parent_comment_id+",\'"+Line+"\',\'"+Real_Signature+"\',\'"+Time_Stamp+"\'"+");");
				 output.write("C~"+Article_name+"~"+topic_thread+"~"+comment_id+"~"+parent_comment_id+"~"+Line+"~"+Real_Signature+"~"+Time_Stamp+"~");
				 output.write("\n");
				 output.close();
				 comment_id++;
				 prev_indendation_level=1;
				 indent_array[line_num][0]=0;
				 indent_array[line_num][1]=comment_id;
				 indent_array[line_num][2]=1;
				 line_num++;
				 continue;
			 }
			 /*else if(indendation_level==prev_indendation_level+1)
			 {
				 parent_comment_id=prev_comment_id;
				 prev_indendation_level=indendation_level;
				 //System.out.println("new indent");
			 }*/
			 else if(indendation_level<prev_indendation_level) 
			 {
				 int f;
				 for( f=0;f<line_num;f++)
				 {
					 if(indent_array[f][2]==indendation_level-1)
					 {
						 break;
					 }
				 }
				 parent_comment_id=indent_array[f][1];
				 prev_indendation_level=indendation_level;
				 indent_array[line_num][0]=parent_comment_id;
				 indent_array[line_num][1]=comment_id;
				 indent_array[line_num][2]=indendation_level;
				 line_num++;
			 }
				 /*if(indendation_level>0 && prev_parent_id==0 && prev_comment_id==0)
				 {
					 parent_comment_id=0;comment_id=1;
					 prev_comment_id=1;
					 prev_parent_id=0;			
					 output.write("B,"+Article_name+","+topic_thread+","+comment_id+","+parent_comment_id+","+"\""+Line+"\""+","+Real_Signature+","+Time_Stamp);
					 output.write("\n");
					 comment_id++;
					 prev_indendation_level=indendation_level;
					 continue;
				 }*/
				 else
				 {
					 parent_comment_id=prev_comment_id;
					 prev_comment_id=comment_id;
					 //output.write("Indendation Level"+indendation_level+"\n");
					 prev_indendation_level=indendation_level;
					 indent_array[line_num][0]=parent_comment_id;
					 indent_array[line_num][1]=comment_id;
					 indent_array[line_num][2]=indendation_level;
					 line_num++;
				 }
				 
			 }     					 
			//System.out.println("File Name"+Article_name+",Discussion Topic"+topic_thread+",Comment_id"+comment_id+",Parent ID"+parent_comment_id+",Line"+Line+",Signature"+Real_Signature+",Time Stamp"+Time_Stamp);				
			//output.write("Insert into Wiki_Comments value("+"\'FA\',\'"+Article_name+"\',\'"+topic_thread+"\',"+comment_id+","+parent_comment_id+",\'"+Line+"\',\'"+Real_Signature+"\',\'"+Time_Stamp+"\'"+");");
			output.write("C~"+Article_name+"~"+topic_thread+"~"+comment_id+"~"+parent_comment_id+"~"+Line+"~"+Real_Signature+"~"+Time_Stamp+"~");
			output.write("\n");
			output.close();
			comment_id++;
			}
		br.close();
		in.close();
		fstream.close();
			
			
			

		System.out.println("File Count"+file_count);
		File file = new File(Article_name+".xml");
		 
		if(file.delete()){
			System.out.println(file.getName() + " is deleted!");
		}else{
			System.out.println("Delete operation is failed.");
		}

		//System.out.println("Number of Lines :"+k);
	} catch (IOException e) {
		e.printStackTrace();
	}
	}
	System.out.println("Final File Count"+file_count);
}
private void get_file_List() {
	// TODO Auto-generated method stub
	String file_name=null;
	for (int i = 0; i < listOfFiles.length; i++) 
	  {
	 
	   if (listOfFiles[i].isFile()) 
	   {
		   file_name = listOfFiles[i].getName();
	       if (file_name.endsWith(".xml") || file_name.endsWith(".XML"))
	       {
	         file_list.add(file_name) ;
	       }
	     }
	  }
	
}
private void display_file_list() {
	System.out.println("List of Files to be parsed");
	for(int i=0;i<file_list.size();i++)
	{
		System.out.println(file_list.get(i));
	}
	System.out.println("Total Files"+file_list.size());
	
}
}