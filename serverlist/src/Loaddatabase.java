import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class Loaddatabase extends HttpServlet {
	private static final long serialVersionUID = 1L;

	public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
		PrintWriter out = response.getWriter();
		System.out.println("------------------------------------------------------");
		String platformURL = request.getParameter("comment");
		System.out.println(platformURL);
		String strComment = "";
		String strLine = "";
		String strResult = "";

		try {
			File f = new File("/opt/database.txt");

			if (f.exists()) {
				System.out.println("File exists");

				BufferedReader input = new BufferedReader(new FileReader(f));

				while ((strLine = input.readLine()) != null) {
					strComment += strLine;
				}

				input.close();
			} else {
				System.out.println("File does not exist");

				if (f.createNewFile()) {
					System.out.println("File created sucessfully");
				} else {
					System.out.println("File created failed");
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}

		strResult = "{\"Comments\":" + "\"" + strComment + "\"}";

		System.out.println(strResult);
		out.print(strResult);
		out.close();

	}
}