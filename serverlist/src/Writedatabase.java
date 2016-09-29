import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class Writedatabase extends HttpServlet {
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
		String comments = request.getParameter("comment");
		System.out.println("------------------------------------------------------");
		System.out.println(comments);
		// String strComment = "";
		// String strLine = "";
		// String strResult = "";
		
		try {
			File f = new File("/opt/database.txt");

			if (f.exists()) {
				System.out.println("File Exists@");

				BufferedWriter output = new BufferedWriter(new FileWriter(f));
				output.write(comments);

				output.close();
				System.out.println("Writing " + comments + " sucessfully");
			} else {
				System.out.println("File does not exist");
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}