#!/usr/bin/env python
import urllib2,urllib
import simplejson as json
import sys
import re

BASE_URL='https://rqmtuc03.storage.tucson.ibm.com/qm'

"""This class is used to operate on RQM"""
class RQM:

    projectAreaName="SONAS"
    projectAreaUUID=None

    opener=None

    def login(self,username,password):
        try:
            self.pass_rqmfw(username,password)

            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            urllib2.install_opener(self.opener)
            identity_url=BASE_URL+"/authenticated/identity"
            auth_url=BASE_URL+"/authenticated/j_security_check"
            params = urllib.urlencode(dict(j_username=username, j_password=password))
            p = self.opener.open(identity_url)
            p = self.opener.open(auth_url,params)
            p.close()

            self.opener.addheaders = [('Accept', 'text/json')]
        
        except AttributeError:
            sys.exit('Failed to log in the Rational Qulity Manager. Please check the connectivity and ensure the credential is correct.')
    
    def pass_rqmfw(self,username,password):
        headers = {'Content-type': 'application/x-www-form-urlencoded'}

        url='https://9.11.250.44/netaccess/connstatus.html'
        body={'login':'Log In Now','sid':'0'}
        req = urllib2.Request(url,urllib.urlencode(body),headers)
        req.get_method = lambda: 'POST'
        f=urllib2.urlopen(req)
        f.close()

        url = 'https://9.11.250.44/netaccess/loginuser.html'
        body = {'username': username,'password': password,'sid':'0'}
        req = urllib2.Request(url,urllib.urlencode(body),headers)
        req.get_method = lambda: 'POST'
        f=urllib2.urlopen(req)
        content=f.read()        
        f.close()

        if content.find('Log Out Now')!=-1:
		pass
#               print 'Passed the firewall for RQM successfully!'
        else:
                print 'Failed to pass the firewall for RQM.'

    def logout(self):
	url=BASE_URL+'/auth/logout'
        self.post(url)
        
    def form_filterparams(self,filters):
        testPhaseName=""
        stateIds=""
	ownerUUIDs=""
	testPlanUUIDs=""
	testPhaseUUIDs=""

	if filters.has_key('testPlanName'):
                testPlanName=filters['testPlanName']
                names=testPlanName.split(',')
                for name in names:
                    uuid=self.get_testplan_uuid(name)
                    testPlanUUIDs=testPlanUUIDs+"&vTestPlanItemIds="+uuid
        

        if filters.has_key('testPhaseName'):
	        testPhaseName=filters['testPhaseName']
                if testPhaseName.strip()!='':
                    names=testPhaseName.split(',')
                    for name in names:
                        uuid=None
                        testplan_names=testPlanName.split(',')
                        for testplan_name in testplan_names:
                            uuid=self.get_testphase_uuid(testplan_name,name)
                            if uuid!=None:
                                break
                        if uuid==None:
                            sys.exit('Failed to find the test phase ['+name+'] in the test plan ['+testPlanName+']')
                        testPhaseUUIDs=testPhaseUUIDs+"&testPhases="+uuid

	if filters.has_key('states'):
        	stateid_map={'Failed':'com.ibm.rqm.execution.common.state.failed','Blocked':'com.ibm.rqm.execution.common.state.blocked'}
            	states=filters['states']
            	for state in states:
                	try:
                    		state_id=stateid_map[state]
                	except KeyError as e:
                    		sys.exit('The state ['+state+'] is not supported in the query filter.')
               		stateIds=stateIds+'&stateIds='+state_id

	if filters.has_key('owners'):
		owneruuid_map={'Rui Shen':'_liu8wE9YEeCOgstpOMGrRA','Ting Jiang':'_OraH8GRaEeCOP53g_H25Xg','Zhen Quan Zhu':'_lgnc4E9YEeCOgstpOMGrRA','Ning Wang':'_lmIPAE9YEeCOgstpOMGrRA','Ling Ling Hu':'_lpYXUE9YEeCOgstpOMGrRA','Xiang Yu Song':'_lkepME9YEeCOgstpOMGrRA','Xiao Yan Tan':'_uM5WgH_qEeCOP53g_H25Xg'}
		owners=filters['owners']
		for owner in owners: 
                	try:
                        	owner_uuid=owneruuid_map[owner]
                        except KeyError as e:
                                sys.exit('The owner name ['+owner+'] is not supported in the query filter.')
	                ownerUUIDs=ownerUUIDs+'&ownerUUIDs='+owner_uuid

	return testPhaseUUIDs+testPlanUUIDs+stateIds+ownerUUIDs
 
    def query_execrecords(self,filters):
	filter_params=self.form_filterparams(filters)   
        url=BASE_URL+'/service/com.ibm.rqm.execution.common.service.rest.ITestcaseExecutionRecordRestService/pagedSearchResult?name=&'+filter_params+'&includeCustomAttributes=true&includeArchived=false&processArea='+self.getProjectAreaUUID()+'&page=0&sortColumns=modified%3ADESCENDING&pageSize=-1'

        content=self.get(url)
        jsonstr=json.loads(content)
	items=jsonstr['soapenv:Body']['response']['returnValue']['value']['results']
        return items
    
    """
    Generate a report to show associated defects
    """
    def get_ers_with_defects(self,filters):
        ers=self.query_execrecords(filters)
        i=0
        for er in ers:
            current_result_itemid=er["currentResultItemId"]
            last_result=self.get_lastresult(current_result_itemid)
            er['lastresult']=last_result
            ers[i]=er
            i=i+1
        return ers
   
    def sum_list(self,a,b):
        c=list()
        for i in range(len(a)):
            c.append(a[i]+b[i])
        return c

    """
    Genernate a report to show execution results by iteration 
    """
    def gen_report2(self,testplan_name,testphase_name):
        print 'This may take a few minutes, please be patient ...'
      
        total=[0,0,0,0,0,0,0,0]
        dataset=dict()

        plan_uuid=self.get_testplan_uuid(testplan_name)
        iter_names=testphase_name.split(',')
        for iter_name in iter_names:
            iteration_uuid=self.get_iteration_uuid(testplan_name,iter_name)
            
            if iteration_uuid==None:
                iteration_uuid=''

            subtotal=self.get_execdata(plan_uuid,iteration_uuid)
	    dataset[iter_name]=subtotal
            total=self.sum_list(total,subtotal)

            #print dataset
            #print total
        self.format_report(testplan_name,testphase_name,dataset,total)
 
    """
    Genernate a report to show execution results by category
    """
    def gen_report(self,testplan_name,testphase_name,has_detail):
        print 'This may take a few minutes, please be patient ...'
      
        total=[0,0,0,0,0,0,0,0]
        dataset=dict()

        plan_uuid=self.get_testplan_uuid(testplan_name)
        iter_names=testphase_name.split(',')
        for iter_name in iter_names:
            iteration_uuid=self.get_iteration_uuid(testplan_name,iter_name)
            
            if iteration_uuid==None:
                iteration_uuid=''

            subtotal=self.get_execdata(plan_uuid,iteration_uuid)
            total=self.sum_list(total,subtotal)

            if has_detail:
                filters={'testPlanName':testplan_name,'testPhaseName':testphase_name}
                items=self.query_execrecords(filters)
                categories=self.get_categories(items)
                for cat in categories:
                    cat_data=self.get_execdata(plan_uuid,iteration_uuid,cat)
                    if dataset.has_key(cat):
                        dataset[cat]=self.sum_list(dataset[cat],cat_data)
                    else:
                        dataset[cat]=cat_data
            #print dataset
            #print total
        self.format_report(testplan_name,testphase_name,dataset,total)
        
    def format_report(self,plan_name,iteration_name,dataset,total):
        # caculate the width of lable
        label_width=len('Category')
        for cat_name in dataset.keys():
            cat_name_len=len(cat_name)
            if cat_name_len>label_width:
                label_width=cat_name_len
        label_width=(label_width/8+1)*8
        
        total_width=label_width+8*8
    
        self.print_seperator('=',total_width)
        print 'Test Plan: %s' % plan_name
        print 'Test Iteration: %s' % iteration_name
        self.print_seperator('=',total_width)
        print 'Category'.rjust(label_width)+'\tU\tA\tP\tF\tB\tI\tPF\tD'
        """ 
        If detailed data is required, this seperator is printed
        """
        if len(dataset)>0:
            self.print_seperator('-',total_width)
        for cat_name in sorted(dataset.keys()):
            line=cat_name.rjust(label_width)
            for val in dataset[cat_name]:
                line=line+'\t'+str(val)
            print line
        self.print_seperator('-',total_width)
        line_total='Total'.rjust(label_width)
        for item in total:
            line_total=line_total+'\t'+str(item)
        print line_total
        self.print_seperator('=',total_width)
        #total=[float(item.replace(',','')) for item in total]
	print 'Exposed Rate: %d%%' % (round(float(total[1])/sum(total[0:2]),2)*100)
        print 'Success Rate: %d%%' % (round(float(total[2])/sum(total[0:2]),2)*100)
        print 'Blocked Rate: %d%%' % (round(float(total[4])/sum(total[0:2]),2)*100)
        self.print_seperator('=',total_width)
        print 'Legend:'
        print 'P - Passed'
        print 'F - Failed'
        print 'B - Blocked'
        print 'I - Inconclusive'
        print 'A - Attemtped'
        print 'N - Not started'
        print 'PF - PermFailed'
        print 'D - Deferred'
        
    def print_seperator(self, dot_str,width):
        line=''
        while width>=0:
            line=line+dot_str
            width=width-1
        print line
        
    def get_categories(self,items):
        categories=[]
        for item in items:
            testcase_id=item['testCaseId']
            category_name=self.get_category_name(testcase_id)
            categories.append(category_name)
        return set(categories)
            
    def get_category_name(self,testcase_id):
        url=BASE_URL+'/service/com.ibm.rqm.planning.common.service.rest.ITestCaseRestService/testCasesDTO?resolveWorkItems=true&includeArchived=true&id='+testcase_id+'&processArea='+self.getProjectAreaUUID()
        content=self.get(url)
        jsonstr=json.loads(content)
        category_name=jsonstr['soapenv:Body']['response']['returnValue']['values'][0]['categories'][1]['name']
        return category_name

    def getReportUUID(self):
        if self.projectAreaName=="SONAS":
            return "_xpOocCUHEeGzyoX6cj_Dpw"
        elif self.projectAreaName=="Unified GUI":
            return "_X8OnFUCYEeGH9fLtLwYHaw"
        else:
            sys.exit("The project area <"+self.projectAreaName+"> is not supported to get report UUID.")
    
    def getQueryUUID(self):
        if self.projectAreaName=="SONAS":
            return "_xqGyMCUHEeGzyoX6cj_Dpw"
        elif self.projectAreaName=="Unified GUI":
            return "_X8z15ECYEeGH9fLtLwYHaw"
        else:
            sys.exit("The project area <"+self.projectAreaName+"> is not supported to get query UUID.")

    def get_execdata(self,plan_id,iteration_id,category_name=''):
        url=BASE_URL+'/service/com.ibm.team.reports.common.internal.service.IReportRestService/renderReport'
        body='projectAreaUUID='+self.getProjectAreaUUID()+'&embeddable=true&parameterName=plan&parameterName=iteration&parameterName=testcase&parameterName=machine&parameterName=owner&parameterName=state&parameterName=category_testplan_type&parameterName=category_testplan_name&parameterName=category_testcase_type&parameterName=category_testcase_name&parameterName=width&parameterValue='+plan_id+'&parameterValue='+iteration_id+'&parameterValue=&parameterValue=&parameterValue=&parameterValue=&parameterValue=&parameterValue=&parameterValue=&parameterValue='+category_name+'&parameterValue=\'800\'&urlPrefix=%2Fjazz%2F&showArchived=false&getCached=false&reportUUID='+self.getReportUUID()+'&queryUUID='+self.getQueryUUID()

        content=self.post(url,body)

        jsonstr=json.loads(content)
        html_content=jsonstr['soapenv:Body']['response']['returnValue']['value']
        groups=re.findall('title="(\d*,?\d*)"',html_content)
        """
        groups=NotStarted,Attempted,Passed,Failed,Blocked,Inconclusive,Permfailed,Deferred
        """
        """
        Ideally, there should be 8 values in groups, but under some situation, it is not. So we need adjust.
        """
        if len(groups)!=8:
            temp=['0']*(8-len(groups))
            temp.extend(groups)
            groups=temp
        #groups.reverse()

        intgroups=list()
        for item in groups:
            item=item.replace(',','')
            intgroups.append(int(item))
        return intgroups
    
    def get_plan_uuid(self,plan_id):
        url=BASE_URL+'/service/com.ibm.rqm.integration.service.IIntegrationService/resources/SONAS/testplan/urn:com.ibm.rqm:testplan:'+plan_id
        content=self.get(url)
        print content
   
    def post(self,url,body={}):
        headers = {'Content-type': 'application/x-www-form-urlencoded; charset=utf-8','Accept':'text/json'}
        req = urllib2.Request(url,body,headers)
        req.get_method = lambda: 'POST'
        f=urllib2.urlopen(req)
        data=f.read()        
        f.close()
        return data

    def get(self,url):
        p=self.opener.open(url)
        data = p.read()
        p.close()
        return data

    def get_testphase_uuid(self,testplan_name,testphase_name):
        #testphase_name=testphase_name.replace(' ','%20')
        testplan_uuid=self.get_testplan_uuid(testplan_name)
        url=BASE_URL+'/service/com.ibm.rqm.process.common.service.rest.ITestPhaseRestService/testPhasesDTO?testPlanId='+testplan_uuid+'&processArea='+self.getProjectAreaUUID()
        content=self.get(url)
        jsonstr=json.loads(content)
        items=jsonstr['soapenv:Body']['response']['returnValue']['values']
        for item in items:
            if item['name']==testphase_name:
                return item['iterationItemId']
        return None

    def get_testplan_uuid(self,testplan_name):
        testplan_name=testplan_name.replace(' ','%20')
        url=BASE_URL+'/service/com.ibm.rqm.planning.common.service.rest.ITestPlanRestService/pagedSearchResult?myItemsOnly=false&includeCustomAttributes=true&includeArchived=false&processArea='+self.getProjectAreaUUID()+'&page=0&textSearch='+testplan_name+'&pageSize=10'
        content=self.get(url)
        jsonstr=json.loads(content)
        itemId=jsonstr['soapenv:Body']['response']['returnValue']['value']['results'][0]['versionableItemId']
        return itemId
    
    def get_iteration_uuid(self,testplan_name,iteration_name):
        testplan_uuid=self.get_testplan_uuid(testplan_name)
        url=BASE_URL+'/service/com.ibm.rqm.process.common.service.rest.ITestPhaseRestService/testPhasesDTO?jsonString=%7B%22testPlanId%22%3A%22'+testplan_uuid+'%22%7D&testPlanId='+testplan_uuid+'&processArea='+self.getProjectAreaUUID()
        content=self.get(url)
        jsonstr=json.loads(content)
        values=jsonstr['soapenv:Body']['response']['returnValue']['values']
        for value in values:
            if value['name']==iteration_name:
                return value['itemId']

    def get_plan_iteration_uuid(self,plan_name,iteration_name):
        url=BASE_URL+'/service/com.ibm.team.reports.common.internal.service.IReportRestService/parameterGroupValues?projectAreaUUID='+self.getProjectAreaUUID()+'&queryUUID=_8nSm5GpzEeGo6oLIJpejOg&reportUUID=_xpOocCUHEeGzyoX6cj_Dpw&showArchived=false&groupName=categories%20test%20case'
        content=self.get(url)
        jsonstr=json.loads(content)
        root=jsonstr['soapenv:Body']['response']['returnValue']['value']['parameters'][0]
        plan_labels=root['labels']
        plan_uuids=root['values']
        pos=plan_labels.index(plan_name)
        plan_uuid=plan_uuids[pos]
        iteration_labels=root['children'][pos]['labels']
        iteration_values=root['children'][pos]['values']
        iteration_uuid=iteration_values[iteration_labels.index(iteration_name)]
        return plan_uuid,iteration_uuid

        
    def get_lastresult(self,resultItemId):
        url=BASE_URL+'/service/com.ibm.rqm.execution.common.service.rest.IExecutionResultRestService/executionResultDTO?jsonString=%7B%22resolveDefects%22%3Atrue%2C%22resultItemId%22%3A%22'+resultItemId+'%22%7D&resultItemId='+resultItemId+'&resolveDefects=true&projectAreaItemId=_ENTk8NVNEd-H14PL1LejDA&isWebUI=true'
        content=self.get(url)
        jsonstr=json.loads(content)
        return jsonstr['soapenv:Body']['response']['returnValue']['value']


    def retrieveProjectAreaUUID(self,projectAreaName):
        projectAreaFullName=projectAreaName+" (Quality Management)"
        url=BASE_URL+'/service/com.ibm.team.process.internal.service.web.IProcessWebUIService/allProjectAreas?userId=shenrui%40cn.ibm.com'
        content=self.get(url)
        jsonstr=json.loads(content)
        projectAreas=jsonstr['soapenv:Body']['response']['returnValue']['values']
        for projectArea in projectAreas:
            if projectArea['name']==projectAreaFullName:
                self.projectAreaUUID=projectArea['itemId']
                break
        if self.projectAreaUUID==None:
            sys.exit('Failed to retireve UUID for the projectArea <'+projectAreaName+'>')

    def getProjectAreaUUID(self):
        if self.projectAreaUUID==None:
            self.retrieveProjectAreaUUID(self.projectAreaName)

        return self.projectAreaUUID
