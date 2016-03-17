import java.io.*;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.regex.Pattern;

public class DiscCommentClassification{
	
     String LABEL_ACKNOWLEDGEMENT="Done|Cheers|Fixed|removed";
     String IMAGES_PICTURES="Images|Image|Picture|Pictures|Albums|jpg";
     String SOURCES_REFERENCES="Source|Reference|Link|Links|References|Sources|Citation|Citations";
     String FONT_FORMAT="font|format|font-size|Wikipedia\\:Article titles|formatting|WP\\:DASH|WP\\:YEAR|WP\\:MOSHEAD|WP\\:HEADINGS|MOS\\:\\&|WP\\:\\&|MOS\\:*|WP\\:NBSP|WP\\:MOSQUOTE|WP\\:PUNCT|WP\\:MOSLQ|WP\\:ELLIPSES|WP\\:ELLIPSIS|WP\\:COMMA|WP\\:HOWEVERPUNC|WP\\:HYPHEN|WP\\:MDASH|WP\\:EMDASH|WP\\:[a-zA-Z]*DASH|WP\\:SLASH|WP\\:ANDOR|WP\\:POUND|WP\\:REFPUNC|WP\\:REFSPACE|WP\\:FIRSTPERSON|WP\\:YOU|WP\\:PLURALS|WP\\:CONTRACTION|WP\\:JARGON|WP\\:MOSIM|WP\\:COMMENT|Wikipedia\\:Manual\\_of\\_Style|WP\\:BOLD";
     String APPRECIATION="Thank you|Thanks";
     String LABEL_SUMMARY="In summary([\\,])|Summary([ ])*\\:|^[ |\\,]to summarise|^[ |\\,]to summarize([\\,|\\:|\\;])*";
     String LABEL_SUGGESTION="I suggest that we include|How about we include|How about adding|How about including|What about including|Can we include|Can we add|I think you should include|I think we should include|I suppose he could be included in|I suppose it could be included in|I suppose it could be included|why not include|Perhaps someone should include|we should include|This should be definetly included|This should be included|you could include it|it is desirable to include|it should be included|should probably also be included|should probably be included|we can include that|we can include|it might be included|it needs to be|we need to|it shold go in the article|we could add";
     String LABEL_CLARIFICATION="What is it|Which is it|How is it|How is that so";
     
     HashMap<String, Boolean> Label_Map=new HashMap<String, Boolean>();
     
     private Pattern ACKNOWLEDGEMENT_PATTERN = Pattern.compile(LABEL_ACKNOWLEDGEMENT, Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
	 private Pattern IMAGES_PATTERN=Pattern.compile(IMAGES_PICTURES, Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
	 private Pattern SOURCES_REFERENCES_PATTERN=Pattern.compile(SOURCES_REFERENCES, Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
     private Pattern FONT_FORMAT_PATTERN=Pattern.compile(FONT_FORMAT,Pattern.CASE_INSENSITIVE|Pattern.UNICODE_CASE);
	 private Pattern APPRECIATION_PATTERN=Pattern.compile(APPRECIATION,Pattern.CASE_INSENSITIVE|Pattern.UNICODE_CASE);
     private Pattern SUMMARY_PATTERN=Pattern.compile(LABEL_SUMMARY,Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
     private Pattern SUGGESTION_PATTERN=Pattern.compile(LABEL_SUGGESTION,Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
     private Pattern CLARIFICATION_PATTERN=Pattern.compile(LABEL_CLARIFICATION,Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
     
     public static void main (String[] args) throws IOException{
		DiscCommentClassification dpp=new DiscCommentClassification();
		dpp.runExample();
	}

	public void runExample() throws FileNotFoundException {
		
		assign_label();
		
	}

	public void assign_label() throws FileNotFoundException {
		try {
			FileInputStream fstream = new FileInputStream("all_comments.txt"); // This is the input file
			DataInputStream in = new DataInputStream(fstream);
			BufferedReader br = new BufferedReader(new InputStreamReader(in));
			String strLine;
			while ((strLine = br.readLine()) != null)   {
				String[] Temp_Line=strLine.replace("\n", "").split("~&");
				String text=Temp_Line[3];
				Label_Map.put("IMAGES", IMAGES_PATTERN.matcher(text).find());
				Label_Map.put("ACKNOWLEDGEMENT", ACKNOWLEDGEMENT_PATTERN.matcher(text).find());
				Label_Map.put("SOURCES_AND_REFERENCES", SOURCES_REFERENCES_PATTERN.matcher(text).find());
				Label_Map.put("FONT_FORMAT", FONT_FORMAT_PATTERN.matcher(text).find());
				Label_Map.put("APPRECIATION",APPRECIATION_PATTERN.matcher(text).find());
				Label_Map.put("SUMMARY", SUMMARY_PATTERN.matcher(text).find());				
				Label_Map.put("SUGGESTION", SUGGESTION_PATTERN.matcher(text).find());
				Label_Map.put("CLARIFICATION", CLARIFICATION_PATTERN.matcher(text).find());

				FileWriter f_output_stream = new FileWriter("Comment_Text_Labels.txt",true); // This is the output file
				BufferedWriter output = new BufferedWriter(f_output_stream);
				Iterator iter = Label_Map.entrySet().iterator();
				output.write(strLine.replace("\n", "")+"--;");
				System.out.println(strLine);
				int flag=0;
				while (iter.hasNext()) {
					Map.Entry mEntry = (Map.Entry) iter.next();
					if((boolean) mEntry.getValue())
					{
						flag=1;
						output.write(mEntry.getKey()+";");
					}
					System.out.println(mEntry.getKey() + " : " + mEntry.getValue());
				}
				if(flag==0)
				{
					output.write("OTHERS;");
				}					
				output.write("\n");	     
				output.close();
			}
			
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}
	
}