AutoGripe
=========

fail2ban action script that uses SMTP or Gmail to send abuse complaints

Requirements
------------

AutoGripe uses Python, and requires the ipaddr and dns modules. 

On a Debian/Ubuntu system, these would be the **python-dnspython** and **python-ipaddr** packages.

AutoGripe is an action script for **fail2ban**, so you should install that if you haven't already.

Instructions for Use
--------------------

1. Create a folder only readable by root
2. Put querycontacts.py and autogripe.py in that folder
3. Edit the top of autogripe.py with your SMTP server, port, and credentials
4. Put autogripe.conf in /etc/fail2ban/action.d and edit it, changing /path/to/autogripe.py to the actual path
5. Add the ```autogripe``` action to the SSH jail in /etc/fail2ban/jail.conf (Instructions below.)

AutoGripe was designed around SSH, but it should work with any sort of jail. All you need to do is change logpath in the jail to a log that contains the IP address and relevant information about the attack.

Configuring the Jail
-------------------

This example for SSH on Debian/Ubuntu

The JAILS section of /etc/fail2ban/jail.conf contains various instructions for fail2ban to recognize and react to a brute force attempt. SSH should be the first "jail", but if it isn't, no big deal. 

The action variable in the jail tells fail2ban what action script to execute. You can specify more than one. Just add the second (or subsequent) action under the first one. For example:

<pre>action   = iptables-multiport
           autogripe[logpath=/var/log/auth.log]</pre>

You will also need to add the path to the log file, as shown above.

Save the file, and then restart fail2ban:

```service fail2ban restart```

And you're done!

