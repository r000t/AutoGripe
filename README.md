AutoGripe
=========

fail2ban action script that uses SMTP or Gmail to send abuse complaints. It was inspired by ```sendmail-complain``` and uses the abusix Abuse Contact Database to obtain abuse email addresses. It was designed for those who don't want to set up an entire mail server just to send abuse reports; Reports sent through sendmail by itself will probably get caught up in spam filters. AutoGripe lets you use an already-existing email account through SMTP.

Requirements
------------

AutoGripe uses Python, and requires the ipaddr and dns modules. 

On a Debian/Ubuntu system, these would be the **python-dnspython** and **python-ipaddr** packages.

AutoGripe is an action script for **fail2ban**, so you should install that if you haven't already.

Known Issues
------------

The single biggest drawback to using an abuse emailer will be bouncebacks, **especially** from China. You'll get nonexistant inboxes, and the ones that do exist are almost always full. You should expect a **lot** of bounced emails. If you feel like doing something about it, it's always possible to report the non-working abuse address to the RIR (APNIC in China's case). A future version of AutoGripe will have an option to not even bother with such ISPs.

A similar issue you may face is that while the Abuse Contact DB is pretty complete, it's not infallible. Some emails will go to the "wrong" address when more than one is listed for abuse. I've been slowly reporting these to Abusix.

Instructions for Use
--------------------

1. Create a folder only readable by root
2. Put querycontacts.py and autogripe.py in that folder
3. Edit the top of autogripe.py with your SMTP server, port, and credentials
4. Put autogripe.conf in /etc/fail2ban/action.d/ and edit it, changing /path/to/autogripe.py to the actual path
5. Add the ```autogripe``` action to the SSH jail in /etc/fail2ban/jail.conf (Instructions below.)

AutoGripe was designed around SSH, but it should work with any sort of jail. All you need to do is change logpath in the jail to a log that contains the IP address and relevant information about the attack.

Configuring the Jail
-------------------

This example for SSH on Debian/Ubuntu

The JAILS section of /etc/fail2ban/jail.conf contains various instructions for fail2ban to recognize and react to a brute force attempt. SSH should be the first "jail", but if it isn't, no big deal. 

The action variable in the jail tells fail2ban what action script to execute. You can specify more than one. Just add the second (or subsequent) action under the first one. For example:

<pre>action   = iptables-multiport
           autogripe[logpath=/var/log/auth.log]</pre>

You will also need to add the path to the log file, as shown above. Just a reminder, AutoGripe only reports abuse. You'll still need to use, for example, `iptables-multiport` to actually enforce a ban. If you don't, the attack will continue past the threshold, and you'll only end up spamming the abuse inbox. Not good.

Save the file, and then restart fail2ban:

```service fail2ban restart```

And you're done!

