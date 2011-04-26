#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# main.py of DreBot
#
#       Copyright 2011 dreadlish <krzysiek996@gmail.com>
#       
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the dreadlish nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys # for exit
import socket # for connecting to internet
import re # for regexps
import pickle # for saving data like seen and ops
import commands # its probably for #uptime - idk
import urllib # for google, and biszkopcik
import simplejson # for google
import time # for seen
import os # next for #uptime?
import random # for #slap

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #standard ipv4 socket - you can do it for ipv6 if you want

HOST = "chat.eu.freenode.net" # server
PORT = 6667 # port to connect to server

NAME = "DreBot" # nickname for bot on IRC

PREFIX = "#" # prefix for command

CHANNEL = "#trollownia" # channel, where DreBot is present

ops = { "unaffiliated/dreadlish": "Dreadlish" } # list of ops if data.pickled isn't present

seen = { } # last seen - this list is empty by default

auth_login = "" # login for nickserv
auth_password = "" # password for nickserv
# nouns and adjectives for #slap - you can skip to next comment
nouns = ['trout','space ship','Orlando Bloom','pi','apple pie',
'rad scorpion','rock band','metal band','Lord of the Rings',
'One','board','tv','floppy 5.25"','dschinn','dice','shadowrunner',
'gmail account','ebay auction','root account','joke','w6','w20','w4',
'undead','orang utan','Wolverine','Cpt. Picard','USS Enterprise',
'super sheep','worm','Gimp','sidekick','statue','statue of liberty',
'chat log','bot','staff','shotgun','rocket launcher','globus','w100',
'coffee cup','flip chart','cow','fret','comic book','laptop',
'bash script','daemon','BSD Devil','quiz','pirate','notebook','w10',
'towel','fish','salmon','herring','foot','tea pot','toilet','w3','w8',
'stunt actor','skeleton','dummy','Mr Johnson','counter','w12',
'robot','C64','copyright','EULA','licence key','crack',
'kombo','trailer','anime','Nemo','country singer','psychiatrist',
'author','wardrobe','red bull(tm) energy drink','linux distribution',
'role playing game','shisha','tomahawk','missile','councelor',
'IE Version 5.5','registration form','Windows CD','sheep','pet',
'Encyclopaedia Britannica','shelf of books','cover girl',
'walrus','python script','PRIVMSG','thermonuclear weapon',
'Nessie - the Loch Ness monster','hitch hikers guide to the galaxy',
'Schnappi (a crocodile)','clown fish','goblin','fairy',
'tuna (Still in the can)','dragon','pillow','hobgoblin',
'gremlin','golem','CD RW','mouse pad','character','wiki',
'gauntlet','plasma gun','rail gun','lighting gun','BFG',
'flak cannon','redeemer','sword of haste','bastard sword +3',
'dagger +6','sword of speed','axe of the heavens',
'sword +2','iPod','mac mini','Neuros','BMW Z4',
'wizard of the coast','decker','exile','bug','alien',
'smoke ring','thesis','glimps of his eye','snap of his finger',
'movie','DVD','magazine','laser cannon','pac man','Lara Craft',
'IP address','werewolf','news paper','asteroid','powerbook',
'wand of the elements','door','magnetic field','strength',
'misery','space marine','zergling','zealot','magician',
'journal','cookie','machine','super hero','orc','trading card',
'elven','finger','smile','rune','symbol','spell','VISA card',
'Steve Jobs','stone','dictionary','CVS','channel operator',
'coconut','perl one liner','DnD source book','brain',
'scroll of wisdom','scroll of identify','magic missile',
'tooth fairy','elephant','Tux','ninja','kungfu master',
'Frostmourne','Doombringer','discipline','endurance',
'rogue','fighter/wizard/thief','powergamer','munchkin',
'Merlin','donkey','Tie Fighter','X-Wing','Y-Wing',
'Millenium Falcon','light saber','stick','Jedi Knight',
'tissue','flower','half-orc','troll','slashdotter',
'monkey king','usurpator','prince','trolley',
'assassin','scroll of town portal','bit','video game',
'sword','Amulet of Yendor','Silmarillion','console',
'script', 'hammer','fork','carrot','smile','power','cheque',
'tricorder','Scotty','Harry','kamikaze pilot','agent',
'Keanu Reeves','network card','USB stick','hat','pipe',
'file system','piano','jet','perl','penguin','whistle',
'core dump','rfc','bottle','avatar','barkeeper','horn',
'Albus Dumbledore','Nazghul','ring','wand of fire',
'wand of blindness','wand of death','wand of destruction',
'club (with a nail in it)','Queen of England','taxi','monitor',
'marshmallow','girl scout','book by Stephen King','fist']
adjectives = ['large','small','foul','steam-powered','empty',
'stinkin','wild','rotten','big','huge','tiny','red',
'iron','glowin','rolling','random','well known','open sourced',
'fleeing','flying','book reading','gigantic','invisible',
'hitch hiking','spiky','heavy','rusty','haunted',
'chinese','fluffy','sweet','cushioned','used','summoned',
'magic','trusted','fuzzy','unnatural','sharp',
'chaotic, good','chaotic, evil','awesome',
'surreal','alien','shipped','serialized','unnoticed',
'dark','polished','dead','emerald','shiny','new','old',
'nifty','talking','burning','frozen','mechanic',
'gas-powered','golden','silver','spicy','unholy',
'mindless','boring','lost','ancient','unworthy',
'precious','expensive','eerie','damaged','rugged',
'xenophobic','feared','casted','cursed',
'uncursed','blessed','speaking','chatting','idling',
'teeny-weeny','romantic','undead','blinking','built',
'resurrected','german','american','english',
'ascended','dumb','dull','russian','korean','nick named',
'bug-free','buggy','symbolic','real','unrealistic',
'unreal','twisted','returning','remote controlled',
'evil','dangerous','armoured','bad','good','enourmous',
'murderous','vicious','mysterous','forgotten','found',
'semi-functional','non-functional','fatal','self-made',
'morbid','crying','powerful','stolen','hidden',
'blue','yellow','pink','white','black','green','painted',
'colorful','holy','meaningful','monstrous',
'virtual','private','public','smellin','vile']
#end of nouns and adjectives

# DreBot answers in polish - if you like you can translate it to other languages
def connect(so):
	while True:
		try:
			so.connect((HOST, PORT))
			so.send("USER drebot 8 * :DreBot\n")
			so.send("NICK " + NAME + "\n")
			so.send("PRIVMSG NickServ :IDENTIFY " + auth_login + " " + auth_password + "\n") 
			break
		except:
			warnmsg("Cannot connect to server! Reconnecting...")
			connect(s)
	return



def kickban(s, mes):
	prog = re.compile(mes[0].split("@")[1])
	if prog.search(" ".join(ops.keys())):
			if len(mes) >= 3:
				s.send("MODE " + CHANNEL + " +b " + mes[4].split('\r')[0] + "\n")
				s.send("KICK " + CHANNEL + " " + mes[4].split('\r')[0] + "\n")
	return

def ban(s, mes):
	prog = re.compile(mes[0].split("@")[1])
	if prog.search(" ".join(ops.keys())):
			if len(mes) >= 5:
				if len(mes) >= 6:
					s.send("MODE " + CHANNEL + " +b " + mes[4].split("\r")[0] + " :" + mes[5].split("\r")[0] + "\n")
					return
				s.send("MODE " + CHANNEL + " +b " + mes[4].split('\r')[0] + "\n")
	return

def kick(s, mes):
	prog = re.compile(mes[0].split("@")[1])
	if prog.search(" ".join(ops.keys())):
			if len(mes) >= 5:
				if len(mes) >= 6:
					s.send("KICK " + CHANNEL + " " + mes[4].split("\r")[0] + " :" + mes[5].split("\r")[0] + "\n")
				s.send("KICK " + CHANNEL + " " + mes[4].split('\r')[0] + "\n")
				infomsg(mes[4].split('\r')[0] + " is kicked.")
	return

def remove(s, mes):
        prog = re.compile(mes[0].split("@")[1])
	if prog.search(" ".join(ops.keys())):
		if len(mes) >= 5:
			s.send("REMOVE " + CHANNEL + " " + mes[4].split('\r')[0] + "\n")
			infomsg(mes[4].split('\r')[0] + " is kicked by remove.")
	return
def unban(s, mes):
	prog = re.compile(mes[0].split("@")[1])
	if prog.search(" ".join(ops.keys())):
			if len(mes) >= 5:
				s.send("MODE " + CHANNEL + " -b " + mes[4].split('\r')[0] + "\n")
	return

def op(s, mes):
	prog = re.compile(mes[0].split("@")[1])
	if prog.search(" ".join(ops.keys())):
			if len(mes) >= 5:
				s.send("MODE " + CHANNEL + " +o " + mes[4].split('\r')[0] + "\n")
				infomsg(mes[4].split('\r')[0] + " is op now.")
	return

def deop(s, mes):
	prog = re.compile(mes[0].split("@")[1])
	if prog.search(" ".join(ops.keys())):
			if len(mes) >= 5:
				s.send("MODE " + CHANNEL + " -o " + mes[4].split('\r')[0] + "\n")
				infomsg(mes[4].split('\r')[0] + " isn't op now.")
	return

def voice(s, mes):
	prog = re.compile(mes[0].split("@")[1])
	if prog.search(" ".join(ops.keys())):
			if len(mes) >= 5:
				s.send("MODE " + CHANNEL + " +v " + mes[4].split('\r')[0] + "\n")
				infomsg(mes[4].split('\r')[0] + " is voiced now.")
	return

def devoice(s, mes):
	prog = re.compile(mes[0].split("@")[1])
	if prog.search(" ".join(ops.keys())):
			if len(mes) >= 5:
				s.send("MODE " + CHANNEL + " -v " + mes[4].split('\r')[0] + "\n")
				infomsg(mes[4].split('\r')[0] + " isn't voiced now.")
	return

def addadm(s, mes):
	prog = re.compile(mes[0].split("@")[1])
	if prog.search(" ".join(ops.keys())):
		if len(mes) >= 6:
			if re.search(mes[4], " ".join(ops.keys())) == None:
				ops[mes[4].split('\r')[0]] = mes[5].split('\r')[0]
				s.send("PRIVMSG " + CHANNEL + " :Ok\n")
				infomsg(mes[4].split('\r')[0] + " added to ops")
	return

def rmadm(s, mes):
	prog = re.compile(mes[0].split("@")[1])
	if prog.search(" ".join(ops.keys())):
		if len(mes) >= 5:
			if re.search(mes[4].split('\r')[0], " ".join(ops.keys())):
				if re.search(mes[4].split('\r')[0], " ".join(ops.keys())).start() != 0:
					ops.pop(mes[4].split('\r')[0])
					s.send("PRIVMSG " + CHANNEL + " :" + mes[4].split('\r')[0] + " nie może już adminować\n")
			return
		s.send("PRIVMSG " + CHANNEL + " :Nie ma takiego, albo nie jest admem\n")
	return

def save(s, mes):
	try:
		os.remove("data.pickled")
		os.remove("seen.pickled")
	except:
		infomsg("Nie ma plików")
	picklink = file("seen.pickled", "w")
	pickle.dump(seen, picklink)
	del picklink
	picklink = file("data.pickled", "w")
	pickle.dump(ops, picklink)
	del picklink
	return

def quit(s, mes):
	prog = re.compile(mes[0].split("@")[1])
	if prog.search(" ".join(ops.keys())):
		try:
			os.remove("data.pickled")
			os.remove("seen.pickled")
		except:
			infomsg("Nie ma plików")
		picklink = file("seen.pickled", "w")
		pickle.dump(seen, picklink)
		del picklink
		picklink = file("data.pickled", "w")
		pickle.dump(ops, picklink)
		del picklink
		s.send("QUIT :Bless dla was!\n")
		time.sleep(2)
		s.close()
		sys.exit(0)
		return

def google(s, mes):
	try:
		lol = googlesearch(" ".join(mes[4:].split("\r")[0]))
		s.send("PRIVMSG " + CHANNEL + " :" + mes[0].split("!")[0][1:] + ": " + lol['title'].replace("<b>", "").replace("</b>","") + " - " + lol['url'] + "\n")
	except:
		s.send("PRIVMSG " + CHANNEL + " :Nie moge guglać :(\n");
	return

def whenseen(s, mes):
	if len(mes) >= 5:
		delikwent = mes[4].split('\r')[0]
		if seen.has_key(delikwent.lower()):
			s.send("PRIVMSG " + CHANNEL + " :" + mes[0].split("!")[0][1:] + ": " + delikwent + " był widziany: " + seen[delikwent.lower()] + "\n")
			return
		s.send("PRIVMSG " + CHANNEL + " :" + mes[0].split("!")[0][1:] + ": " + delikwent + " nie był widziany\n")
	return

def helper(s, mes):
	s.send("PRIVMSG " + CHANNEL + " :" + mes[0].split("!")[0][1:] + ": Possible commands: ")
	for i in commandy.keys():
		s.send(PREFIX + i + " ")
	s.send("\n")
	return

def sops(s, mes):
	s.send("PRIVMSG " + CHANNEL + " :" + mes[0].split("!")[0][1:] + ": " + " ".join(ops.values()) + "\n")
	return

def biszkopcik(s, mes): #this is uptime for my friend
	try:
		lol = urllib.urlopen("http://biszkopcik.eu/uptime.txt").read()
		s.send("PRIVMSG " + CHANNEL + " :" + lol + "\n")
	except:
		s.send("PRIVMSG " + CHANNEL + " :Biszkopcik wyłączył serwer.\n");
	return

def ping(s, mes):
	s.send("PRIVMSG " + CHANNEL + " :" + mes[0].split("!")[0][1:] + ": pong\n")
	infomsg("Sent pong by channel")
	return

def pong(s, mes):
	s.send("PRIVMSG " + CHANNEL + " :" + mes[0].split("!")[0][1:] + ": ping\n")
	infomsg("Sent ping by channel")
	return

def uptime(s, mes):
	s.send("PRIVMSG " + CHANNEL + " :" + commands.getoutput("uptime") + "\n")
	return

def infor(s, mes):
	s.send("PRIVMSG " + CHANNEL + " :To jest DreBot. Więcej info: http://dreadlish.co.cc/drebot\n")
	return

def tia(s, mes):
	s.send("PRIVMSG " + CHANNEL + " :Funkcjonuje.\n")
	return

def slap(s, mes):
	if len(mes) >= 5:
		if mes[4].split('\r')[0] != NAME:
			s.send("PRIVMSG " + CHANNEL + " :\x01ACTION slaps " + mes[4].split('\r')[0] + " around with a " + random.choice(adjectives) + " " + random.choice(nouns) + "\x01\n")  
		else: 
			s.send("PRIVMSG " + CHANNEL + " :\x01ACTION slaps " + mes[0].split('!')[0][1:] + " around with a " + random.choice(adjectives) + " " + random.choice(nouns) + "\x01\n")
	else: 
		s.send("PRIVMSG " + CHANNEL + " :\x01ACTION slaps " + mes[0].split('!')[0][1:] + " around with a " + random.choice(adjectives) + " " + random.choice(nouns) + "\x01\n")
	return

commandy = { "remove" : remove,
	     "slap" : slap,
	     "chodzisz" : tia,
	     "op" : op,
	     "deop" : deop,
	     "voice" : voice,
	     "devoice" : devoice,
	     "k" : kick,
	     "b" : ban,
	     "kb" : kickban,
	     "kick" : kick,
	     "ban" : ban,
             "kickban" : kickban,
	     "bankick" : kickban,
	     "unban" : unban,
	     "addadm" : addadm,
	     "rmadm" : rmadm,
	     "save" : save,
	     "quit" : quit,
	     "g" : google,
	     "seen" : whenseen,
	     "help" : helper,
	     "info" : infor,
	     "sops" : sops,
	     "ping" : ping,
	     "pong" : pong,
	     "biszkopcik" : biszkopcik,
	     "uptime" : uptime }


def parse(s, message):
	mes = message.split(" ")
	if mes[0] == "PING":
		s.send("PONG " + mes[1] + "\n")
		infomsg("Send PONG " + mes[1])
		return
	if mes[0].split("!")[0][1:] == NAME:
		if (mes[1] == "PART") or (mes[1] == "KICK"):
			s.send("JOIN " + CHANNEL + "\n")
			return
	if mes[2] == NAME:
		if mes[3] == ":\x01PING":
			nejm = mes[0].split("!")[0]
			stir = " ".join(mes[4:])
			s.send("NOTICE " + nejm[1:] + " :\x01PING " + stir + "\n")
			infomsg("Sent PONG by CTCP")
			return
	if mes[2] == CHANNEL || mes[2] == NAME:
		if len(mes) > 2:
			if len(mes[3].split(PREFIX)) == 2:
				komenda = mes[3].split(PREFIX)[1]
				if commandy.has_key(komenda.split('\r')[0]):
					commandy[komenda.split('\r')[0]](s, mes)
					return
		seen[mes[0].split("!")[0][1:].lower()] = czaspolski() + ": " + " ".join(mes[3:])[1:] # << seen is here <<
	if len(mes) >= 4:	
		if re.search("KICK", mes[3]):
			if re.search(NAME, mes[3]):
				s.send("JOIN " + CHANNEL + "\n")
			return
	return

def googlesearch(what):
	query = urllib.urlencode({"q" : what})
	url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query
	search_results = urllib.urlopen(url)
	json = simplejson.loads(search_results.read())
	results = json['responseData']['results']
	ret = results[0]
	return ret

def czaspolski():
	czas = time.gmtime()
	ret = "%d.%d.%d %d:%d" % (czas.tm_mday, czas.tm_mon, czas.tm_year, czas.tm_hour, czas.tm_min)
	return ret

def warnmsg(message):
	print "[!] %s" % (message)

def infomsg(message):
	print "[*] %s" % (message)
		
def linerecv(s):
	ret = ''
	
	while True:
		c = s.recv(1)
		if c == '\n' or c == '':
			break
		else:
			ret += c
	return ret


if __name__ == "__main__":
	try:
		picklink = file("data.pickled")
		ops = pickle.load(picklink)
		picklink = file("seen.pickled")
		seen = pickle.load(picklink)
	except:
		warnmsg("data.pickled not found")
	infomsg("Data succesfully unpickled, creating socket and connecting...")
	connect(s)
	infomsg("Connection opened. Joining into channel " + CHANNEL + "...")
	while True:
		try:
			buf = linerecv(s)
		except socket.timeout:
			connect(s)
		print buf
		if re.search("unaffiliated", buf):
			break
	time.sleep(5)
	s.send("JOIN " + CHANNEL + "\n")
	infomsg("Joined. Bot started.")
	while 1:
		try:
			buf = linerecv(s)
		except socket.timeout:
			connect(s)
		print buf
		parse(s, buf)
