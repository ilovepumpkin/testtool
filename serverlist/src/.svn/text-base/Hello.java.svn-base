import java.io.IOException;
import java.net.InetAddress;
import java.net.UnknownHostException;


import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.HttpException;
import org.apache.commons.httpclient.methods.GetMethod;
import org.apache.commons.httpclient.protocol.Protocol;

public class Hello {

	/**
	 * @param args
	 * @throws IOException
	 * @throws HttpException
	 */
	public static void main(String[] args) throws HttpException, IOException {
		/*
		Protocol.registerProtocol("https", new Protocol("https",
				new EasySSLProtocolSocketFactory(), 443));
		HttpClient httpclient = new HttpClient();
		GetMethod httpget = new GetMethod("https://cim-svc-cluster-3.tivlab.austin.ibm.com");
		try {
			System.out.println("here");
			httpclient.executeMethod(httpget);
			System.out.println(httpget.getStatusLine());
		} finally {
			httpget.releaseConnection();
		}
		*/
		try
		{
		InetAddress ad = InetAddress.getByName("www.baidu.com");
		boolean state = ad.isReachable(5000);//
		
		if(state)
		System.out.println("" + ad.getHostAddress());
		else{
			System.err.println("");
			System.out.println("not availabe");
		}
		
		}
		catch(UnknownHostException e)
		{
		System.err.println("");
		}

	}

}
