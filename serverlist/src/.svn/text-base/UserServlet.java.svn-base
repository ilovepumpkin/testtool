import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class UserServlet extends HttpServlet {

	public void doGet(HttpServletRequest request, HttpServletResponse response)
			throws IOException, ServletException {

		UserManager userManager = UserManager.getInstance();

		String action = request.getParameter("action");

		if (action.equals("save")) {
			String url = request.getParameter("url");
			String user = request.getParameter("user");

			if (user.equals("---")) {
				userManager.removeEntry(url);
			} else {
				userManager.updateEntry(url, user);
			}
			userManager.save();

		} else if (action.equals("loadall")) {
			String allJSON = userManager.getAllAsJSON();
			PrintWriter out = response.getWriter();
			out.print(allJSON);
			out.close();
		}
	}
}
