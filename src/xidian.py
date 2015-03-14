#! /usr/bin/env python
#coding:utf-8
# @file xidian.py
# @description get the information from job.xididan.edu.cn
# @author doodlesomething
# @version 1.0
# @date 2014-11-17


from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import re,urllib2,sys,os,pdb,smtplib
from email.mime.text import MIMEText
from email.header import Header
reload(sys)
sys.setdefaultencoding('gbk')


##
# @description  get whole page
#
# @param    xdUrl
#
# @return   page_content
def getPageContent(xdUrl):
	req = urllib2.Request(url = xdUrl)
	try:
		response  = urllib2.urlopen(req)
	except urllib2.URLError,e:
		return e
	page_content = response.read()
	return page_content


##
# @descriptio
#
# @param    page_content
#
# @return   
def getJobInfo(page_content):
    page_soup = BeautifulSoup(page_content)
    job_content = page_soup.find("div",{"class":"imiddleb mt5"})
    job_info = job_content.findAll("div",{"id":re.compile('con_two_.')})
    return job_info


##
# @description  
#
# @param    zhao_info
# @param    url_prefix
def get_zhao(zhao_info,url_prefix):
    zhao_dict = {}
    zhao_list = []
    i = 0
    #pdb.set_trace()
    for liTag in zhao_info[:-2]:
        spanTag,aTag = liTag.findAll(['span','a'])
        zhao_dict['time'] = spanTag.string
        zhao_dict['company'] = aTag.string
        zhao_dict['link'] =  url_prefix + aTag['href']




##
# @description  
#
# @param    info
# @param    url_prefix
def get_nanbei(info,url_prefix):
    zhao_dict = {}
    zhao_list = []
    for trTag in info[2:-2]:
        linkTag,placeTag,timeTag = trTag.findAll('td')
        zhao_dict['link'] = url_prefix + linkTag.a['href']
        zhao_dict['company'] = linkTag.a.string
        zhao_dict['where'] = placeTag.string
        zhao_dict['time'] = BeautifulStoneSoup(timeTag.string,convertEntities = BeautifulStoneSoup.HTML_ENTITIES)
        zhao_list.append(zhao_dict)
    return zhao_list





xdUrl = 'http://job.xidian.edu.cn/index.html'
url_prefix = 'http://job.xidian.edu.cn'


# get each item info 
page_content = getPageContent(xdUrl).encode('utf-8')
job_info = getJobInfo(page_content)
zhao_info = job_info[0].findAll('li')
nan_info = job_info[1].findAll('tr')
bei_info = job_info[2].findAll('tr')

get_zhao(zhao_info,url_prefix)

    



"""send the information by email"""

# server and user information




##
# @description  make the message 
#
# @param    doc
#
# @return   msg
def make_msg(doc):
    subject = "spider"
    msg = MIMEText(doc,'html','utf-8')
    msg['Subject'] = subject
    return msg


##
# @description  send email
#
# @param    toddr
# @param    message
#
# @return   boolean
def send_mail(toddr,message):
    global server,username,passwd

    s = smtplib.SMTP(server)
    s.login(username,passwd)
    s.sendmail(fromaddr,toaddr,message)
    s.close()
    return True

if send_mail(toaddr,msg.as_string()):
    print "Got it"




