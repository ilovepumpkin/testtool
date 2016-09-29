var users=new Array();
users.push(["---","---"]);
users.push(["shenrui","Shen Rui"]);
users.push(["sonia","Sonia"]);
users.push(["frank","Frank"]);
users.push(["ting","Jiang Ting"]);
users.push(["winnie","Wang Ning"]);
users.push(["hulingling","Hu Ling Ling"]);
users.push(["duanling","Duan Ling"]);
users.push(["liaojun","Liao Jun"]);
users.push(["dongjie","Dong Jie"]);
users.push(["minqi","Wu Min Qi"]);
users.push(["wenbao","Yin Wen Bao"]);
users.push(["external_team","External Team"]);


var xmlHttpReqs;
var xmlHttpUserReq;

var servers=new Array();
servers.push(["http://9.123.196.242:1080","SONAS","9.123.196.242 - st001<br>CLI: 1602 (root/Passw0rd)","FVT"]);
servers.push(["http://9.123.196.242:1082","SONAS","9.123.196.242 - st002<br>CLI: 1604 (root/Passw0rd)","FVT"]);
servers.push(["http://9.123.196.243:1080","SONAS","9.123.196.243 - st001<br>CLI: 1602 (root/Passw0rd)","FVT"]);
servers.push(["http://9.123.196.243:1082","SONAS","9.123.196.243 - st002<br>CLI: 1604 (root/Passw0rd)","FVT"]);
servers.push(["https://9.123.196.231:1081","IFS","CLI: 9.123.196.232 (SSH Port 1602 , root/Passw0rd) <br> Backend V7k: 9.123.196.225 <br>  Public IP: 9.123.196.234/235","FVT"]);
servers.push(["https://9.123.196.236:1081","IFS","CLI: 9.123.196.237 (SSH Port 1602 , root/Passw0rd) <br> Backend V7k: 9.123.196.219 <br> Public IP: 9.123.196.239/240","FVT"]);

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
		
		/*
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
		*/
		
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
	var servletUrl=temp.substring(0,temp.lastIndexOf('/'))+"/checkservice?product=sonas&platform="+url;
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
	//refreshUserInfo();
	updateTable();
}
