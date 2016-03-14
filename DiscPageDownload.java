import java.io.*;
import java.net.*;
//import java.nio.ByteBuffer;
//import java.nio.CharBuffer;
//import java.nio.channels.FileChannel;
//import java.nio.charset.Charset;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.xml.sax.SAXException;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;



public class DiscPageDownload{
  
	public static void main (String[] args) throws IOException{
		FileInputStream fstream = new FileInputStream("final_output_file_FA.txt");
		DataInputStream in_stream = new DataInputStream(fstream);
		BufferedReader br = new BufferedReader(new InputStreamReader(in_stream)); 
		 String strLine;
		//start reading the files here
		 while ((strLine=br.readLine()) != null){
		 Pattern pattern = Pattern.compile("/");
		 Matcher matcher = pattern.matcher(strLine);
		 System.out.println("Now Downloading the page for '"+strLine+"'");
		// String keyword=strLine;
		 //if it is an archive file then append the comments to the same page 
		 /*if(matcher.find())
		 {
			//int i=matcher.group().indexOf('/');
			//System.out.println("i="+i);
			keyword=strLine.split("/")[0];
			System.out.println("Keyword"+keyword);
		 }*/
		BufferedWriter output_file =matcher.find()? new BufferedWriter(new FileWriter(strLine.split("/")[0]+".xml", true)):new BufferedWriter(new FileWriter(strLine+".xml"));// this opens the file in append mode
		 
		 URL u = new URL("http://en.wikipedia.org/wiki/Special:Export/Talk:"+strLine);
		 HttpURLConnection uc = (HttpURLConnection) u.openConnection();
		 InputStream in = new BufferedInputStream(uc.getInputStream());
		// Reader r = new InputStreamReader(in);
		 DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		 try {
			DocumentBuilder db = dbf.newDocumentBuilder();
			Document dom = db.parse(in);
			Element docEle = dom.getDocumentElement(); // get the root element
			NodeList nl = docEle.getElementsByTagName("text");
			if(nl.item(0)==null)
				continue;
			Element el = (Element)nl.item(0);
			String str=el.getFirstChild().getNodeValue();
			if(str!=null)
			{
			output_file.write(el.getFirstChild().getNodeValue());// write the value of text
			}
			else
				continue;
		 }
			catch (ParserConfigurationException | SAXException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		 output_file.write("\n\n\n\n\n\n\n\n");
		 output_file.close(); 
  }
		 
	}
}