#!/bin/sh

ssh mgmt001st002 "get_version | cut -d':' -f2 > /opt/ibm/tomcat/webapps/ROOT/hmi_version.txt"
ssh mgmt001st001 "get_version | cut -d':' -f2 > /opt/ibm/tomcat/webapps/ROOT/hmi_version.txt"
ssh -p1602 9.123.196.232 "get_version | cut -d':' -f2 > /opt/ibm/tomcat/webapps/ROOT/hmi_version.txt"
ssh -p1602 9.123.196.237 "get_version | cut -d':' -f2 > /opt/ibm/tomcat/webapps/ROOT/hmi_version.txt"
