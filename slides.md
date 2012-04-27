Be More Elite, A How To
=======================

A rapid fire series of lessons you can take home and put into practice.


Learn to RTFM
=============

(Read the fine manual)

    $ man bash
    $ man man
    $ man which
    $ man printf
    $ info emacs

Learn to ask the Almighty Google
================================

    $ chromium-browser "http://www.google.com?q=learn to use the linux"
    $ firefox http://www.google.com?q="ConfigFile.cxx:189:38: error: 'strtol' was not declared in this scope"


Make your environment awesome
=============================

 * bash
 * ssh
 * screen
 * network shenanigans
 * dotfiles
 * versioning configs

Make your bash awesome
======================

Set up bash autocompletion

    # emerge -av bash-completion
    # yum install bash-completion
    # apt-get install bash-completion

Most package managers will set this up for you, but be sure to test it, and
follow any instructions.  Sometimes you have to tell bash to use it explicitly,
like so:

    source /etc/bash_completion

Tweak ~/.bashrc for great justice
=================================

    alias ls='ls --color=auto'     # Pretty colors for ls output
    alias grep='grep --color=auto' # highlights grep output
    alias mp='python manage.py'    # Helpful shorthand for django management
    alias rs='rails server'        # Helpful shorthand for django management
    alias rc='rails console'       # Helpful shorthand for django management
    alias R="R --save"             # Keeps R from prompting when you exit (saves valuable miliseconds)

    # Clever but ghetto ssh-agent environment. Grabs ssh-agent info and sticks it in the current environment
    if [[ -e $HOME/.ssh_agent_info ]]
    then
      source $HOME/.ssh_agent_info
    fi
    alias ghetto-agent="source `which ghetto-agent`"

Make your prompt more useful
============================

There are multiple levels here.  The first is to simply use color codes for readability:

    export PS1="\[\033[01;32m\]\u@\h\[\033[01;34m\] \w \$\[\033[00m\] "

But we can do better. Say you use mercurial or git for version control, and you
want to know your current branch; you can use the PROMPT\_COMMAND to have bash
run a command to generate your prompt.  That command can dynamically set PS1
based on your current context.  Here's how you set that up:

    if [[ -f "$HOME/bin/ps1" ]]
    then
      export PROMPT_COMMAND="source $HOME/bin/ps1"
    fi

This relies on a script at `~/bin/ps1`.  Mine looks like this:

    #!/bin/bash

    HG_BRANCH=`hg branch 2>&1`
    if [[ $? == 0 ]]
    then
      VCS_PROMPT="\[\033[00;33m\](\[\033[00;37m\]$HG_BRANCH\[\033[00;33m\]) \[\033[01;34m\]"
    else
      VCS_PROMPT=""
    fi

    GIT_BRANCH=`git branch 2>&1 | grep \* | cut -d ' ' -f 2`
    if [[ -z "$VCS_PROMPT" && -n "$GIT_BRANCH" ]]
    then
      VCS_PROMPT="\[\033[00;33m\](\[\033[00;37m\]$GIT_BRANCH\[\033[00;33m\]) \[\033[01;34m\]"
    fi

    if [[ -e $VIRTUAL_ENV ]]
    then
      ENVNAME=`echo $VIRTUAL_ENV | cut -d / -f 5`
    VENV_PROMPT="\[\033[00;33m\][\[\033[00;37m\]$ENVNAME\[\033[00;33m\]] "
    else
      VENV_PROMPT=""
    fi

    export PS1="$VENV_PROMPT\[\033[01;32m\]\u@\h\[\033[01;34m\] \w $VCS_PROMPT$ \[\033[00m\]"

This adds a virtualenv indicator for python at the beginning, and a version
control system branch indicator at the end of my prompt.  Here's one with a
`django` virtualenv working on this talk on the branch `default`:

    [django] bensonk@silence ~/Code/lfnw-elite-talk (master) $

Learn how `$PATH` works
=======================

 * Bash looks for programs to execute in the places mentioned in your $PATH variable
 * It looks in order, so if you have two versions of a program, put the "better" one first
 * Be careful, putting . in your path is insecure if you ever visit someone else's directory
 * Experiment!
 * Let me say this again, for emphasis.  Experiment!

SSH Keys
========

SSH is one of the most incredibly versatile tools I've ever seen. You shouldn't
need a password to log into other machines you own.

First, generate a key:

    $ ssh-keygen -t dsa

Then, copy the public part key to another machine you want to log into:

    $ scp .ssh/id_dsa.pub

Tell that machine to allow the private half of that key to let you in

    $ ssh othermachine                        # Log into the other machine
    $ mkdir .ssh                              # Makes sure the dir exists -- if it does, gives you a harmless error.
    $ chmod 700 .ssh                          # Ensure no one else can see or touch what's in here.  Mandatory.
    $ cat id_dsa.pub >> .ssh/authorized_keys  # Sticks your id_dsa.pub on the end of the list of authorized keys, creating it if necessary
    $ chmod 600 .ssh/authorized_keys          # Keeps your keys safe
    $ rm id_dsa.pub

Now, log out of the machine and back in to test it

    $ exit
    $ ssh othermachine
    $ echo rm -rf /          # Don't do this! This is a very bad plan. DO NOT BLINDLY TYPE EVERYTHING YOU READ.
                             # But, just in case someone doesn't know how to READ, I stuck an echo in there, so
                             # it's not so bad. 

SSH Config
==========

 * In your homedir
 * Lots of options
 * Host specific settings are awesome
 * RTFM for WAY more than I can cover

Simple host alias
-----------------

    Host monkey           # Your shortname for the host
    HostName 63.27.43.32  # An IP address I just made up. Insert a real one for best results

Something fancier -- a reverse tunnel
-------------------------------------

From a machine inside a NAT:

    $ ssh -R 2222:localhost:22 internetmachine.yourdomain.com    # Creates a tunnel back to the machine you ssh out from

Now, add a stanza to your ~/.ssh/config on a machine elsewhere on the internet:

    Host hiddenmachine
    ProxyCommand ssh internetmachine.yourdomain.com nc localhost 2222    # pixie magic I'll explain on request

And finally, ssh out from the machine you just did the config on:

    $ ssh hiddenmachine
    $ echo "Hooray! I'm on the hidden machine!"


X11 Forwarding
--------------
This is not always a good idea (an admin on the remote machine can own your
local box), but it's good fun.  If you have an account on another machine, and
a decently fast connection to it, you can run graphical programs on the other
machine, but have the gui show up locally.  

    # Enable on the commandline with -X in .ssh/config like so
    ForwardX11 yes

So, to test it out, ssh to a machine with some sort of X program installed.  My favourite test program is `xeyes`:

    $ ssh othermachine
    $ xeyes

Blink in amazement as the GUI shows up!


Long Running SSH Stuff
======================

Sometimes you want to ssh somewhere, start something up, and then leave it
running, but you need to close the connection.  There are a couple of great
tools for this. 

GNU Screen
----------

GNU Screen has been around for years.  It's the venerable trustworth one, and
it's what I've always used, so I still use it. 

    $ ssh foobar
    $ screen
    $ irssi        # My favourite IRC client
    $ <C-a>d       # This escape sequence will disconnect you from screen
    [detached from 12715.pts-2.foobar]
    $ exit         # Your IRC client is still running, but you're not able to see it

Now, come back in an hour, and check in on irc:

    $ ssh foobar
    $ screen -r

You can create multiple "windows" inside of screen to do multiple things at
once, and switch between them with <C-a>n where n is a number.  It's very cool,
and if you're short on terminals extremely handy. 

TMux
----

 * Lots of fancy features
 * Awesome client-server architecture makes reconnecting less confusing
 * Less arcane configs
 * Probably better to learn this one if you're starting today


Network Stuff
=============

Configuring your network can be extremely powerful, and most of the awesome
stuff you can do is beyond the scope of this talk.  Here are a couple of quick
things you should know how to mess with. 

/etc/hosts
----------

This file is a list of machine aliases.  If you want to override DNS, you stick things in here. 

    127.0.0.1 www.google.com   # This will make www.google.com redirect to localhost. Probably liable to break things.

Let's say you want to blacklist ads from doubleclick:

    10.42.42.42 ad.doubleclick.net   # This tells your computer that ads from doubleclick come from a non-routable IP block.

/etc/resolv.conf
----------------

This file keeps track of all the nameservers your computer knows about.  Often,
your ISP distribute their nameservers via DHCP, which will propagate to your
computer via your rouer.  Your ISP's nameservers are probably extremely slow.
To drastically speed up your networked computing experience, try one of
google's or opendns's servers:

    nameserver 8.8.8.8         # Google 1
    nameserver 8.8.4.4         # Google 2
    nameserver 208.67.222.222  # OpenDNS 1
    nameserver 208.67.220.220  # OpenDNS 2

Keep in mind opendns and google both have business reasons for running these
servers.  They may be mining your datas.  On the other hand, you've gotta
resolve your dns names somehow, and comcast is probably not all that benevolent
either. 


Manage Dotfiles with Git
========================

A lot of the tweaks I've mentioned above are pretty awesome, but if you work on
a lot of machines it can be incredibly hard to keep track of what machines have
the most up to date configs, and distributing new hacks as you set them up.
Git to the rescue!

First, you'll need to move all your version controllable dotfiles to a single
subdirectory of your homedir and then symlink them back out:

    $ mkdir -p configs/dotfiles
    $ mv .bashrc configs/dotfiles/bashrc
    $ mv .vimrc configs/dotfiles/vimrc
    $ ln -s configs/dotfiles/bashrc .bashrc
    $ ln -s configs/dotfiles/vimrc .vimrc

Then, you just need to version control that directory:

    $ cd configs
    $ git init
    $ git add .
    $ git commit -m 'Initial repo creation'  # Now go sign up for a github account and create a repo for your dotfiles
    $ git remote add origin git@github.com:yourname/config.git
    $ git push origin master


And on any new machine you set up:

    $ git clone git@github.com:yourname/config.git
    $ ln -s configs/dotfiles/bashrc .bashrc
    $ ln -s configs/dotfiles/vimrc .vimrc
      ... etc

Note: it's tempting to put .ssh on github, but it's dangerous.  First, free
repos are public, and you definitely don't want to share those private configs
with the world.  Second, sometimes github gets compromised, and you don't want
anyone to be able to read your private keys, ever.  If you DO want to put your
.ssh stuff on github, ONLY do your config and maybe your authorized keys.  


But this is all a pain!
-----------------------

I've written some scripts to make this easier.  Once I get them cleaned up,
I'll publish them at http://github.com/bensonk/dotfiles  In the mean time, you
might have a look at what some other folks have done:
http://dotfiles.github.com/


Git ALL the things!
===================

Git is SO much fun, sometimes you just want to version control the heck out of your system.  I highly recommend using git for all your configs in `/etc`:

    # cd /etc
    # git init
    # git add . "Initial repo creation"

Then, when you (or your package manager) changes anything in /etc do this:

    # cd /etc
    # git add .
    # git commit -m 'Talk about what you changed here'

Now you'll be able to look at logs of what has changed, and roll back configuration changes that break your system.  Please don't put your `/etc` on github, because that would be stupid. 


Develop badass habits
=====================

 * Learn an awesome editor
 * Learn arcane shell shortcuts
 * Automate things
 * If you can't yet, learn to program

Editors
=======

Learn vim, it kicks ass and a variant of it exists on almost all systems ever built.

Consider emacs for heavyweight editing.  

This is not a joke.  Using nano is not elite.  You will save yourself hours, perhaps days by learning a very powerful editor. 

Learn arcane shortcuts
======================

GNU Readline powers bash, and provides emacs style and vim style keybindings.  Though I edit code with vim, I edit commands with emacs keys.  Some examples:

Note: C-x denotes "control+x", M-x denotes "alt+x"

 * `C-a` Takes you to the beginning of the line
 * `C-e` Takes you to the end of the line
 * `C-k` Deletes from here to the end of the line
 * `C-y` Pastes whatever you just deleted
 * `C-h` Backspace (I never use this)
 * `C-b` Takes you back a character
 * `M-b` Takes you back a word
 * `C-f` Takes you forward a character
 * `M-f` takes you forward a word

Just those will save you a lot of time by avoiding moving your hands from home row.  Some bonuses that will make you a ninja:

 * `C-r` Puts you in reverse-search mode, finding the most recent command that matches your search
 * `C-l` Clears the screen, helping you collect your thoughts, or temporarily hide what you've been up to
 * `M-.` Cycles through recent arguments.  Useful for something like this: 

     $ mkdir "Man this is a long directory name, I hope I don't have to type it twice."
     $ cd `M-.`  # Changes to the absurdly named directory above

Another great trick is bash history completion.  To do the same sort of thing
as `M-.` above, you can use `cd  !$`.  Read the second `HISTORY COMPLETION` in
the bash man page for more fun tricks here. 

If you want to kill bash without letting it write a history file, run `kill -9 $$`.  Useful if you're doing things you oughtn't.  

Please note: I admonish you not to do anything you oughtn't.  I especially admonish you not to get _caught_ doing anything you oughtn't.

Learn how your shell works
==========================

This one is hard.  The best thing to do here is take Dr. Philip Nelson's Unix
class at WWU.  He'll have you write a shell, and by the time you're done you'll
understand the basics of how all shells work.  Failing that, do a whole lot of 
experimentation, and try very hard to wrap your head around some basics:

 * Everything is text
 * Substitutions are done in a particular order
 * Everything is in the manual
 * Quotes just surround argument entities on the command line, so `foo` is the same as `"foo"`, but `foo bar` is different from `"foo bar"`
 * Pipes connect program inputs and outputs to each other
 * Backticks are like pipes, but their output produces arguments
 * Redirects are useful, and do the same thing as pipes but to and from files
 * The special "source" builtin command runs a script INSIDE your current shell instance (the only way to alter a running shell's environment)
 * Environment varialbes are (with a few exceptions) just a simple text substitution table

Comands are just programs. Scripts are just programs.  If you're doing a lot of the same thing, stick that series of commands in a file and call it a script. 

Create `~/bin` and put it in your path.  Put useful scripts there. 

The `*` glob just creates a space-separated list of all the files in your current directory.  Experiment with "echo \*" to see what I mean.

The second time you do a thing, automate it
===========================================

 * Shell scripts are easy: just type a bunch of commands into a file. 
 * Python is pretty easy to learn, too.  If you've done any programming, you can probably learn python.
 * Ruby is a little more complex to learn, but is just as cool.  Pick what you like

Bash Scripting
==============

Pipes are your friends
----------------------

    $ ifconfig | grep inet | grep 192                     # Returns any addresses you own on a 192. subnet
    $ egrep ^cat /usr/share/dict/words | egrep -v "'|s$"  # All words in that begin with cat, don't contain an apostrophe, and don't end with s
    $ du -hs * | sort -h | tail -n 10                     # List 10 largest files in the current directory

Let bash run in circles for you
-------------------------------

    $ for fname in *.jpg; do cp $fname ~/archive/photos/; done

Backticks
---------

    $ vim -p `find . -iname '*.py'`  # Edit all python files in this and all subdirs, in tabs. 

Putting it all together
-----------------------

This bash script will find all GIFs in the current directory and
subdirectories, and convert them to PNGs in the png subdir:

    mkdir pngs
    for f in `find . -iname \*.gif`
    do
      echo "Converting $f"
      mkdir -p `basename pngs/$f`
      convert $f pngs/`sed -e s/gif/png/i <<< $f`
    done


Python
======

Python is extremely powerful and can do all sorts of things, but here's a quick
script that logs tweets.  It requires a little bit of setup of the pine siskin
library, but it works great:

    #!/usr/bin/env python
    from streaming_twitter import TwitterClient
    from sys import argv
    
    def logger(tweet):
      f.write(str(tweet))
      f.write("\n")
    
    client = TwitterClient()
    with open(argv[1], 'w') as f:
      client.watch("https://userstream.twitter.com/2/user.json", logger)

To run it:

    $ python twitter_logger.py my_log.txt

Ruby
====

Ruby is also extremely powerful.  There's the famous rails framework, but for
simple tasks sometimes you just want a little web service.  With a few lines of
code, you can spin up a webserver that lets you run commands with a few button
clicks.  Here's a quick and dirty mpd controller webapp:

    require 'sinatra'
    
    def mpc_status
      mpc_output = IO.popen("mpc").readlines.join("<br/>")
      "<html><body><h3>#{mpc_output}</body></html>"
    end
    
    get "/" do
      mpc_status
    end
    
    get '/prev' do
      system "mpc prev"
      mpc_status
    end
    
    get '/next' do
      system "mpc next"
      mpc_status
    end
    
    get '/toggle' do
      system 'mpc toggle'
      mpc_status
    end


Understand your system
======================

 * Explore /proc
   * /proc/version
   * /proc/$$
   * /proc/mounts
   * And everything else!
 * Explore /etc
   * Read all your config files
   * Tweak them!
   * Shut off any services you don't use
   * Find out you actually *do* use that service
   * Turn it back on!
 * Explore your dotfiles extensively: `ls -ald ~/.*`
 * Install and play with `lsof`
 * Play with `ps axf` (read the ps man page for details)
 * Look at `sudo netstat -tpln` output (and look at netstat's man page)

IP, TCP, UDP, NAT, WTF?
=======================

Look these up, and __understand__ them.  Try to understand them as deeply as
possible, and experiment as much as possible.


Discover things using nmap
==========================

Basic network scan:

    $ ifconfig | grep inet  # find your IP, let's say this returned 192.168.1.101
    # nmap 192.168.1.1-254

Read the man page for details, and see what you can find on your network.
Don't go scanning will-nilly, because a lot of sysadmins consider this the
precursor to a full-fledged attack, and will blacklist you.


Probe Layer 2
=============

The network works in layers.  One of the layers most people take for granted is
the data-link layer.  Local attackers can do some nasty things here, so it's
good to understand it.

    # ifconfig | grep inet    # Again, know your IP
    # arping 192.168.1.1      # A common convention is for the router to be .1 on its subnet
    ARPING 10.42.0.1 from 10.42.0.21 eth0
    Unicast reply from 10.42.0.1 [00:18:F8:BD:AD:D3]  0.893ms
    Unicast reply from 10.42.0.1 [00:18:F8:BD:AD:D3]  0.716ms
    Unicast reply from 10.42.0.1 [00:18:F8:BD:AD:D3]  0.732ms
    Unicast reply from 10.42.0.1 [00:18:F8:BD:AD:D3]  0.735ms

The output here is very instructive.  It tells us the router's IP (which we
knew) and the router's MAC address. If that ever changes, somebody's doing some
monkeybusiness trying to convince network users THEY are the router.  This is
called arp poisoning, and it's a great way for a bad actor to redirect
everyone's traffic through their machine.  They will pass it on to the router
after they're done inspecting it. 

We can keep an eye on this with a program called `arpwatch`. 

    # apt-get install arpwatch
    # yum install arpwatch
    # emerge -av arpwatch
    ... whatever. 

Once arpwatch is installed and running, you can keep an eye on root's mail
spool to see if anyone's trying arp poisoning attacks on your network.

Watch traffic
=============

To really understand the network, sometimes you have to look at what's going
on.  The most instructive tool I've found for this is wireshark.  Install it
with your favourite package manager and run it:

    # sudo wireshark

You should then do some general browsing, IMing, and other normal stuff.  Watch
the wireshark window as you do these things -- you might recognize some of the
things going by.  This is what the creepy kid in the corner of starbucks can
see when you browse there.  

For something really instructive, try right clicking on an http session and
clicking "follow tcp stream".  This will let you see a reassembled version of
the whole conversation between hosts, including HTTP headers (cookies!) and the
page content.  By inspecting these headers tools like firesheep can let you
impersonate someone on a network that doesn't use HTTPS. 



Experiment with connectivity
============================

To understand things further, you should learn to talk to networked hosts. The
best tool for this is netcat:

    $ nc localhost 22
    SSH-2.0-OpenSSH_5.8p1 Debian-7ubuntu1

The SSH greeting is great, but unless you can do some pretty impressive mental
math, you won't get much further there.  Try hitting google.com on port 80 and
sending an HTTP header:

    $ nc www.google.com 80
    GET / HTTP/1.0

    ... lots of http traffic comes back ...

Another fun trick is to talk straight to an smtp server, and send some mail.
I leave this as an exercise to the reader. 

More fun with netcat
====================

If you and a friend want to go really old school chat-wise, you can use raw TCP:

    your-machine $ nc -l 2012

    your-friend $ nc your-machine.yourdomain.com 2012

    Hi
    Hello!

Once the connection is establised, you can just _talk_. 

Let's say you wanted to copy a folder as efficiently as possible from the
machine balrog to the machine hunter.  Using scp is easy, but adds a lot of
overhead. Let's do it raw with netcat:

    hunter $ nc -l 4242 | tar jxvf -                  # First set up hunter to listen on port 4242 and unzip whatever comes over the pipe
    balrog $ tar jcvf - some_files | nc hunter 4242   # Then send the files to hunter on port 4242

The important thing here is to be able to establish a TCP connection.  If one machine is behind a firewall and the other isn't, you can reverse the sending and receiving machine, like so:

    balrog $ tar jcvf - some_files | nc -l 4242
    hunter $ nc balrog 4242 | tar jxvf -


Python Webserver
================

Netcat is all well and good, but getting everything set up can be a bit tricky,
especially if you're not in control of both endpoints.  You can use a few lines
of python to spin up a quick webserver:

    #!/usr/bin/env python
    from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
    from SocketServer import TCPServer
    httpd = TCPServer(("", 4200), Handler)
    httpd.serve_forever()

Or, if you find you do this a lot, you can clone sendy, a little wrapper I wrote around this concept:

    $ git clone https://github.com/bensonk/sendy.git
    $ cp sendy/sendy.py ~/bin/sendy                    # Copy it to your bin folder in your homedir
    $ chmod +x !$                                      # Make sure it's executable
    $ cd some/dir/to/send/from                         # Go to the directory you want to be the root
    $ sendy                                            # Sends on port 4200 by default, but configurable


Evil Things
===========

You can do some pretty evil things with a tool called `ettercap`. 

Please don't do these things to anyone's traffic but your own.  Ettercap is a
great instructional tool, but it's also possible to do horrible things with it.
Don't do those things. 

  * ARP poisoning
  * Various MITM attacks
  * Sniffing
  * Blackhole a machine
  * Kill individual connections

Lesson: __NEVER__ trust an open network!

Looking for certain kinds of traffic
====================================

If you'd like to see packets over the network that contain a certain string, ngrep is a great tool:

    $ sudo ngreap GET
    ... all HTTP GET requests show up here ...

Sniffing Passwords
==================

Again.  Don't do this to anyone but yourself or people whose systems you
administer, for teaching purposes only. 

If you're in an evil mood, you can look for anyone sending things over an
insecure channel with a tool called `dsniff`.  

    $ sudo dsniff
    ... Any insecure passwords your computer can see should show up here ...

Supported protocols include 

 * FTP
 * Telnet
 * SMTP
 * HTTP
 * POP
 * poppass
 * NNTP
 * IMAP
 * SNMP
 * LDAP
 * Rlogin
 * RIP
 * OSPF
 * PPTP MS-CHAP
 * NFS
 * VRRP
 * YP/NIS
 * SOCKS
 * X11
 * CVS
 * IRC
 * AIM
 * ICQ
 * Napster
 * PostgreSQL
 * Meeting Maker
 * Citrix ICA
 * Symantec pcAnywhere
 * NAI Sniffer
 * Microsoft SMB
 * Oracle SQL\*Net
 * Sybase and Microsoft SQL

Sniffing Images
===============

If you're interested in seeing all the images that travel over your network,
you can use a tool called driftnet. Driftnet grabs and reassembles all the
image traffic it can find on the network, and either puts them into a capture
directory or into a window.  Run over a wifi network, or with arp poisoning
this will give you a very clear picture of what the network's users are
browsing. 


Note: one evening I was testing this out in the lab, and my friend Phillip
thought it would be funny to run google image searches in windows he then
quickly minimized.  He was able to make images show up on my screen without
having to seem them himself.  Beware of people like Phillip. 

Visualizing Network Traffic
===========================

Sometimes it's nice to get a sense of how many machines your computer is
talking to.  There's an unfortunately named tool called EtherApe that dos a
great job of visualizing this sort of connectivity.  It's a great way to
visualize how much traffic various activities produce. 

Advanced Network Stuff
======================

If you've been bored by all the stuff I just talked about, check out scapy.
It's a fantastic tool which is an internal DSL built on top of python for
crafting packets, sending them, and inspecting what's returend.   Here's
a demo from the scapy tutorial:

    # ./scapy.py -s mysession
    New session [mysession]
    Welcome to Scapy (0.9.17.108beta)
    >>> IP()
    <IP |>
    >>> target="www.target.com"
    >>> target="www.target.com/30"
    >>> ip=IP(dst=target)
    >>> ip
    <IP dst=<Net www.target.com/30> |>
    >>> [p for p in ip]
    [<IP dst=207.171.175.28 |>, <IP dst=207.171.175.29 |>,
     <IP dst=207.171.175.30 |>, <IP dst=207.171.175.31 |>]

On Being A Script Kiddie
========================

I've just shown you a bunch of powerful network manipulation tools.  If all you
do is use them to screw with people, you are a script kiddie.  Don't do that,
you're just embarrassing yourself and making the world a little worse.  Use
these things to learn, to grow, and to make the world a little better. 


So long, and thanks for all the fish
====================================

<3
