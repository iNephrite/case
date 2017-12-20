#coding=utf8
from apscheduler.schedulers.blocking import BlockingScheduler
from lxml import etree
import requests
import json
import os
import logging
logging.basicConfig()
rs = requests.Session()
proxies = {'http':'socks5://0.0.0.0:6000', 'https':'socks5://0.0.0.0:6000'}
# 输出时间
def Lab_job():
    yy_Lab("480","660")
    yy_Lab("1110","1290")

def get_headers_cookie():
    nocode = rs.get(os.environ.get("Lab_Url"),proxies=proxies)  
    headers = {'Content-Type': 'application/json'}
    return headers

def get_ruleid(headers):
    url = 'http://10.23.4.31/laa/discuss/userAppoint/default'

    r = rs.get(url, headers=headers,proxies=proxies)

    selector = etree.HTML(r.text)
   
    ruleid = selector.xpath('//*[@id="timeSelect"]/option[3]')[0].attrib['value']
    return ruleid

def post_form(ruleid,headers,stime,etime):
    form = {
		"_subject": "学习",
		"_stime": stime,  # 480 1110
		"_etime": etime,  # 660 1290
		"_roomid": "1285b3ca77594b3095c7b89d4922553c",
		"UUID": "VEmkgCYM",
		"ruleId": ruleid,
		"_summary": "学习",
		"users": "14401010232 17408070219",
		"usercount": 3,
		"_seatno": ""
	}

    posturl = 'http://10.23.4.31/laa/form/dynamic/saveForm'

    getstatus = rs.post(posturl, data=json.dumps(form), headers=headers,proxies=proxies)

    return (json.loads(getstatus.content)['status'])


def yy_Lab(stime_str,etime_str):
	headers = get_headers_cookie()
	ruleid = get_ruleid(headers)
	status = post_form(ruleid,headers,stime_str,etime_str)
	# if status != true send email
	print(status)

def test():
    Lab_job()
    pass
# BlockingScheduler
test()
scheduler = BlockingScheduler()
scheduler.add_job(Lab_job, 'cron', hour=0, minute=0, second=1)
scheduler.start()
