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

    $ chromium-browser http://lmgtfy.com/?q=learn%2520to%2520use%2520the%2520linux
    $ firefox http://lmgtfy.com/?q=ConfigFile.cxx%3A189%3A38%3A+error%3A+%27strtol%27+was+not+declared+in+this+scope

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

And something like this in `~/.bashrc`

    source /etc/bash_completion

Tweak `~/.bashrc` for great justice
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

First, some color

    export PS1="\[\033[01;32m\]\u@\h\[\033[01;34m\] \w \$\[\033[00m\] "

But we can do better:

    if [[ -f "$HOME/bin/ps1" ]]
    then
      export PROMPT_COMMAND="source $HOME/bin/ps1"
    fi

Which relies on a script at `~/bin/ps1`:

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

Which adds a context sensitive indicator for `virtualenv_wrapper` and `git` or `hg` current branch:

    [django] bensonk@silence ~/Code/lfnw-elite-talk (master) $

Learn how `$PATH` works
=======================

 * Bash looks for programs in dirs mentioned in $PATH
 * Executes first match, in left-to-right order
 * __Don't__ put `.` in $PATH
 * Experiment!
 * Again for emphasis:  Experiment!

SSH without passwords
=====================

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

`.ssh/config` simple host alias
-----------------

    Host monkey           # Your shortname for the host
    HostName 63.27.43.32  # An IP address I just made up. Insert a real one for best results

SSH: A reverse tunnel
=====================

From a machine inside a NAT:

    $ ssh -R 2222:localhost:22 internetmachine.yourdomain.com    # Creates a tunnel back to the machine you ssh out from

Now, add a stanza to your ~/.ssh/config on a machine elsewhere on the internet:

    Host hiddenmachine
    ProxyCommand ssh internetmachine.yourdomain.com nc localhost 2222    # pixie magic I'll explain on request

And finally, ssh out from the machine you just did the config on:

    $ ssh hiddenmachine
    $ echo "Hooray! I'm on the hidden machine!"

SSH X11 Forwarding
==================

Run GUI programs remotely

    $ ssh -X othermachine
    $ xeyes

Blink in amazement as the GUI shows up!

Long Running Commands via SSH 
=============================

Log out and keep things running

GNU Screen
----------

It's been around for years, and is pretty great. 

    $ ssh foobar
    $ screen
    $ irssi        # My favourite IRC client
    $ <C-a>d       # This escape sequence will disconnect you from screen
    [detached from 12715.pts-2.foobar]
    $ exit         # Your IRC client is still running, but you're not able to see it

Now, come back in an hour, and check in on irc:

    $ ssh foobar
    $ screen -r

Create another "window":
    
    $ <C-a>c
    $ 

tmux
----

 * Everything Screen does
 * Plus lots of new features
 * Less arcane interface
 * Less arcane configs
 * Probably better to learn if you're starting fresh

Network Stuff
=============

/etc/hosts
----------

A list of aliases; supersedes DNS. 

    127.0.0.1 www.google.com   # This will make www.google.com redirect to localhost. Probably liable to break things.

Blacklist doubleclick adserver:

    10.42.42.42 ad.doubleclick.net   # This tells your computer that ads from doubleclick come from a non-routable IP block.

Name your home server:

    192.168.1.42  bistromath

/etc/resolv.conf
----------------

DNS servers

    nameserver 8.8.8.8         # Google 1
    nameserver 8.8.4.4         # Google 2
    nameserver 208.67.222.222  # OpenDNS 1
    nameserver 208.67.220.220  # OpenDNS 2

Manage Dotfiles with Git
========================

Collect version controllable files in a single subdirectory

    $ mkdir -p configs/dotfiles
    $ mv .bashrc configs/dotfiles/bashrc
    $ mv .vimrc configs/dotfiles/vimrc

And symlink them back out

    $ ln -s configs/dotfiles/bashrc .bashrc
    $ ln -s configs/dotfiles/vimrc .vimrc

Version control that:

    $ cd configs
    $ git init
    $ git add .
    $ git commit -m 'Initial repo creation'  # Now go sign up for a github account and create a repo for your dotfiles
    $ git remote add origin git@github.com:yourname/config.git
    $ git push origin master

On any new machine:

    $ git clone git@github.com:yourname/config.git
    $ ln -s configs/dotfiles/bashrc .bashrc
    $ ln -s configs/dotfiles/vimrc .vimrc
      ... etc

Note: it's tempting to put `~/.ssh` on github, but it's dangerous.

But this is all a pain!
-----------------------

Scripts make this easier, see http://dotfiles.github.com/


Git ALL the things!
===================

git for `/etc`:

    # cd /etc
    # git init
    # git add . "Initial repo creation"

When anything changes in `/etc`:

    # cd /etc
    # git add .
    # git commit -m 'Talk about what you changed here'

All the fun of git in `/etc`.

_Please don't put your `/etc` on github, because that would be stupid._

Develop badass habits
=====================

 * Learn an awesome editor
 * Learn arcane shell shortcuts
 * Automate things
 * If you can't yet, learn to program

Editors
=======

Learn vim.

Or maybe emacs. 

For f\*\*\*'s sake, don't use nano. _It is not elite._

Learn arcane bash shortcuts
======================

_Note: C-x denotes "control+x", M-x denotes "alt+x"_

Moving about:

 * `C-a` Takes you to the beginning of the line
 * `C-e` Takes you to the end of the line
 * `C-k` Deletes from here to the end of the line
 * `C-y` Pastes whatever you just deleted
 * `C-h` Backspace (I never use this)
 * `C-b` Takes you back a character
 * `M-b` Takes you back a word
 * `C-f` Takes you forward a character
 * `M-f` takes you forward a word

Bonus awesomeness:

 * `C-r` Puts you in reverse-search mode, finding the most recent command that matches your search
 * `C-l` Clears the screen, helping you collect your thoughts, or temporarily hide what you've been up to
 * `M-.` Cycles through recent arguments.  Useful for something like this: 

     $ mkdir "Man this is a long directory name, I hope I don't have to type it twice."
     $ cd `M-.`  # Changes to the absurdly named directory above

Use bash `HISTORY EXPANSION` (see man page for more):

    $ mkdir foo
    $ rmdir !$          # Same as rmdir <M-.>
    $ mv foo someplace
    $ ^foo^bar^         # mv bar someplace

To avoid saving a bash\_history file, run `kill -9 $$`.

Learn how your shell works
==========================

Take Dr. Philip Nelson's Unix class at WWU, and write your own shell.

Failing that, experiment, and learn some basics:

 * Everything is text
 * Substitutions are done in a particular order
 * Everything is in the manual
 * Quotes just surround argument entities on the command line, so `foo` is the same as `"foo"`, but `foo bar` is different from `"foo bar"`
 * Pipes connect program inputs and outputs to each other
 * Backticks are like pipes, but their output produces arguments
 * Redirects are useful, and do the same thing as pipes but to and from files
 * The special `source` builtin executes scripts INSIDE your current shell
 * Most environment variables are a simple text substitution table

Comands are just programs. Scripts are just programs.  Write scripts and use them as commands:

    $ mkdir ~/bin
    $ echo 'export PATH="$HOME/bin:$PATH"' >>~/.bashrc
    $ vim ~/bin/fun_command
    $ chmod +x !$

The `*` glob creates a space-separated list of matching files.

    $ ls
    Code         Desktop      Downloads    ISOs         Movies       Packages     Public       dart         dotfiles     old-vimrc
    Data         Documents    Dropbox      Library      Music        Pictures     bin          doc          node_modules test.py
    $ echo *
    Code Data Desktop Documents Downloads Dropbox ISOs Library Movies Music Packages Pictures Public bin dart doc dotfiles node_modules old-vimrc test.py

The second time you do a thing, automate it
===========================================

 * Shell scripts are easy.
 * Python is pretty easy, too.
 * Ruby is _also_ easy.
 * Pick one and get really, really good.

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

Python is powerful; here's a quick script that logs tweets.

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

I wrote this browser based MPD control app in a few minutes:

    require 'sinatra'

    get "/" do
      mpc_output = IO.popen("mpc").readlines.join("<br/>")
      "<html><body>" +
      "  <h3>#{mpc_output}</h3>" +
      '  <p><a href="prev">prev</a> <a href="/toggle">play/pause</a> <a href="/next">next</a></p>' +
      "</body></html>"
    end

    get '/prev' do
      system "mpc prev"
      redirect "/"
    end

    get '/next' do
      system "mpc next"
      redirect "/"
    end

    get '/toggle' do
      system 'mpc toggle'
      redirect "/"
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
 * Explore /dev
   * /dev/disk/by-\*
   * /dev/input/by-\*
 * Explore your dotfiles extensively: `ls -ald ~/.*`
 * Explore your kernel logs with `dmesg` (or `watch bash -c 'dmesg | tail -n 30'`)
 * Install and play with `lsof`
 * Play with `ps axf` (read the ps man page for details)
 * Look at `sudo netstat -tpln` output (and look at netstat's man page)

IP, TCP, UDP, NAT, WTF?
=======================

Look these up, and __understand__ them.  Experiment!

Discover things using nmap
==========================

Basic network scan:

    $ ifconfig | grep inet  # find your IP, let's say this returned 192.168.1.101
    # nmap 192.168.1.1-254  # Read this output and understand _everything_.

Find machines with an SSH server:

    # nmap -p 22 192.168.1.0/24

Probe Layer 2
=============

Most people take layer 2 for granted. _Don't._

    # ifconfig | grep inet    # Again, know your IP
    # arping 192.168.1.1      # A common convention is for the router to be .1 on its subnet
    ARPING 10.42.0.1 from 10.42.0.21 eth0
    Unicast reply from 10.42.0.1 [00:18:F8:BD:AD:D3]  0.893ms
    Unicast reply from 10.42.0.1 [00:18:F8:BD:AD:D3]  0.716ms
    Unicast reply from 10.42.0.1 [00:18:F8:BD:AD:D3]  0.732ms
    Unicast reply from 10.42.0.1 [00:18:F8:BD:AD:D3]  0.735ms

 * router's IP
 * router's MAC address

If this relationship changes, __shenanigans__ are afoot.

Keep an eye on this with a program called `arpwatch`. 

    # apt-get install arpwatch
    # yum install arpwatch
    # emerge -av arpwatch
    ... whatever. 

Watch traffic
=============

    # sudo wireshark

 * See traffic go by
 * Filter based on complex queries
 * Follow individual conversations
 * Read unencrypted traffic

[WireShark](http://screenshots.en.sftcdn.net/en/scrn/34000/34498/wireshark-24.jpg)

Experiment with connectivity
============================

Speak TCP with netcat

    $ nc localhost 22
    SSH-2.0-OpenSSH_5.8p1 Debian-7ubuntu1

SSH greeting is great, but I can't speak it. Try google.com:80 with a GET:

    $ nc www.google.com 80
    GET / HTTP/1.0

    ... lots of web page shows up ...

Another fun trick is smtp.  I leave this as an exercise.

More fun with netcat
====================

Chat
----

    your-machine $ nc -l 2012

    your-friend $ nc your-machine.yourdomain.com 2012

    Hi
    Hello!

Once the connection is establised, you just _talk_. 

File Transfers
--------------

Let's copy a folder.  It's easy with `scp`, but that adds overhead.

    hunter $ nc -l 4242 | tar jxvf -                  # First set up hunter to listen on port 4242 and unzip whatever comes over the pipe
    balrog $ tar jcvf - some_files | nc hunter 4242   # Then send the files to hunter on port 4242

If one machine is behind a firewall, you can reverse the sending and receiving machine:

    balrog $ tar jcvf - some_files | nc -l 4242
    hunter $ nc balrog 4242 | tar jxvf -


Python Webserver
================

You can use a few lines of python to spin up a quick webserver:

    #!/usr/bin/env python
    from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
    from SocketServer import TCPServer
    httpd = TCPServer(("", 4200), Handler)
    httpd.serve_forever()

To make it easier, you can clone `sendy`, which wraps this in a command.

    $ git clone https://github.com/bensonk/sendy.git
    $ cp sendy/sendy.py ~/bin/sendy                    # Copy it to your bin folder in your homedir
    $ chmod +x !$                                      # Make sure it's executable

Once it's installed:

    $ cd some/dir/to/send/from                         # Go to the directory you want to be the root
    $ sendy                                            # Sends on port 4200 by default, but configurable

Evil Things
===========

You can do some pretty evil things with a tool called `ettercap`. 

_Don't do those things to other people._

 * ARP poisoning
 * Various MITM attacks
 * Sniff __all__ the things
 * Null route a MAC
 * Kill individual connections via FIN injection

Lesson: __NEVER__ trust an open network!

Looking for certain traffic
====================================

If you'd like to see packets over the network that contain a certain string, ngrep is a great tool:

    $ sudo ngreap GET
    ... all HTTP GET requests show up here ...

Sniffing Passwords
==================

_Again.  Don't do this to anyone but yourself._

Look for things sent in the clear `dsniff`.  

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

Use `driftnet` to show all the images drifting past. 

[driftnet](http://www.ex-parrot.com/~chris/driftnet/screenshot.jpg)

_Beware of Phillip._

Visualizing Network Traffic
===========================

Have a look at traffic volumes and connectedness with `EtherApe`

[EtherApe](http://etherape.sourceforge.net/images/v0.9.3.png)

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

[Scapy](http://jamesdotcom.com/wp-content/uploads/2010/03/2-300x247.jpg)

On Being A Script Kiddie
========================

If all you do is use tools to screw with people, you are a script kiddie.  Don't do that.
Use these things to learn, to grow, and to make the world a little better. 

So long, and thanks for all the fish
====================================

<3
