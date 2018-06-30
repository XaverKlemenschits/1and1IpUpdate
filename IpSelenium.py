#!/usr/bin/python
'''
Script to automatically update Ip if it changes.
'''
import time, shlex, subprocess
from selenium import webdriver
from pyvirtualdisplay import Display


def changeIp(newIp):
    #Website specific info for login
    host = 'https://www.1und1.de:443'
    url = host + '/login'
    loginForm = 'loginform'
    formLogin = 'oaologin.username'
    formPassw = 'oaologin.password'
    formSubmit = 'ct-btn-submitbutton-lead'
    ipInput = 'recordValue'


    # get user information
    lines = open('user.txt', 'r').readlines()
    User = lines[0]
    Pass = lines[1]

    # URL of domain settings page of german 1&1, might be slightly different for others
    dnsUrl = "https://mein.1und1.de/edit-dns-record/" + User + "/872624373?__lf=HomeFlow&linkId=ct.link.dns.editrecord"

    # where to save detailed log
    vlog = 'verblog.txt'
    vstream = open(vlog, 'w')

    # set up browser and load login page
    browser = webdriver.Firefox()
    browser.get(url)

    #Fill in user name
    time.sleep(5)
    UserName = browser.find_element_by_name(formLogin)
    UserName.send_keys(User)
    vstream.write(time.strftime("%d/%m/%Y-%H:%M") + "\nFilled in Username\n")

    #Fill in password
    Password = browser.find_element_by_name(formPassw)
    Password.send_keys(Pass)
    vstream.write("Filled in password\n")

    #Submit login
    browser.find_element_by_id(formSubmit).click()
    vstream.write("Submitted password\n")

    #navigate to DNS page
    time.sleep(5)
    browser.get(dnsUrl)
    vstream.write("Entered Domain Page\n")

    #put in the new ip
    time.sleep(10)
    ipv4Input = browser.find_element_by_id(ipInput)
    ipv4Input.clear()
    ipv4Input.send_keys(newIp)
    vstream.write("Filled in new IP\n")

    #save changes
    browser.find_element_by_xpath(".//button[contains(.,'Speichern')]").click()

    #wait for server response and quit
    time.sleep(5)
    browser.quit()
    vstream.write("Quit browser\n")
    vstream.close()


def appendLog(filename, string, maxlines=20):
    ''' Appends one line to log and keeps lines in file to maxlines'''
    try:
        lines = open(filename, 'r').readlines()
    except:
        lines = []
    lines.append(string)
    logFile = open(filename, 'w')
    for line in lines[-maxlines:]:
        logFile.write(line)
    logFile.close()


#check for Ip
ipFile = 'WanIp.txt'
logFile = 'log.txt'
mailFile = 'mail_user.txt'

try:
    fstream = open(ipFile, 'r')
    currentIp = fstream.read().strip()
    fstream.close()
except:
    currentIp = "";

# find new ip by resolving dns
cmd='dig @resolver2.opendns.com myip.opendns.com -4 +short'
proc=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE)
out,err=proc.communicate()
newIp = out.decode("utf-8").strip()

appendLog(logFile, time.strftime("%d/%m/%Y-%H:%M") + ": Checked IP(" + currentIp + ")\n")

if(currentIp != newIp):

    #write log
    appendLog(logFile, time.strftime("%d/%m/%Y-%H:%M") + '  changing Ip to ' + newIp + '\n')
    #change ip at 1und1.de

    #start display and change ip
    with Display(visible=0, size=(800,600)) as display:
        changeIp(newIp)

    appendLog(logFile, time.strftime("%d/%m/%Y-%H:%M") + '  changed Ip to ' + newIp + '\n')

    #change saved ip
    fstream = open(ipFile, 'w')
    fstream.write(newIp)
    fstream.close()


    #send email confirming that ip was changed
    from smtplib import SMTP_SSL as SMTP

    lines = [i.strip() for i in open(mailFile, 'r').readlines()]
    sender = lines[0]
    receivers = [lines[0]]

    message = """From: """ + lines[2] + """ <""" + lines[3] + """>
To: """ + lines[4] + """ <""" + lines[5] + """>
Subject: IP change detected

The old ip """ + currentIp + """ was changed to """ + newIp + """."""

    smtpObj = SMTP('smtp.1und1.de', 465)
    smtpObj.set_debuglevel(0)
    smtpObj.login(sender, lines[1])
    smtpObj.sendmail(sender, receivers, message)
    smtpObj.quit()
