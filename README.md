# 1and1IpUpdate
DNS Ip-Updater for 1and1 customers

When run, this script checks the current ip using ipgetter and compares it to the last known IP.
If they are different, it goes through the login procedure and navigates to the DNS Settings page
to automatically change the Ipv4 adress to the new one.

Dependencies:
 - Python 2.7
 - Selenium (pip install selenium)
 - Geckodriver (https://github.com/mozilla/geckodriver/releases)
 - Ipgetter (pip install ipgetter)
 - pyvirtualdisplay (pip install pyvirtualdisplay)
 
User and Password:
For now, User information is stored in a plain text file "user.txt".
The first line should be the Top Domain of your page(e.g. google.com)
The second line should be the password.
   
