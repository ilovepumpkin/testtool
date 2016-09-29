var users=new Array();
users.push(["---","---"]);
users.push(["shenrui","Shen Rui"]);
users.push(["sonia","Sonia"]);
users.push(["frank","Frank"]);
users.push(["ting","Jiang Ting"]);
users.push(["winnie","Wang Ning"]);
users.push(["hulingling","Hu Ling Ling"]);
users.push(["duanling","Duan Ling"]);
users.push(["kezhao","Li Ke Zhao"]);
users.push(["wangmingming","Wang Ming Ming"]);
users.push(["liaojun","Liao Jun"]);
users.push(["dongjie","Dong Jie"]);
users.push(["minqi","Wu Min Qi"]);
users.push(["wenbao","Yin Wen Bao"]);
users.push(["external_team","External Team"]);


var xmlHttpReqs;
var xmlHttpUserReq;

var servers=new Array();
servers.push(["https://9.186.9.76","SVCGUI01","117478(9.186.9.77)<br>117556(9.186.9.78)","FVT"]);
servers.push(["https://9.186.9.81","SVCGUI02","117535(9.186.9.79)<br>117542(9.186.9.80)","FVT"]);
servers.push(["https://9.186.9.12","SVCGUI03","117543(9.186.9.82)<br>117563(9.186.9.83)","FVT"]);
servers.push(["https://guinness.cn.ibm.com","SVC-Guinness","9.123.199.153(gin104007.cn.ibm.com)<br>9.123.199.152(gin105640.cn.ibm.com)","FVT"]);
servers.push(["https://9.119.40.158","SVC-Newton","9.119.40.156(svc107756.cn.ibm.com)<br>9.119.40.157(svc107927.cn.ibm.com)","FVT"]);
servers.push(["https://9.186.12.35","SVC-Thinkstor","9.186.12.36(svc107925.cn.ibm.com)<br>9.186.12.37(svc107964.cn.ibm.com)","FVT"]);
servers.push(["https://9.186.12.81","SVC-Sydney","9.186.12.75(svc152112.cn.ibm.com)<br>9.186.12.76(svc152233.cn.ibm.com)","FVT"]);
servers.push(["https://9.186.12.64","SVC-Austin","9.186.12.77(svc152161.cn.ibm.com)<br>9.186.12.78(svc152231.cn.ibm.com)","FVT"]);
servers.push(["https://9.186.12.60","SVC-Fexpo","9.186.12.79(svc152215.cn.ibm.com)<br>9.186.12.83(svc152214.cn.ibm.com)","FVT"]);
//servers.push(["https://tbcluster-08.ssd.hursley.ibm.com","Storwize V7000-tbcluster-08","9.71.46.81(st0402.ssd.hursley.ibm.com)<br>9.71.46.241(st0420 .ssd.hursley.ibm.com)","FVT"]);
//servers.push(["https://gui-tbird-01.ssd.hursley.ibm.com","Storwize V7000-gui-tbird-01","9.71.46.134(gui-tbird-01a.ssd.hursley.ibm.com)<br>9.71.47.173(gui-tbird-01b.ssd.hursley.ibm.com)","FVT"]);
servers.push(["https://9.123.196.219","Storwize V7000-Lupus","lupus-a 9.123.196.220<br>lupus-b 9.123.196.221","FVT"]);
servers.push(["https://9.123.196.222","Storwize V7000-Lepus","lepus-a 9.123.196.223<br>lepus-b 9.123.196.224","FVT"]);
servers.push(["https://9.123.196.225","Storwize V7000-Phoenix","phoenix-a 9.123.196.226<br>phoenix-b 9.123.196.227","FVT"]);
servers.push(["https://9.123.196.228","Storwize V7000-Volans","volans-a 9.123.196.229<br>volans-b 9.123.196.230","FVT"]);
servers.push(["https://9.123.196.69","Storwize V7000-Pavo","9.123.196.70<br>9.123.196.71","FVT"]);
servers.push(["https://9.186.12.204","SVC-Aquila","9.186.12.205(151228)<br>9.186.12.206(151232)","Dev"]);
servers.push(["https://9.125.52.64","Storwize V7000-Bootes","9.125.52.73<br>9.125.52.74","Dev"]);
servers.push(["https://9.125.52.75","Storwize V7000-Gemini","9.125.52.76(78Z002A-1)<br>9.125.52.77(78Z002A-2)","Dev"]);
servers.push(["https://9.37.117.130","Nimitz - System 1","9.37.117.150<br>9.37.117.151","Raleign"]);
servers.push(["https://9.37.117.198","Nimitz - System 2","9.37.117.196<br>9.37.117.197","Raleign"]);
servers.push(["https://9.186.96.180","TBird4 - Peony","9.186.96.178(BG070KH-1)<br>9.186.96.179(BG070KH-2)","FVT"]);
servers.push(["https://9.186.96.183","TBird4 - Molly","9.186.96.181(BG074C9-1)<br>9.186.96.182(BG074C9-2)","DEV"]);
servers.push(["https://9.186.96.223","TBird4 - Glory","9.186.96.221(BG074D1-1)<br>9.186.96.222(BG074D1-2)","FVT"]);
servers.push(["https://9.186.96.226","TBird4 - Daisy","9.186.96.224(BG074CD-1)<br>9.186.96.225(BG074CD-2)","FVT"]);

function initXmlHttpReqsArray(){
	xmlHttpReqs=new Array();
	for(k=0;k<servers.length;k++){
		xmlHttpReqs.push(createXMLHttpRequest());
	}
}

function initTable(){
	var mytable=document.getElementById('mytable');
	var mytbody=mytable.getElementsByTagName('TBODY')[0];
	mytbody.innerHTML="";
	
	for(i=0;i<servers.length;i++){
		var server=servers[i];
		var url=server[0];
		var name=server[1];
		var node_ips=server[2];
		var ownedBy=server[3];

		var tr=document.createElement("TR");
		if(i%2==0){
			tr.className="even";
		}else{
			tr.className="odd";
		}
		
		var tdStatus=document.createElement("TD");
		tdStatus.id="status"+i;
		tdStatus.align="center";
		tdStatus.innerHTML="<img id = 'img"+i+"' src = 'images/indicator_mozilla_blu.gif'>";
		tr.appendChild(tdStatus);
		
	    var tdUrl=document.createElement("TD");
		tdUrl.innerHTML="<a href='"+url+"'>"+url+"</a>";
		tr.appendChild(tdUrl);

		var tdBuild=document.createElement("TD");
		tdBuild.id="buildNo"+i;
		tdBuild.innerHTML='unknown';
		tr.appendChild(tdBuild);
		
		var tdOwnedBy=document.createElement("TD");
		tdOwnedBy.innerHTML=ownedBy;
		tr.appendChild(tdOwnedBy);

		var tdOwner=document.createElement("TD");
		var userSelect=document.createElement("Select");
		userSelect.setAttribute("url",url);
		userSelect.setAttribute("id",url);
		for(k=0;k<users.length;k++){
			var user=users[k];
			var userid=user[0];
			var username=user[1];

			var anOption = document.createElement("OPTION");
			anOption.text=username;
			anOption.value=userid;
			userSelect.options.add(anOption);
			userSelect.onchange=function(event){userOnChange(event);};
		}
		tdOwner.appendChild(userSelect);
		tr.appendChild(tdOwner);

		var tdName=document.createElement("TD");
		tdName.innerHTML=name;
		tr.appendChild(tdName);
		
		var tdNodeIPs=document.createElement("TD");
		tdNodeIPs.innerHTML=node_ips;
		tr.appendChild(tdNodeIPs);

		mytbody.appendChild(tr);
	}
}

function userOnChange(evt){
	var oSelect=evt.target;
	var opts=oSelect.options;
	for(i=0;i<opts.length;i++){
		var opt=opts[i];
		if(opt.selected==true){
			var user=opt.value;
			var url=oSelect.getAttribute("url");
			var xmlHttpReq=createXMLHttpRequest();
			var temp=new String(window.location);
			var servletUrl=temp.substring(0,temp.lastIndexOf('/'))+"/userservice?action=save&url="+url+"&user="+user;
			xmlHttpReq.open("GET", servletUrl, true);
			xmlHttpReq.onreadystatechange = function(){
				
			};
		    xmlHttpReq.send(null);
		}
	}
	
}

function refreshUserInfo(){
	xmlHttpUserReq=createXMLHttpRequest();
	var temp=new String(window.location);
	var servletUrl=temp.substring(0,temp.lastIndexOf('/'))+"/userservice?action=loadall";
	xmlHttpUserReq.open("GET", servletUrl, true);
	xmlHttpUserReq.onreadystatechange = callbackUserInfo;
	xmlHttpUserReq.send(null);
}

function callbackUserInfo(){
	var respText = xmlHttpUserReq.responseText;
	jsonObj = respText.parseJSON();

	for(j=0;j<servers.length;j++){
		var server=servers[j];
		var url=server[0];
		
		var user=jsonObj[url];
		if(user!=""){
			var userSelect=document.getElementById(url);
			var opts=userSelect.options;
			for(i=0;i<opts.length;i++){
				var opt=opts[i];
				if(opt.value==user){
					opt.selected=true;
				}	
			}
		}
	}
}

function createXMLHttpRequest()
{
	if(window.ActiveXObject)
	{
		return new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	else if(window.XMLHttpRequest)
	{
		return new XMLHttpRequest();
	}
}	

function callBackFunc(idx)
{

	if(xmlHttpReqs[idx].readyState == 4)
	{
		if(xmlHttpReqs[idx].status == 200)
		{
			var JsonTextFromServer = xmlHttpReqs[idx].responseText;
			jsonObject = JsonTextFromServer.parseJSON();
	
			if(jsonObject.status == "stopped")
			{
				document.getElementById("img" + idx).src = "images/vm-power-off.png";
			}			
			else
			{
				document.getElementById("img" + idx).setAttribute("src", "images/vm-power-on.png");
			}
			document.getElementById("buildNo" + idx).innerHTML = jsonObject.buildNo;
		}
	}
}

function check(idx)
{
	var server=servers[idx];
	var url=server[0];
	var xmlHttpReq=xmlHttpReqs[idx];
	var temp=new String(window.location);
	var servletUrl=temp.substring(0,temp.lastIndexOf('/'))+"/checkservice?product=svc&platform="+url;
	xmlHttpReq.open("GET", servletUrl, true);
	xmlHttpReq.onreadystatechange = function(){
		callBackFunc(idx);
	};
    xmlHttpReq.send(null);
    xmlHttpReqs[idx]=xmlHttpReq;
}



function updateTable(){
	for(j=0;j<servers.length;j++){
		check(j);
	}
}

function refresh(){
	initTable();
	initXmlHttpReqsArray();
	refreshUserInfo();
	updateTable();
}
