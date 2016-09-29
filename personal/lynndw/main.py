#!/usr/bin/env python
#coding=utf-8
from clearquest import *
username='admin'
password=''
base_url='http://9.186.10.154/cqweb/oslc/repo/cqdb/db/SAMPL'
repository='cqdb'
database='db'

def main(): 
    cq = ClearQuest(base_url,repository,database)
    cq.basic_login(username,password)

    defect = Defect()
    defect.hello='ddd'
    defect.headline = '创建一个新的测试缺陷'
    defect.severity = '2 － 重要'
    defect.priority = '1 － 立即解决'
    defect.description ='样本缺陷描述'
    defect_id = cq.create_defect(defect)

    defect = cq.get_defect(defect_id)

    defect.did = defect_id
    defect.headline = '更新样本缺陷标题'
    defect.severity = '4 － 次要'
    defect.priority = '3 － 正常排队'
    defect.description = '更新样本缺陷描述'
    cq.modify_defect(defect)

if __name__ == "__main__":
    main()


