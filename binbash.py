#!/usr/bin/env python
# BinBashCord, Discord quote bot based on an IRC quote bot.
# BinBashCord is Copyright 2017-2018 Dylan Morrison based on code
# Copyright 2010 Dylan Morrison
# See LICENSE file for licensing.

# Users: Edit these
TOKEN=""             # Discord authentication token for the bot.

CHANNELIDS=[]        # List of channel IDs to listen on

RESTRICTADD=False    # Restrict adding quotes to certain roles
ROLEIDS=[]           # List of role IDs allowed to add quotes.

ALLOWPMS=True        # Allow responding to PMs

MAINTAINER="Someone" # Your name/handle/whatever here.

# Users: Do not edit below here

import discord
import asyncio
import os
import sys
import re
from random import choice, randint

# Removed due to discord flood protection. Probably not needed anymore anyway.
#
#def slicestring(input):
#	if len(input) < 1994:
#		return [input]
#	else:
#		return list(filter(lambda x: x != '', re.split("(.{1,1994} )", input+" ")))
#

def slicestring(input):
	if len(input) < 1994:
		return [input]
	else:
		return [input[0:1994]]

client = discord.Client()

@client.event
async def on_ready():
	print('BinBash logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')


@client.event
async def on_message(message):
	origin = message.author
	dest = message.channel
	if ((dest.is_private == False) and (dest.id not in CHANNELIDS)) or ((dest.is_private == True) and (ALLOWPMS == False)):
		return
	msg = message.content
	splitmsg = msg.split(' ')
	command = splitmsg[0]
	recom = re.match("^!([a-zA-Z0-9]+)bash$", command)
	if recom != None:
		try:
			with open("bashes/" + recom.group(1) + ".txt") as bashfile:
				for i, l in enumerate(bashfile):
					pass
				numlines = i + 1
				bashfile.seek(0)
				lines = bashfile.readlines()
				if (len(splitmsg) == 2) and (re.match("^[0-9]+$", splitmsg[1]) != None) and (int(splitmsg[1]) > 0) and (int(splitmsg[1]) < len(lines)):
					linenum = int(splitmsg[1])
					if linenum == None:
						await client.send_message(dest, 'Malformed command. (Invalid line number *' + splitmsg[1] + '*)')
						return
				else:
					linenum = randint(1, numlines)
				myline = lines[linenum - 1]
			slicelist = slicestring(myline.rstrip())
			await client.send_message(dest, str(linenum) + ". " + slicelist[0])
			del slicelist[0]
			if slicelist != []:
				for tmpline in slicelist:
					await client.send_message(dest, tmpline)
		except IOError as e:
			await client.send_message(dest, 'Sorry, *' + recom.group(1) + 'bash* is not a valid bash file, or another error occurred: IOError #' + str(e.errno) + ' ' + str(e))
	if (command == "!addquote") and (len(splitmsg) >= 3) and (re.match("^[a-zA-Z0-9]+$", splitmsg[1]) != None):
		if (dest.is_private == True) and (RESTRICTADD == True): # Can't check roles on a private message.
			await client.send_message(dest, 'Sorry, you are not authorized to add quotes over PM.')
			return
		if RESTRICTADD == True: 
			allowed = False
			for role in origin.roles:
				if role.id in ROLEIDS:
					allowed = True
			if allowed == False:
				await client.send_message(dest, 'Sorry, you are not authorized to add quotes to the database.')
				return
		try:
			output = open("bashes/" + splitmsg[1] + ".txt", "a")
			output.write(" ".join(splitmsg[2:]) + "\n")
			output.close()
			await client.send_message(dest, 'Quote successfully added to ' + splitmsg[1] + "bash.")
		except IOError as e:
			await client.send_message(dest, 'IOError adding quote. Is *' + splitmsg[1] + 'bash* a valid bash file? Ask ' + MAINTAINER + '. IOError #' + str(e.errno) + ' ' + str(e))
	elif command == "!bashes":
		liststring = " ".join(os.listdir("bashes/"))
		liststring = re.sub(".txt", "", liststring)
		await client.send_message(dest, 'Bashes currently in my list: ' + liststring)


client.run(TOKEN)

