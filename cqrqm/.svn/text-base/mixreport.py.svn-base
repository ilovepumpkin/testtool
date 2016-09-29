#!/usr/bin/env python
from rqm.rqmlib import *
from cq.cqlib import *
from utils.datetimeutil import *
from utils.table import *

class Reporter:
    def __init__(self, username, password):
        self.username=username
        self.password=password
        
    def check_er_health(self,plan_name,iteration_name=None):
	timer=Timer()
	timer.start()
        ers=self.get_ers_with_defects(plan_name,iteration_name)
        print 'The following ERs are Failed/Blocked but without defects. Please check.'
        for er in ers:
            lastresult=er['lastresult']
            state=lastresult['state']['name']
            ewiname=lastresult['ewiName']
            if state in ['Failed','Blocked'] and len(er['defects'])==0:
                print ewiname
	timer.end('check the health of ERs')
        
    def propose_defect_fix_priority(self,plan_name,iteration_name,o_type):
        filters={'testPlanName':plan_name,'testPhaseName':iteration_name}
        ers=self.get_ers_with_defects(filters)
        defect_table={}
        defect_detail_table={}
        for er in ers:
            lastresult=er['lastresult']
            state=lastresult['state']['name']
            if state=='Failed':
                points_failed=lastresult['pointsFailed']
                defects=er['defects']
                defect_in_open_count=0
                defects_in_open=[]
                for defect in defects:
                    defect_id=defect['id']
                    defect_detail_table[defect_id]=defect
                    defect_state=defect['State']
                    if defect_state in ['Open','Working','Assigned','MoreInfo','Rejected']:
                        defects_in_open.append(defect_id)
                        defect_in_open_count+=1
                avg_failing_points=0
		if defect_in_open_count>0:
			avg_failing_points=round((points_failed*1.0)/defect_in_open_count)
                #print avg_failing_points
                for defect_id in defects_in_open:
                    if defect_id in defect_table:
                        defect_table[defect_id]=defect_table[defect_id]+avg_failing_points
                    else:
                        defect_table[defect_id]=avg_failing_points

        sorted_defect_table=sorted(defect_table.items(), key=lambda x: x[1],reverse=True) 

        rows=[]
        for item in sorted_defect_table:
            key=item[0]
            defect_detail=defect_detail_table[key]
            uid=defect_detail['Universal_Id']
            #owner=defect_detail['OwnerInfo'][0]['oslc_cm:label']
            owner=defect_detail['OwnerInfo']
            severity=defect_detail['Severity']
            headline=defect_detail['Headline']
            component=defect_detail['Component_Name']
            state=defect_detail['State']
            rowdata=[defect_table[key],uid,component,headline,severity,state,owner]
            rows.append(rowdata)

        colnames=['Failing Points','Universal Id','Component','Headline','Severity','State','Owner']

        displayer=TableDisplayer(colnames,rows)
        return displayer.format(o_type)
        
    def gen_ers_with_defects_report(self,*args,**kwargs):
      	timer=Timer()
	timer.start() 
	ers=self.get_ers_with_defects(kwargs)

	owners=set()
	for er in ers:
	    owner_name=er['ownerName']
	    owner_email=er['ownerUserId']
	    owners.add(owner_name)
	
	for owner in owners:
	    print '*************************************************************************************'
	    print '*************************************************************************************'
	    print owner
	    print '*************************************************************************************'
	    print '*************************************************************************************'
	  
            for er in ers:
		owner_name=er['ownerName']
		if owner_name==owner:
            		lastresult=er['lastresult']
            		ewiname=lastresult['ewiName']
            		points_attempted=lastresult['pointsAttempted']
            		points_passed=lastresult['pointsPassed']
                	points_failed=lastresult['pointsFailed']
                	points_inclusive=lastresult['pointsInconclusive']
                	points_blocked=lastresult['pointsBlocked']
                	state=lastresult['state']['name']
                	defects=er['defects']

			j=len(defects)
                	# cacluate non-closed defect count
			nonclosed_count=0
			for defect in defects:
				state=defect['State']
				if state!='Closed':
					nonclosed_count=nonclosed_count+1

			print '%s\tF:%s\tB:%s\t%s/%s' % (ewiname,points_failed,points_blocked,str(nonclosed_count),str(j))

			#sort defects by state
			while j>0:
        			i=0
        			while j-1>i:
                			a=defects[i]['State']
                			b=defects[i+1]['State']
               				if a>b:
                        			temp=defects[i]
                       				defects[i]=defects[i+1]
                        			defects[i+1]=temp
               				i=i+1
        			j=j-1	
			

                	for defect in defects:
	  	   		defect_id=defect['Universal_Id']
                   		defect_state=defect['State']
                   		defect_headline=defect['Headline']
                   		print '%s\t%s\t%s' % (defect_id,defect_state,defect_headline)
            
                	print '---------------------------------------------------------------------------------'
        timer.end('generate ers with defects report')

    def dbid2id(self,dbid):
         id_val=40000+(int(dbid)-33594432)
         return 'STORG'+str(id_val).rjust(8,'0')

    def get_ers_with_defects(self,filters):
	filters['states']=['Failed','Blocked']

        timer=Timer()
        timer.enabled=False
        timer.start()
        
        rqm=RQM()
        rqm.login(self.username,self.password)
        ers=rqm.get_ers_with_defects(filters)
        rqm.logout()

        timer.end('retrive all ER data')

        cq=ClearQuest()
#	cq.basic_login(self.username,self.password)
	cq.login(self.username,self.password)

        for er in ers:
            er_name=er['name']
            lastresult=er['lastresult']
            defect_list=[]
            try:
                defects=lastresult['defects']
                for defect in defects:
                    defecturl=defect['workItem']['itemId']
                    defect_id=defecturl[defecturl.index('-')+1:]
                    defect_id=self.dbid2id(defect_id)
		    timer.start()
		    timer.enabled=False
                    defect_list.append(cq.get_defect2(defect_id))
#                    defect_list.append(cq.get_defect(defect_id))
                    timer.end('get a defect data')
            except KeyError:
                pass
            er['defects']=defect_list
	cq.logout()
        return ers


