# 1and1IpUpdate
DNS Ip-Updater for 1and1 customers

When run, this script checks the current ip using OpenDNS and compares it to the last known IP.
If they are different, it goes through the login procedure and navigates to the DNS Settings page
to automatically change the Ipv4 address to the new one. Then a confirmation email is sent to the
specified address using a 1and1 email address.

Dependencies:
 - Python 2.7
 - Selenium (pip install selenium)
 - Geckodriver (https://github.com/mozilla/geckodriver/releases)
 - pyvirtualdisplay (pip install pyvirtualdisplay)

User and Password:
For now, User information is stored in a plain text file "user.txt".
The first line should be the Top Domain of your page(e.g. google.com)
The second line should be the password.

Email User and Password:
"mail_user.txt" stores information line by line:
<sender email address>
<sender email password>
<sender name>
<sender email shown to receiver>
<receiver name>
<receiver email address>
