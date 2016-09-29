import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;

import com.sun.net.ssl.TrustManagerFactory;
import com.sun.net.ssl.TrustManager;
import com.sun.net.ssl.X509TrustManager;
import org.apache.commons.logging.Log; 
import org.apache.commons.logging.LogFactory;

public class EasyX509TrustManager implements X509TrustManager {
	private X509TrustManager standardTrustManager = null;

	/*** Log object for this class. */
	private static final Log LOG = LogFactory
			.getLog(EasyX509TrustManager.class);

	/***
	 * Constructor for EasyX509TrustManager.
	 */
	public EasyX509TrustManager(KeyStore keystore)
			throws NoSuchAlgorithmException, KeyStoreException {
		super();
		TrustManagerFactory factory = TrustManagerFactory
				.getInstance("SunX509");
		factory.init(keystore);
		TrustManager[] trustmanagers = factory.getTrustManagers();
		if (trustmanagers.length == 0) {
			throw new NoSuchAlgorithmException(
					"SunX509 trust manager not supported");
		}
		this.standardTrustManager = (X509TrustManager) trustmanagers[0];
	}

	/***
	 * @see com.sun.net.ssl.X509TrustManager#isClientTrusted(X509Certificate[])
	 */
	public boolean isClientTrusted(X509Certificate[] certificates) {
		return this.standardTrustManager.isClientTrusted(certificates);
	}

	/***
	 * @see com.sun.net.ssl.X509TrustManager#isServerTrusted(X509Certificate[])
	 */
	public boolean isServerTrusted(X509Certificate[] certificates) {
		if ((certificates != null) && LOG.isDebugEnabled()) {
			LOG.debug("Server certificate chain:");
			for (int i = 0; i < certificates.length; i++) {
				LOG.debug("X509Certificate[" + i + "]=" + certificates[i]);
			}
		}
		if ((certificates != null) && (certificates.length == 1)) {
			X509Certificate certificate = certificates[0];
			try {
				certificate.checkValidity();
			} catch (CertificateException e) {
				LOG.error(e.toString());
				return false;
			}
			return true;
		} else {
			return this.standardTrustManager.isServerTrusted(certificates);
		}
	}

	/***
	 * @see com.sun.net.ssl.X509TrustManager#getAcceptedIssuers()
	 */
	public X509Certificate[] getAcceptedIssuers() {
		return this.standardTrustManager.getAcceptedIssuers();
	}


}
