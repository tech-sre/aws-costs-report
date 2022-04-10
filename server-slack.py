# AWS Cost Report
import os
import subprocess as sp
import urllib3
import json
import datetime
from dateutil.relativedelta import relativedelta
http = urllib3.PoolManager()
end = datetime.date.today().replace(day=1)
riend = datetime.date.today()
start = (datetime.date.today() - relativedelta(months=+12)).replace(day=1)
ristart = (datetime.date.today() - relativedelta(months=+11)).replace(day=1)
sixmonth = (datetime.date.today() - relativedelta(months=+6)).replace(day=1)


cmd = 'aws ce get-cost-and-usage --time-period Start=' + end.isoformat() + ',End=' + riend.isoformat() + ' --granularity=DAILY --metrics UnblendedCost > cost-test.json'
sp.getoutput(cmd)
x = []
testmsg = '*Date*                 ==>   *Cost (in $)*\n'
f = open('cost-test.json')
data = json.load(f)

## For loop for parse
for a in data['ResultsByTime']:
    x.append(float((a['Total']['UnblendedCost']['Amount'])))
    cost = str(round(float(a['Total']['UnblendedCost']['Amount']) * float(1000) / float(1000), 2))
    testmsg+= a['TimePeriod']['Start'] + "    ==>    " + cost + "\n"

testmsg+= '*Toatl*' + "                ==>     *" + str(round(float(sum(x)) * float(1000) / float(1000), 2)) + '*'

#Slack Alert Enable
url="<webhook url>"
msg = {
    "channel": "#phase1",
    "username": "AWS Daily Cost Report",
    "text": testmsg,
    "icon_emoji": "money_with_wings"
    }
encoded_msg = json.dumps(msg).encode('utf-8')
resp = http.request('POST',url, body=encoded_msg)
