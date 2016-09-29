import java.net.MalformedURLException;
import java.net.URL;
import java.util.Locale;

import javax.cim.CIMInstance;
import javax.cim.CIMObjectPath;
import javax.security.auth.Subject;
import javax.wbem.CloseableIterator;
import javax.wbem.WBEMException;
import javax.wbem.client.PasswordCredential;
import javax.wbem.client.UserPrincipal;
import javax.wbem.client.WBEMClient;
import javax.wbem.client.WBEMClientConstants;
import javax.wbem.client.WBEMClientFactory;

public class CIMClientTest {

	/**
	 * @param args
	 * @throws WBEMException
	 * @throws MalformedURLException
	 */
	public static void main(String[] args) throws WBEMException,
			MalformedURLException {
		/*
		System.out.println("server1");
		System.out.println(new CIMClientTest().getBuildNumber("9.123.199.154"));
		
		System.out.println("server2");
		System.out.println(new CIMClientTest().getBuildNumber("newton.cn.ibm.com"));
		
		System.out.println("server3");
		System.out.println(new CIMClientTest().getBuildNumber("thinkstor.cn.ibm.com"));
		System.out.println("server4");
		System.out.println(new CIMClientTest().getBuildNumber("9.186.12.60"));
		System.out.println("server5");
		System.out.println(new CIMClientTest().getBuildNumber("9.186.12.65"));
		System.out.println("server6");
		System.out.println(new CIMClientTest().getBuildNumber("9.186.12.82"));
		System.out.println("server7");
		System.out.println(new CIMClientTest().getBuildNumber("9.123.199.13"));
		System.out.println("server8");
		System.out.println(new CIMClientTest().getBuildNumber("tbcluster-08.ssd.hursley.ibm.com"));
		System.out.println("server9");		
		System.out.println(new CIMClientTest().getBuildNumber("tbcluster-07.ssd.hursley.ibm.com"));
		*/
		//System.out.println("server10");		
		System.out.println(new CIMClientTest().getBuildNumber("9.37.117.189"));
		/*
		System.out.println("server11");		
		System.out.println(new CIMClientTest().getBuildNumber("collingwood.ssd.hursley.ibm.com"));
		System.out.println("server12");		
		System.out.println(new CIMClientTest().getBuildNumber("flintoff.ssd.hursley.ibm.com"));
		
		System.out.println("server13");		
		System.out.println(new CIMClientTest().getBuildNumber("cim-svc-cluster-3.tivlab.austin.ibm.com"));
		*/
	}
	
	
	public String getBuildNumber(String ip) {
		try {
			
			URL cimomUrl = new URL("https://" + ip + ":5989");
			String user = "superuser";
			String pw = "passw0rd";
			
			/*
			final WBEMClient client = WBEMClientFactory
					.getClient(WBEMClientConstants.PROTOCOL_CIMXML);
			final CIMObjectPath path = new CIMObjectPath(
					cimomUrl.getProtocol(), cimomUrl.getHost(), String
							.valueOf(cimomUrl.getPort()), null, null, null); */
			
			final WBEMClient client = WBEMClientFactory
			.getClient("CIM-XML"); 
			/*
			final CIMObjectPath path = new CIMObjectPath(
					"https", "9.71.46.136", "5989", "root/ibm", null, null); 	*/
			final CIMObjectPath path = new CIMObjectPath(
					cimomUrl.getProtocol(), cimomUrl.getHost(), String
							.valueOf(cimomUrl.getPort()), "root/ibm", null, null);
			
			
			final Subject subject = new Subject();
			subject.getPrincipals().add(new UserPrincipal(user));
			subject.getPrivateCredentials().add(new PasswordCredential(pw));

			//client.initialize(path, subject, Locale.getAvailableLocales());
			client.initialize(path, subject, new Locale[] { Locale.US });
			
			CIMObjectPath clusterPath = new CIMObjectPath("IBMTSSVC_Cluster",
					"root/ibm");

			CloseableIterator e = (CloseableIterator) client
					.enumerateInstances(clusterPath, false, false, false, null);
			CIMInstance inst = (CIMInstance) e.next();		
			return (String) inst.getProperty("CodeLevel").getValue();
			
			
		} catch (WBEMException e) {
			e.printStackTrace();
		} catch (MalformedURLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}

}
