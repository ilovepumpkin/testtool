#!/usr/bin/env python
#coding=utf-8
import simplejson as json
import urllib2

TYPE_ID = '16777224'
class Defect:
     did = ''
     headline = ''
     severity = ''
     priority = ''
     description =''
     
class ClearQuest:
        def __init__(self,base_url,repository,database):
                self.base_url=base_url
                self.repository=repository
                self.database=database

        def basic_login(self, username, password):
                auth_handler = urllib2.HTTPBasicAuthHandler()
                auth_handler.add_password(realm=self.repository,uri=self.base_url,user=username,passwd=password)
                opener = urllib2.build_opener(auth_handler)
                urllib2.install_opener(opener)
                print 'Log in the Clear Quest successfully.'

        def create_defect(self,defect):
                dic = {"dc:type": {
                            "rdf:resource":self.base_url+"record-type/"+TYPE_ID,
                            "name":"Defect"
                        },
                        "Headline":defect.headline,
                        "Severity":defect.severity,
                        "Priority":defect.priority,
                        "Description":defect.description
                      }
                url = self.base_url+'/record'
                fields = json.dumps(dic)
                headers={'Content-type': 'application/json;charset=utf-8'}
                req = urllib2.Request(url,fields,headers)
                #f=None
                f = urllib2.urlopen(req)
                location = f.info().getheader('Location')
                pef = '-'
                defect_id = location[location.find(pef)+1:]
                the_page = f.read()
                print 'Create defect '+defect_id+" successfully."
                return defect_id

        def get_defect(self,defect_id):
                base_query_url=self.base_url+'/record/'+TYPE_ID+'-'+defect_id+'?rcm.contentType=application/json'
                handle =urllib2.urlopen(base_query_url)
                #req=None
                try:
                    req=handle.read()
                    jsonstr=json.loads(req)
                    defect = Defect()
                    defect.headline = jsonstr['Headline']
                    defect.severity = jsonstr['Severity']
                    defect.priority = jsonstr['Priority']
                    defect.description = jsonstr['Description']
                    print "Get defect "+defect_id+" successfully."
                    print 'Headline: '+jsonstr['Headline']
                    print 'Severity: '+jsonstr['Severity']
                    print 'Priority: '+jsonstr['Priority']
                    print 'Description: '+jsonstr['Description']
                except urllib2.HTTPError, e:
                    print e.code
                return defect

        def modify_defect(self,defect):
                dic = {"dc:type": {
                            "rdf:resource":self.base_url+"record-type/"+TYPE_ID,
                            "name":"Defect"
                        },
                        "Headline":defect.headline,
                        "Severity":defect.severity,
                        "Priority":defect.priority,
                        "Description":defect.description
                      }
                url=self.base_url+'/record/'+TYPE_ID+'-'+defect.did
                fields=json.dumps(dic)
                headers={'Content-type': 'application/json;charset=utf-8'}
                req = urllib2.Request(url,fields,headers)
                req.get_method = lambda: 'PUT'
                #f=None
                info = None
                try:
                    f=urllib2.urlopen(req)
                    info = f.info()
                    print "Modify defect "+defect.did+" successfully."
                    print 'Headline: '+defect.headline
                    print 'Severity: '+defect.severity
                    print 'Priority: '+defect.priority
                    print 'Description: '+defect.description
                except urllib2.HTTPError, e:
                    print e.code
                return info
