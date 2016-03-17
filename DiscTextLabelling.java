import java.io.*;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.regex.Pattern;

public class DiscTextLabelling{
	
     String LABEL_POSITIVE_APOLOGY="Please forgive me|Apologies|(?!No)([ ])*apologies([ ])*(?!needed)|apology|I([ ])*do([ ])*apologise|(?!No)([ ])*(?!Need)([ ])*(?!to)([ ])*apologise|(?!No)([ ])*(?!Need)([ ])*(?!to)([ ])*apologize|I([ ])*apologise|I([ ])*apologize|My([ ])*apology|My([ ])*apologizing|Im([ ])*really([ ])*sorry|I([ ])*am([ ])*sorry|sorry|my([ ])*mistake|apologizing|Im([ ])*sorry|my([ ])*apologies";
     //String LABEL_NEGATIVE_APOLOGY="apologetic view|unapologetically| No need to apologi[z|s]e|apologist|apologists|No apologies necessary|apologetics";
     String LABEL_AGREEMENT="Agree totally|Agree completely|^[Agree]|I agree|I agree with|\\Wagree\\W|(!(agrees\\?))|\\bAgreed\\b|Im in agreement with|I am in agreement with|I\\'m in agreement with|I tend to agree";
     String LABEL_DISAGREEMENT="I dont see how|I sincerely question your motives|I honestly do not know|I am ignoring the arguments that make sense to you|I am ignoring your arguments|(!no) (!real) disagreement|I dont think so|I don\\'t think so|(!if) (!you) disagree|Strongly disagree[^s]|I disagree|It is not true";
     String LABEL_SUMMARY="In summary([\\,])|Summary([ ])*\\:|^[ |\\,]to summarise|^[ |\\,]to summarize([\\,|\\:|\\;])*";
     String LABEL_APPRECIATION="Thanks([ ])*([\\w+|\\,|\\!|\\.])|Thank([ ])*([\\w+|\\,|\\!|\\.])|Thank([ ])*you([ ])*[\\w+|\\,|\\!]|Thanks([ ])*for([ ])*the([ ])*info|Thanks\\!|thanks([ ])*again|appreciate|appreciated|will([ ])*be([ ])* appreciated";
     String LABEL_JUSTIFICATION="Wikipedia\\:Manual of Style|Wikipedia policy|\\[\\[WP\\:|WP\\:|I Justify this now|I\\'ve decided to go with|I have decided to go with|(!(you|your|please|how can you)) justify|(!(I dont think using any of these pictures could be|I dont think this can be|not|Is it|I dont see any such)) justification|The justifications for the changes are listed|The justifications are provided|The justifications are given|I am justified|The relevance has definitely been explained|I think it is justified|justifiably";
     String LABEL_REWORDING="re-worded|reworded|rewording|reword";
     String LABEL_REQUEST="Can anybody provide|please fix|Can anyone provide|Can you provide|Can you justify|Can somebody make|Can someone make|Can someone provide|Please justify|Please provide|Please\\, Can|Please can|Please let us know|Can somebody add this|Can someone add this|Please Check|please include|Opinions please|Can I know your opinion|May I know your opinion|I need|please show us";
     String LABEL_SUGGESTION="How about we include|How about adding|How about including|What about including|Can we include|Can we add|I think you should include|I think we should include|I suppose he could be included in|I suppose it could be included in|I suppose it could be included|why not include|Perhaps someone should include|we should include|This should be definetly included|This should be included|you could include it|it is desirable to include|it should be included|should probably also be included|should probably be included|we can include that|we can include|it might be included|it needs to be|we need to|it shold go in the article|we could add";
     String LABEL_APPRISE="(\\:|\\*|\\#)*Moved|Move done|(\\:|\\*|\\#)*Reworded|(!needs) (!to) (!be) done\\W+|I\\'ve done|I will delete it|I redid|Ive done|Ive moved|I have moved|I|I have just put in|I just did|I just undid|I have put in|I have put|Ive consolidated|I\\'ve consolidated|I have consolidated|I plan to |I([ ])*am planning to|I\\'m planning to|I will include|I will add|Ill include|Ill add|I\\'ll include|I\\'ll add|I\\'ve uploaded|I have uploaded|I uploaded|I corrected|I included|I\\'ve made some changes|Made some fixes|I added|I deleted|Updated the article";
     String LABEL_ACKNOWLEDGEMENT="I see what you mean|while it should be acknowledged|I acknowledge|I have to acknowledge|I acknowledged|is widely acknowledged";
     String LABEL_FORMATTING="Wikipedia\\:Article titles|formatting|WP\\:DASH|WP\\:YEAR|WP\\:MOSHEAD|WP\\:HEADINGS|MOS\\:\\&|WP\\:\\&|MOS\\:*|WP\\:NBSP|WP\\:MOSQUOTE|WP\\:PUNCT|WP\\:MOSLQ|WP\\:ELLIPSES|WP\\:ELLIPSIS|WP\\:COMMA|WP\\:HOWEVERPUNC|WP\\:HYPHEN|WP\\:MDASH|WP\\:EMDASH|WP\\:[a-zA-Z]*DASH|WP\\:SLASH|WP\\:ANDOR|WP\\:POUND|WP\\:REFPUNC|WP\\:REFSPACE|WP\\:FIRSTPERSON|WP\\:YOU|WP\\:PLURALS|WP\\:CONTRACTION|WP\\:JARGON|WP\\:MOSIM|WP\\:COMMENT|Wikipedia\\:Manual\\_of\\_Style|WP\\:BOLD";
     String LABEL_SPLITTING="I think if we split|How about splitting";
     String LABEL_CLARIFICATION="What is it|Which is it|How is it|How is that so";
     String LABEL_CONTROLLING="WP\\:Talk_Page_Guidelines";
     String LABEL_GRAMMAR="capitalized\\?";
     
     
     HashMap<String, Boolean> Label_Map=new HashMap<String, Boolean>();
     
     private Pattern POSITIVE_APOLOGY_PATTERN = Pattern.compile(LABEL_POSITIVE_APOLOGY, Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
     //private Pattern NEGATIVE_APOLOGY_PATTERN = Pattern.compile(LABEL_NEGATIVE_APOLOGY, Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
     private Pattern SUMMARY_PATTERN=Pattern.compile(LABEL_SUMMARY,Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
     private Pattern APPRECIATION_PATTERN=Pattern.compile(LABEL_APPRECIATION,Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
	 private Pattern AGREEMENT_PATTERN=Pattern.compile(LABEL_AGREEMENT, Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
	 private Pattern DISAGREEMENT_PATTERN=Pattern.compile(LABEL_DISAGREEMENT, Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
	 private Pattern JUSTIFICATION_PATTERN=Pattern.compile(LABEL_JUSTIFICATION, Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
	 private Pattern REWORDING_PATTERN=Pattern.compile(LABEL_REWORDING, Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
	 private Pattern REQUEST_PATTERN=Pattern.compile(LABEL_REQUEST, Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
     private Pattern SUGGESTION_PATTERN=Pattern.compile(LABEL_SUGGESTION,Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
     private Pattern APPRISE_PATTERN=Pattern.compile(LABEL_APPRISE,Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
     private Pattern ACKNOWLEDGEMENT_PATTERN=Pattern.compile(LABEL_ACKNOWLEDGEMENT, Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
     private Pattern FORMATTING_PATTERN=Pattern.compile(LABEL_FORMATTING, Pattern.CASE_INSENSITIVE| Pattern.UNICODE_CASE);
     
	 public static void main (String[] args) throws IOException{
		DiscTextLabelling dpp=new DiscTextLabelling();
		dpp.runExample();
	}

	public void runExample() throws FileNotFoundException {
		
		assign_label();
		
	}

	public void assign_label() throws FileNotFoundException {
		try {
			FileInputStream fstream = new FileInputStream("Formatting.txt"); // This is the input file
			DataInputStream in = new DataInputStream(fstream);
			BufferedReader br = new BufferedReader(new InputStreamReader(in));
			String strLine;
			while ((strLine = br.readLine()) != null)   {
				Label_Map.put("APOLOGY", POSITIVE_APOLOGY_PATTERN.matcher(strLine).find());
				Label_Map.put("SUMMARY", SUMMARY_PATTERN.matcher(strLine).find());
				Label_Map.put("APPRECIATION", APPRECIATION_PATTERN.matcher(strLine).find());
				Label_Map.put("AGREEMENT", AGREEMENT_PATTERN.matcher(strLine).find());
				Label_Map.put("DISAGREEMENT", DISAGREEMENT_PATTERN.matcher(strLine).find());
				Label_Map.put("JUSTIFICATION", JUSTIFICATION_PATTERN.matcher(strLine).find());
				Label_Map.put("REWORDING", REWORDING_PATTERN.matcher(strLine).find());
				Label_Map.put("REQUEST", REQUEST_PATTERN.matcher(strLine).find());
				Label_Map.put("SUGGESTION", SUGGESTION_PATTERN.matcher(strLine).find());
				Label_Map.put("APPRISE", APPRISE_PATTERN.matcher(strLine).find());
				Label_Map.put("ACKNOWLEDGEMENT", ACKNOWLEDGEMENT_PATTERN.matcher(strLine).find());
				Label_Map.put("FORMATTING", FORMATTING_PATTERN.matcher(strLine).find());
				
				FileWriter f_output_stream = new FileWriter("Formatting_test_1.txt",true); // This is the output file
				BufferedWriter output = new BufferedWriter(f_output_stream);
				Iterator iter = Label_Map.entrySet().iterator();
				output.write(strLine);
				System.out.println(strLine);
				while (iter.hasNext()) {
					Map.Entry mEntry = (Map.Entry) iter.next();
					System.out.println(strLine);
					output.write(strLine);
					if((boolean) mEntry.getValue())
					{
						//output.write(strLine);
						output.write("--"+mEntry.getKey());
					}
					System.out.println(mEntry.getKey() + " : " + mEntry.getValue());
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