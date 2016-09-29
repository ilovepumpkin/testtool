#!/usr/bin/env python
import urllib
from BeautifulSoup import BeautifulSoup

url='http://9.123.196.12/tr_dir/tr_sh_054/tivoli_storage_ui_ttt.nsf/9448ab41a04adc838525683b0053e574?OpenView&CollapseView'
it='SVC 6.4/Nimitz GUI Sprint 1'

class Data:
    unattempted=0
    blocked=0
    attempted=0
    failed=0
    permfail=0
    success=0
    deferred=0
    total=0
    total_attempts=0
    
    def attempt_rate(self):
        return "{0}%".format(round(float(self.total_attempts)/float(self.total),2)*100)
    
    def success_rate(self):
        return "{0}%".format(round(float(self.success)/float(self.total),2)*100)

class TTT:

    def get(self,url,it):
        f=urllib.urlopen(url)
        s=f.read()
        f.close()

        soup=BeautifulSoup(s)
        html=soup.prettify()

        table=soup.findAll('table')[1]
        b_tags=table.findAll('b')
        for b_tag in b_tags:
            if b_tag.text==it:
                td_tags=b_tag.findParent('tr').findAll('td')
                data=Data()
                data.unattempted=td_tags[1].text
                data.blocked=td_tags[2].text
                data.attempted=td_tags[3].text
                data.failed=td_tags[4].text
                data.permfail=td_tags[5].text
                data.success=td_tags[6].text
                data.deferred=td_tags[7].text
                data.total=td_tags[8].text
                data.total_attempts=td_tags[11].text
                return data


ttt=TTT()
d=ttt.get(url,it)
print "Iteration name:"+it
print "Unattempted:{0}, Blocked:{1}, Attempted:{2}, Failed:{3}, PermFail:{4}, Success:{5}, Deferred:{6}, Total:{7}, Total Attempts:{8}".format(d.unattempted,d.blocked,d.attempted,d.failed,d.permfail,d.success,d.deferred,d.total,d.total_attempts)
print "Attempt%:{0}, Success%:{1}".format(d.attempt_rate(),d.success_rate())
