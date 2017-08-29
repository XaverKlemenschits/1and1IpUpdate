#!/usr/bin/python
'''
Script to automatically update Ip if it changes.
'''
import time, sys, os
import ipgetter
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

    IpForm = 'is-ipv4'

    # get user information
    lines = open('user.txt', 'r').readlines()
    User = lines[0]
    Pass = lines[1]

    # URL of domain settings page of german 1&1, might be slightly different for others
    domainUrl = "https://mein.1und1.de/domain-dns-settings/" + User + "?__lf=HomeFlow&linkId=ct.txt.domainlist.advancedsettings.pro&from=domain-details%2F" + User


    vlog = 'verblog.txt'
    vstream = open(vlog, 'w')

    browser = webdriver.Firefox()
    browser.get(url)
    
    #Fill in user name
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


    #got to DNS page after waiting for server to process login    
    #time.sleep(5)
    #browser.get(domainUrl)
    #vstream.write("Entered Domain Page\n")

    #navigate to DNS page
    time.sleep(5)
    browser.get(domainUrl)
    vstream.write("Entered Domain Page\n")

    #put in the new ip
    time.sleep(10)
    ipv4Input = browser.find_element_by_name('ipv4')
    ipv4Input.clear()
    ipv4Input.send_keys(newIp)
    vstream.write("Filled in new IP\n")

    #save changes
    browser.find_element_by_xpath(".//button[contains(.,'Speichern')]").click()
    time.sleep(2)
    browser.find_element_by_xpath(".//button[contains(.,'Ja')]").click()
    vstream.write("Clicked save\n")
    
    #wait for server response and quit
    time.sleep(5)
    browser.quit()
    vstream.write("Quit browser\n")
    vstream.close()

def appendLog(filename, string, maxlines=20):
    ''' Appends one line to log and keeps lines in file to maxlines'''
    lines = open(filename, 'r').readlines()
    lines.append(string)
    logFile = open(filename, 'w')
    for line in lines[-maxlines:]:
        logFile.write(line)
    logFile.close()
    

#start display
display = Display(visible=0, size=(800, 600))
display.start()

#check for Ip
ipFile = 'WanIp.txt'
logFile = 'log.txt'
fstream = open(ipFile, 'r')
currentIp = fstream.read().strip()
fstream.close()
#print(currentIp)

newIp = ipgetter.myip().strip()
#print(newIp)

appendLog(logFile, time.strftime("%d/%m/%Y-%H:%M") + ": Checked IP(" + currentIp + ")\n")

#print(currentIp)
#print(newIp)

if(currentIp != newIp):
    #startxvfb
    #os.system('Xvfb :99')
    #os.system('export DISPLAY=:99')

    #write log
    #logFile = open('log.txt', 'a')
    appendLog(logFile, time.strftime("%d/%m/%Y-%H:%M") + '  changing Ip to ' + newIp + '\n')
    #print("Wrote log")
    #change ip at 1und1.de
    changeIp(newIp)
    
    appendLog(logFile, time.strftime("%d/%m/%Y-%H:%M") + '  changed Ip to ' + newIp + '\n')
    
    #change saved ip
    fstream = open(ipFile, 'w')
    fstream.write(newIp)
    fstream.close()
#else:
#    print('No changes')

