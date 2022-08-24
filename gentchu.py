from typing import AnyStr
import discord
from database.psql_db import *
from database.objects import *
from asyncio import sleep
from twitter_downloader import download_from_twitter
from os import remove

TWITTER_VIDEO_TMP = "./tmp/var_tmp_vd.mp4"

class Gentchu(discord.Client):
	"""
	Basic class client for the bot
	"""

	async def on_ready(self):
		print("logged as ", self.user)
	
	async def on_message(self, message):
		curses = CursedUsers()
		if message.author == self.user:
			return 
		elif curses.is_cursed(message.author.id):
			await message.delete()
			msg = await message.channel.send("Nono you're cursed my dear, now SHUT THE FUCK UP'")
			await sleep(1.5)
			await msg.delete()
		else:
			# defines internal functions
			if not message.content.startswith("sh"): return 
			else:
				# runs commands content
				spl = message.content.split(" ")
				if spl[1] == "port":
					ports = Portifolios()
					if len(spl) <= 3:
						# using_id = message.author.id if not len(message.mentions) else message.mentions[0].id
						usr = message.author if not len(message.mentions) else message.mentions[0]
						p = ports.get_portifolio(usr.id)
						if p.user_id != usr.id:
							await message.reply("You don't have a portifolio yet!'")
						else:
							dd = Distros()
							em = discord.Embed()
							em.title = f"{usr} portifolio's: "
							em.add_field(name="Distro Name", value=p.distro, inline=False)
							em.add_field(name="Favorite Languages", value=", ".join(p.fav_langs), inline=True)
							em.add_field(name="Github", value=p.github_link, inline=False)
							em.add_field(name="Custom URL", value=p.custom_link, inline=False)
							em.set_thumbnail(url=dd.get_distro_url(p.distro))
							await message.channel.send(embed=em)
					elif spl[2] == "add":
						uid = message.author.id
						wait_callback = lambda m: m.author.id == uid and m.channel == message.channel
						await message.channel.send("Insert your Favorite distro")
						m_distro = await self.wait_for("message", check=wait_callback, timeout=60.0)
						await message.channel.send("Now insert your favorite languages (like this -> lang1, lang2)")
						m_langs = await self.wait_for("message", check=wait_callback, timeout=60.0)
						await message.channel.send("Now insert your github link")
						m_git  = await self.wait_for("message", check=wait_callback, timeout=60.0)
						await message.channel.send("Now insert a custom URL")
						m_url  = await self.wait_for("message", check=wait_callback, timeout=60.0)
						port = DevData((uid, m_distro.content, m_langs.content.split(", "), m_git.content, m_url.content))
						ports.add_portifolio(port)
						await message.channel.send("Created your portifolio now UWU")
					elif spl[2] == "update":
						if ports.check_userid(message.author.id):
							uid = message.author.id
							wait_callback = lambda m: m.author.id == uid and m.channel == message.channel
							await message.channel.send("Insert your Favorite distro")
							m_distro = await self.wait_for("message", check=wait_callback, timeout=60.0)
							await message.channel.send("Now insert your favorite languages (like this -> lang1, lang2)")
							m_langs = await self.wait_for("message", check=wait_callback, timeout=60.0)
							await message.channel.send("Now insert your github link")
							m_git  = await self.wait_for("message", check=wait_callback, timeout=60.0)
							await message.channel.send("Now insert a custom URL")
							m_url  = await self.wait_for("message", check=wait_callback, timeout=60.0)
							port = DevData((uid, m_distro.content, m_langs.content.split(", "), m_git.content, m_url.content))
							ports.update_portifolio(port)
							await message.channel.send("Updated your portifolio now UWU")
						else: await message.channel.send("You dont have a portifolio yet!")
					elif spl[2] == "del":	
						if ports.check_userid(message.author.id):
							callback = lambda m: m.author.id == message.author.id and m.channel == message.channel
							await message.reply("Do you really want to delete your portifolio in all the servers with me? (y/n)")
							m_confirm = self.wait_for("message")
						else: await message.channel.send("You dont have a portifolio yet!")
				elif spl[1] == "curse":
					if curses.check_author(message.author.id):
						if len(message.mentions) == 0:
							await message.reply("Pwease, mention the user you want to curse")
						else:
							for cui in message.mentions: 
								if not curses.check_author(cui.id) and cui.id != self.user:
									curses.add_cursed(cui.id)
							await message.reply("Cursed those users for you masta")
					else:
						await message.reply("Only my creator can put someone in that list.")
				elif spl[1] == "uncurse":
					if curses.check_author(message.author.id):
						if len(message.mentions) == 0:
							await message.reply("Pwease, mention the user you want to curse")
						else:
							for cui in message.mentions: 
								curses.del_cursed(cui.id)
							await message.reply("Uncursed and blessed  users for you masta")
					else:
						await message.reply("Only my creator can remove someone in that list.")
				elif spl[1] == "cursehist":
					ll = curses.list_users()
					content = ">>> Cursed users on this server\n"
					guild_list = []
					for i in ll:
						u = await self.fetch_user(i[0])
						with open("debug.log", "w") as log:
							log.write("\n".join([str(x) for x in message.guild.members]))
						if await message.guild.fetch_member(i[0]) != None:
							guild_list.append(f"<@{i[0]}>")
					if len(guild_list) == 0:
						await message.channel.send("No users cursed in this channel yet")
					else:
						for gi in guild_list: content += gi + "\n"
						await message.channel.send(content)
				elif spl[1] == "distro_test":
					dd = Distros()
					await message.reply(dd.get_distro_url(spl[2]))
				elif spl[1] == "scoord":
					uid = message.author.id
					x, y, z = [float(i) for i in spl[3].split("/")]
					nc = Coordinate((uid, spl[2], x, y, z))
					mc = MinecraftCoordinates()
					mc.add_coordinate(nc)
					await message.reply("Added coordinate " + spl[3])
				elif spl[1] == "coords":
					mc = MinecraftCoordinates()
					try:
						if len(spl) == 3:
							await message.channel.send(mc.get_coordinate(spl[2], message.author.id).__message__())
						elif len(spl) == 4 and len(message.mentions):
							await message.channel.send(mc.get_coordinate(spl[2], message.mentions[0].id).__message__())
						else:
							m = ""
							for c in mc.get_user_coordinates(message.author.id):
								m += c.__message__() + "\n"
							await message.channel.send(m)
					except MinecraftCoordinates.CoordinateNotFound:
						await message.reply("You don't have any coordinates yet")
				elif spl[1] == "dcoord":
					try:
						mc = MinecraftCoordinates()
						if len(spl) == 3:
							c = Coordinate((message.author.id, spl[2], 0, 0, 0))
							mc.del_coordinate(c)
							await message.reply("Deleted coordinate " + spl[2])
					except MinecraftCoordinates.CoordinateNotFound:
						await message.reply(f"No such coordinate **{spl[2]}**")
				elif spl[1] == "ucoord":
					mc = MinecraftCoordinates()
					uid = message.author.id
					x, y, z = [float(i) for i in spl[3].split("/")]
					nc = Coordinate((uid, spl[2], x, y, z))
					# mc = MinecraftCoordinates()
					mc.upd_coordinate(nc)
					await message.reply("Updated coordinate " + spl[3])
				elif spl[1] == "alink":
					sl = SavedLinks()
					if len(spl) == 4:
						al = SavedLink((message.author.id, spl[2], spl[3]))
						sl.add_link(al)
						await message.reply("Saved link " + spl[2])
				elif spl[1] == "unlink":
					sl = SavedLinks()
					if len(spl) == 3:
						rl = SavedLink((message.author.id, spl[2], None))
						sl.del_link(rl)
						await message.reply("Removed link " + spl[2])
				elif spl[1] == "link":
					sl = SavedLinks()
					if len(spl) == 3:
						ll = sl.get_link(spl[2], message.author.id)
						await message.reply(ll.__message__())
					else:
						listl = [l.__message__() for l in sl.get_user_links(message.author.id)]
						c = "\n".join(listl) if len(listl) else "No links saved by YOU...Dumbass"
						await message.reply(c)
				elif spl[1] == "cup":
					cc = CoffeeCounter()
					cc.add_counter(message.author.id)
					await message.channel.send(f"{message.author} got a coffee cup how delicious!")
				elif spl[1] == "cups":
					cc = CoffeeCounter()
					cn = cc.get_counter(message.author.id)
					tm = cn.last_cup.strftime("%d-%m-%y %H:%M:%S")
					await message.channel.send(f"{message.author} drank {cn.total} coffee cups or whatever, last one at: {tm}")
				elif spl[1] == "dtwitter":
					await message.reply("Downloading pwease wait")
					download_from_twitter(spl[2], TWITTER_VIDEO_TMP)
					fl = discord.File(TWITTER_VIDEO_TMP)
					await message.channel.send(file=fl)
					remove(TWITTER_VIDEO_TMP)





					
					
	
		



