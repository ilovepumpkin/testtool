import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;

import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.httpclient.ConnectTimeoutException;
import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.methods.GetMethod;
import org.apache.commons.httpclient.params.HttpConnectionParams;
import org.apache.commons.httpclient.protocol.Protocol;
import org.apache.commons.httpclient.protocol.SecureProtocolSocketFactory;

public class ServerStatusServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;

	// String Serverstatus = "Stopped";
	// String ClusterBuildNumber = "Unknow";
	// CIMClientTest getClusterBuildNo;

	/*
	 * public void getProved(String httpPrefix) { System.out.println("Server:" +
	 * httpPrefix); String httpsURL = httpPrefix.substring(8);
	 * Protocol.registerProtocol("https", new Protocol("https", new
	 * EasySSLProtocolSocketFactory(), 443)); HttpClient httpclient = new
	 * HttpClient(); GetMethod httpget1 = new GetMethod(httpPrefix);
	 * 
	 * try { int statusCode=httpclient.executeMethod(httpget1);
	 * System.out.println("status code:"+statusCode);
	 * 
	 * if (statusCode == 200) { System.out.println("Server is Here!");
	 * Serverstatus = "Running"; httpclient.executeMethod(httpget2);
	 * GUIBuildNumber=httpget2.getResponseBodyAsString();
	 * httpclient.executeMethod(httpget3);
	 * ClusterBuildNumber=httpget3.getResponseBodyAsString(); ClusterBuildNumber
	 * = getClusterBuildNo.getBuildNumber(httpsURL); //ClusterBuildNumber =
	 * "123"; }
	 * 
	 * } catch (IOException e) { // TODO Auto-generated catch block
	 * System.out.println("Server Error2"); e.printStackTrace(); } finally {
	 * httpget1.releaseConnection(); }
	 * 
	 * }
	 */

	public static String getSONASBuildNum(String url) {
		String guiverUrl = url + "/gui_version.txt";
		String hmiverUrl = url + "/hmi_version.txt";

		Protocol.registerProtocol("https", new Protocol("https",
				new EasySSLProtocolSocketFactory(), 443));

		HttpClient httpclient = new HttpClient();
		GetMethod httpget1 = new GetMethod(guiverUrl);
		GetMethod httpget2 = new GetMethod(hmiverUrl);

		String sonasVersion = "???";
		String guiVersion = "???";
		String hmiVersion = "???";

		try {
			int statusCode = 0;
			try {
				statusCode = httpclient.executeMethod(httpget1);
				if (statusCode == 200)
					guiVersion = httpget1.getResponseBodyAsString();
				guiVersion = guiVersion.trim();
			} catch (IOException ioe1) {
				System.err.println("Failed to get GUI version - " + guiverUrl);
				ioe1.printStackTrace();
			}

			try {
				statusCode = httpclient.executeMethod(httpget2);
				if (statusCode == 200) {
					hmiVersion = httpget2.getResponseBodyAsString();
					hmiVersion = hmiVersion.trim();
				}
			} catch (IOException ioe2) {
				System.err.println("Failed to get HMI version - " + hmiverUrl);
				ioe2.printStackTrace();
			}

			sonasVersion = guiVersion + " ( " + hmiVersion + " )";

		} finally {
			httpget1.releaseConnection();
			httpget2.releaseConnection();
		}
		return sonasVersion;
	}

	public void doGet(HttpServletRequest request, HttpServletResponse response)
			throws IOException, ServletException {

		String serverStatus = "stopped";
		String buildNumber = "unknown";
		CIMClientTest getClusterBuildNo = new CIMClientTest();
		PrintWriter out = response.getWriter();
		String strBuildNumberStatus = "";
		String platformURL = request.getParameter("platform");
		String product = request.getParameter("product");

		System.out
				.println("------------------------------------------------------");

		System.out.println(platformURL);
		String hostName = platformURL.substring(8);
		// add for ping
		// InetAddress ad = InetAddress.getByName(hostName);
		// boolean state = ad.isReachable(5000);
		// if(state){
		Protocol.registerProtocol("https", new Protocol("https",
				new EasySSLProtocolSocketFactory(), 443));
		HttpClient httpclient = new HttpClient();
		GetMethod httpget1 = new GetMethod(platformURL);

		try {
			int statusCode = httpclient.executeMethod(httpget1);
			if (statusCode == 200) {
				serverStatus = "running";
				if (product.equalsIgnoreCase("svc")) {
					// add for cimserver down
					buildNumber = new CIMClientTest().getBuildNumber(hostName);
					if (buildNumber == null || buildNumber.isEmpty()) {
						buildNumber = "cimon is down!!";
					}
				} else if (product.equalsIgnoreCase("sonas")) {
					buildNumber = getSONASBuildNum(platformURL);
				}
			}

		} catch (IOException e) {
			System.out.println("Server Error2");
			e.printStackTrace();
		} finally {
			httpget1.releaseConnection();
		}
		// }

		strBuildNumberStatus = "{\"status\":" + "\"" + serverStatus + "\"";
		strBuildNumberStatus += ",\"buildNo\":" + "\"" + buildNumber + "\"";
		strBuildNumberStatus += ",\"url\":" + "\"" + platformURL + "\"}";

		System.out.println("Server:" + strBuildNumberStatus);
		out.print(strBuildNumberStatus);
		out.close();
	}
}
