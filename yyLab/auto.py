#coding=utf8
from apscheduler.schedulers.blocking import BlockingScheduler
from lxml import etree
import requests
import json
import os
import logging
logging.basicConfig()

# 输出时间
def Lab_job():
    yy_Lab("480","660")
    yy_Lab("660","1290")

def get_headers_cookie():
    nocode = requests.get(os.environ.get("Lab_Url"))
    jsessionid = nocode.url[55:87]

    headers = {"Cookie": "JSESSIONID=" + jsessionid + "; JSESSIONID_NS_Sig=Auskw42vcZYUHmaH",
			   'Content-Type': 'application/json'}
    return headers

def get_ruleid(headers):
    url = 'http://yy.nbut.edu.cn/laa/discuss/userAppoint/default'

    r = requests.get(url, headers=headers)

    selector = etree.HTML(r.text)

    ruleid = selector.xpath('//*[@id="timeSelect"]/option[3]')[0].attrib['value']
    return ruleid

def post_form(ruleid,headers,stime,etime):
    form = {
		"_subject": "学习",
		"_stime": stime,  # 480 1110
		"_etime": etime,  # 660 1290
		"_roomid": "81bc4a16d0884be7a3ded10f8a5f2a6b",
		"UUID": "VEmkgCYM",
		"ruleId": ruleid,
		"_summary": "学习",
		"users": "14401010232 17408070219",
		"usercount": 3,
		"_seatno": ""
	}

    posturl = 'http://yy.nbut.edu.cn/laa/form/dynamic/saveForm'

    getstatus = requests.post(posturl, data=json.dumps(form), headers=headers)

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
