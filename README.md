linknlog
========

Description: Passive IRC URL logger for multiple channels, storing to sqlite3.

linknlog is easy to configure, just register a bot name on the IRC server, and rename the config/config_template.txt file to config/config.txt.

This bot is not daemonized, so it's best if you use a multiplexer like tmux or screen. This bot also has no in-channel controls.

04/19/2017 06:30:25 PM

News: I am trying to figure out how to automatically reconnect. I keep getting an error:

<pre>
socket.error: [Errno 54] Connection reset by peer
</pre>

I think I may have a solution by catching the error and retrying.
