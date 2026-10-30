# Copyright (c) 2026 Vibe-Bots
# Open-sourced under MIT terms.
# Included within AnonMusic framework.


HELP_1 = """<b><u>Here is the help for admin module :</u></b>

<b><u>Admin commands :</u></b>

<b>Just add <code>c</code> in the starting of the commands to use them for channels.</b>

<b>๏ /pause -</b> pause the current playing stream
<b>๏ /resume -</b> resume the paused stream
<b>๏ /skip -</b> skip the current playing stream and start the next track in queue
<b>๏ /end or /stop -</b> clears the queue and end the current playing stream
<b>๏ /queue -</b> shows the queued tracks list
<b>๏ /loop [disable/enable] or [between 1:10] -</b> when activated bot will play the current stream in loop for 10 times or the number of requested loops
<b>๏ /shuffle -</b> shuffle the queued tracks
<b>๏ /seek -</b> seek the stream to the given duration
<b>๏ /seekback -</b> backward seek the stream to the given duration
"""

HELP_2 = """<b><u>Here is the help for auth module :</u></b>

<b><u>Auth users :</u></b>

<b>Auth users can use admin rights in the bot without admin rights in the chat. [admins only]</b>

<b>๏ /auth [username] -</b> add a user to auth list of the bot.

<b>๏ /unauth [username] -</b> remove a auth user from the auth users list.

<b>๏ /authusers -</b> shows the auth users list of the group.
"""

HELP_3 = """<b><u>Here is the help for blacklist module :</u></b>

<b><u>Blacklist chat :</u></b>

<b>๏ /blacklistchat [chat id] -</b> blacklist a chat from using the bot.

<b>๏ /whitelistchat [chat id] -</b> whitelist the blacklisted chat.

<b>๏ /blacklistedchat -</b> shows the list of blacklisted chats.

<b><u>Block users:</u></b>

<b>๏ /block [username or reply to a user] -</b> starts ignoring the user, so that he can't use bot commands.

<b>๏ /unblock [username or reply to a user] -</b> unblocks the blocked user.

<b>๏ /blockedusers -</b> shows the list of blocked users.
"""

HELP_4 = """<b><u>Here is the help for broadcast module :</b></u>

<b><u>Broadcast feature [only for sudoers] :</b></u>

<b>๏ /broadcast [message or reply to a message] -</b> send a broadcast message to all served chats of the bot.

<b><u>Broadcasting modes:</b></u>
๏ <code>-pin</code> : pins your broadcasted messages in served chats.
๏ <code>-pinloud</code> : pins your broadcasted message in served chats and sends notification to the members.
๏ <code>-user</code> : broadcasts the message to the users who have started your bot.
๏ <code>-nobot</code> : forces the bot to not broadcast the message.

<pre language='python'>๏ example : /broadcast -user -pin testing broadcast</pre>

"""

HELP_5 = """<b><u>Here is the help for ping module :</b></u>

<b><u>Ping command :</b></u>

<b>๏ /ping -</b> show the ping and system stats of the bot.
<b>๏ /stats -</b> get top 10 track global stats, top 10 users of the bot, top 10 chats on the bot, top 10 played in the chat and many more...
"""

HELP_6 = """<b><u>Here is the help for play module :</b></u>

<b><u>Play commands:</b></u>

<b>๏ c</b> stands for channel play.
<b>๏ v</b> stands for video play.
<b>๏ force</b> stands for force play.

<b>๏ /play or /vplay or /cplay -</b> starts streaming the requested track on videochat.
<b>๏ /playforce or /vplayforce or /cplayforce -</b> force play stops the ongoing stream and starts streaming the requested track.
<b>๏ /channelplay [chat username or id] or [disable] -</b> connect channel to a group and starts streaming tracks by the help of commands sent in group.
"""

HELP_7 = """<b><u>Here is the help for sudo module :</b></u>

<b>Storage cleaner :</b>
๏ <b>/clean</b> – view storage usage & cleanable folders
๏ click buttons to clean specific folders :
├ downloads
├ cache
└ temp
๏ <b>clean all</b> – cleans everything in one go
๏ folder structure, size & file count included
๏ full disk stats also shown

<b>File manager — paid :</b>
<b>๏ soon</b> – it will be public in the next update

<b>These tools are of no use :</b>
<b>๏ /logs -</b> get logs of the bot
<b>๏ /logger [enable/disable] -</b> bot will start logging the activities happen on bot
<b>๏ /maintenance [enable/disable] -</b> enable or disable the maintenance mode of your bot

<b>Manage your sudo list :</b>
<b>๏ /sudo -</b> add a sudo user
<b>๏ /rmsudo -</b> remove sudo user
<b>๏ /sudolist -</b> check sudolist
"""

HELP_8 = """<b><u>Here is the help for active videochats module :</b></u>

<b><u>Active videochats :</b></u>

<b>๏ /activevoice -</b> shows the list of active voicechats on the bot.
<b>๏ /activevideo -</b> shows the list of active videochats on bot.
<b>๏ /autoend [enable|disable] -</b> enable stream auto end if no one is listening.
"""

HELP_9 = """<b><u>Here is the help for start module :</b></u>

<b><u>Get started with bot</b></u>

<b>๏ /start -</b> starts the music bot.
<b>๏ /help -</b> get help menu with explanation of commands.
<b>๏ /reboot -</b> reboots the bot for your chat.
<b>๏ /settings -</b> shows the group settings with an interactive inline menu.
"""
