import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Iterator;
import java.util.Properties;

public class UserManager {
	private static UserManager instance;
	private Properties userProps;
	private File dataFile;

	private UserManager() {
		userProps = new Properties();

		String userHome = System.getProperty("user.dir");
		dataFile = new File(userHome, "userdata.properties");
		if (!dataFile.exists()) {
			try {
				dataFile.createNewFile();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		} else {
			try {
				userProps.load(new FileInputStream(dataFile));
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}

	public static UserManager getInstance() {
		if (instance == null) {
			instance = new UserManager();
		}
		return instance;
	}
	
	public String getAllAsJSON(){
		StringBuffer sb=new StringBuffer("{");
		
		if(!userProps.isEmpty()){
			Iterator iKeys=userProps.keySet().iterator();
			while (iKeys.hasNext()) {
				String url = (String) iKeys.next();
				String user=userProps.getProperty(url);
				sb.append("\"").append(url).append("\":\"").append(user).append("\",");
			}
			sb.deleteCharAt(sb.length()-1);
		}
		
		sb.append("}");
		return sb.toString();
	}
	
	public void removeEntry(String url){
		userProps.remove(url);
	}

	public void updateEntry(String url, String user) {
		userProps.put(url, user);
	}

	public String getUser(String url) {
		Object user = userProps.get(url);
		return user == null ? "" : user.toString();
	}

	public void save() {
		try {
			FileOutputStream fos = new FileOutputStream(dataFile);
			userProps.store(fos, "");
			
			System.out.println(dataFile.getCanonicalPath());
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}	
	}
}
