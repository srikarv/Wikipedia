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

import sun.misc.IOUtils;



public class ArticleEditHistoryDownload{
  
	public static void main (String[] args) throws IOException{
		ArticleEditHistoryDownload obj=new ArticleEditHistoryDownload();
		//obj.get_revids(); //get revision ids
		obj.get_rev_info(); //get revision info
	}
	
	public void get_rev_info() throws IOException {
		FileInputStream fstream = new FileInputStream("FA_Article_Revision_ids_NEWER.txt");
		DataInputStream in_stream = new DataInputStream(fstream);
		BufferedReader br = new BufferedReader(new InputStreamReader(in_stream)); 
		String strLine;
		//start reading the files here
		 while ((strLine=br.readLine()) != null)
		 {
			 try
			 {
				 String article=strLine.split(";")[0];
				 int rev_id=Integer.parseInt(strLine.split(";")[1]);
				 int parent_id=Integer.parseInt(strLine.split(";")[2]);
				 String minor=strLine.split(";")[3];
				 String user=strLine.split(";")[4];
				 String timestamp=strLine.split(";")[5];
				 int size=Integer.parseInt(strLine.split(";")[6]);
				//String comment=strLine.split(";")[7];				 
			 
			 
			System.out.println("NOW DOWNLOADING THE PAGE FOR:"+article+" REVISION:"+rev_id+"\n");
			URL u = new URL("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles="+article+"&rvstartid="+rev_id+"&rvendid="+rev_id+"&rvprop=content&format=xml");
			HttpURLConnection uc = (HttpURLConnection) u.openConnection();
			InputStream in = new BufferedInputStream(uc.getInputStream());
			
				 File targetFile = new File(article+"_1_RevHistory_GA.xml");
				 OutputStream outStream = new FileOutputStream(targetFile);
				 
	     		 byte[] buffer = new byte[8 * 1024];
				 int bytesRead;
				 while ((bytesRead = in.read(buffer)) != -1) 
				 {
				        outStream.write(buffer, 0, bytesRead);
				 }
				 in.close();
				 outStream.close();
				 DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
				//Using factory get an instance of document builder
				 DocumentBuilder db = dbf.newDocumentBuilder();

					//parse using builder to get DOM representation of the XML file
				 Document dom = db.parse(article+"_1_RevHistory_GA.xml");
					//get the root element
				 Element docEle = dom.getDocumentElement();
					//get a nodelist of elements
				NodeList nl = docEle.getElementsByTagName("rev");	
				if(nl != null && nl.getLength() > 0) 
				{
					Element el = (Element)nl.item(0);
					String rev_text=el.getFirstChild().getNodeValue();
					System.out.println("Revision_text:"+rev_text);
					BufferedWriter output_file1=new BufferedWriter(new FileWriter(article+"_rev_text_GA.txt",true));
					output_file1.write(article+";~"+rev_id+";~"+parent_id+";~"+minor+";~"+user+";~"+timestamp+";~"+size+";~"+rev_text.replaceAll("(\\r|\\n)", "")+"\n");
					output_file1.close();					
				}
				targetFile.delete();
				uc.disconnect();
			 }
			 
				catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			 
			
		 }
		
	}

	public void get_revids() throws IOException 
	{
		FileInputStream fstream = new FileInputStream("Talk_Page_List_FA.txt");
		DataInputStream in_stream = new DataInputStream(fstream);
		BufferedReader br = new BufferedReader(new InputStreamReader(in_stream)); 
		 String strLine;
		//start reading the files here
		 while ((strLine=br.readLine()) != null)
		 {
		 System.out.println("Now Downloading the page for '"+strLine+"'");
		 
		 //URL u = new URL("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles="+strLine+"&rvprop=timestamp|user|comment|content|flags|ids|size|tags&rvlimit=50&format=xml");
		 URL u = new URL("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvlimit=500&titles="+strLine+"&rvdir=newer&rvcontinue=true&rvprop=timestamp|user|comment|flags|ids|size|tags&format=xml");
		 HttpURLConnection uc = (HttpURLConnection) u.openConnection();
		 InputStream in = new BufferedInputStream(uc.getInputStream());
		 try {
			 File targetFile = new File(strLine+"_1_RevHistory_FA.xml");
			 OutputStream outStream = new FileOutputStream(targetFile);
			 
     		 byte[] buffer = new byte[8 * 1024];
			 int bytesRead;
			 while ((bytesRead = in.read(buffer)) != -1) 
			 {
			        outStream.write(buffer, 0, bytesRead);
			 }
			 in.close();
			 outStream.close();
			 DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();

			//Using factory get an instance of document builder
				DocumentBuilder db = dbf.newDocumentBuilder();

				//parse using builder to get DOM representation of the XML file
				Document dom = db.parse(strLine+"_1_RevHistory_FA.xml");
				//get the root element
				Element docEle = dom.getDocumentElement();
				//get a nodelist of elements
				NodeList nl = docEle.getElementsByTagName("rev");
				if(nl != null && nl.getLength() > 0) 
				{
					//System.out.println("Not NULL");
					for(int i = 0 ; i < nl.getLength();i++) 
					{
						Element el = (Element)nl.item(i);
						String rev_id=el.getAttribute("revid");
						String parent_id=el.getAttribute("parentid");
						String minor=el.getAttribute("minor");
						String user=el.getAttribute("user");
						String timestamp=el.getAttribute("timestamp");
						String size=el.getAttribute("size");
						String comment=el.getAttribute("comment");
						BufferedWriter output_file=new BufferedWriter(new FileWriter("FA_Article_Revision_ids_NEWER.txt",true));
						output_file.write(strLine+";"+rev_id+";"+parent_id+";"+minor+";"+user+";"+timestamp+";"+size+";"+comment+";\n");
						output_file.close();
       			}
					
								
				}
				targetFile.delete();
			    }
		 
			catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		 
		 uc.disconnect();
		 URL u1 = new URL("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvlimit=500&titles="+strLine+"&rvcontinue=true&rvprop=timestamp|user|comment|flags|ids|size|tags&format=xml");
		 HttpURLConnection uc1 = (HttpURLConnection) u1.openConnection();
		 InputStream in1 = new BufferedInputStream(uc1.getInputStream());
		 try {
			 File targetFile1 = new File(strLine+"_1_RevHistory_FA.xml");
			 OutputStream outStream1 = new FileOutputStream(targetFile1);
			 
     		 byte[] buffer1 = new byte[8 * 1024];
			 int bytesRead1;
			 while ((bytesRead1 = in1.read(buffer1)) != -1) 
			 {
			        outStream1.write(buffer1, 0, bytesRead1);
			 }
			 in1.close();
			 outStream1.close();
			 DocumentBuilderFactory dbf1 = DocumentBuilderFactory.newInstance();

			//Using factory get an instance of document builder
				DocumentBuilder db1 = dbf1.newDocumentBuilder();

				//parse using builder to get DOM representation of the XML file
				Document dom1 = db1.parse(strLine+"_1_RevHistory_FA.xml");
				//get the root element
				Element docEle1 = dom1.getDocumentElement();
				//get a nodelist of elements
				NodeList nl1 = docEle1.getElementsByTagName("rev");
				//System.out.println("Node Length:"+nl.getLength());
				if(nl1 != null && nl1.getLength() > 0) 
				{
					//System.out.println("Not NULL");
					for(int i = 0 ; i < nl1.getLength();i++) 
					{
						Element el1 = (Element)nl1.item(i);
						String rev_id=el1.getAttribute("revid");
						String parent_id=el1.getAttribute("parentid");
						String minor=el1.getAttribute("minor");
						String user=el1.getAttribute("user");
						String timestamp=el1.getAttribute("timestamp");
						String size=el1.getAttribute("size");
						String comment=el1.getAttribute("comment");
						BufferedWriter output_file1=new BufferedWriter(new FileWriter("FA_Article_Revision_ids_OLDER.txt",true));
						output_file1.write(strLine+";"+rev_id+";"+parent_id+";"+minor+";"+user+";"+timestamp+";"+size+";"+comment+"\n");
						output_file1.close();

						
					}
					
								
				}
				targetFile1.delete();

			    }
		 
			catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		 uc1.disconnect();
  }
	        
		
	}

	 
	}
