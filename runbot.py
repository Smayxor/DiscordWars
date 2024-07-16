import datetime
import time
import ujson as json
import math
import threading
import sys
import random
from discord.ext import tasks
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
import requests
import os

init = json.load(open('apikey.json'))
BOT_TOKEN = init['APP_TOKEN']
BOT_APP_ID = init['APP_ID']

class MyNewHelp(commands.MinimalHelpCommand):
	async def send_pages(self):
		strHelp = """}help for commands for Smayxor
/gex ticker dte strike-count charttype
/8ball followed by a question, ending in ?
/news days <- Displays upcoming events

The blue bars on left are OI.
The Red/Green bars left of the strikes are Total Gamma Exposure.
To the right of the strikes is Call Put GEX individually

}gm }tits }ass }pump }dump also exist"""
		destination = self.get_destination()
		for page in self.paginator.pages:
			await destination.send(strHelp)
bot = commands.Bot(command_prefix='}', intents=discord.Intents.all(), help_command=MyNewHelp(), sync_commands=True)

@bot.event
async def on_ready():
	pass
	
@bot.event
async def on_message(message):
	print( f'Message Event?!?!? {message}' )
	
@tasks.loop(seconds=30)
async def your_loop():
	pass

class AddUserButton(ui.Button):
	def __init__(self):
		super().__init__(label="Add Me!", style=discord.ButtonStyle.green)

	async def callback(self, intr: discord.Interaction):
		# Get the role you want to add the user to
		#role_id = 1234567890  # Replace with the actual role ID
		#role = intr.guild.get_role(role_id)

		await intr.response.send_message(f"{intr.user.global_name} you've clicked my button")#, ephemeral=True)


@bot.tree.command(name="farm", description="Answers your question?")
async def slash_command_farm(intr: discord.Interaction):
	perms = await checkInteractionPermissions( intr )
	await intr.response.defer(thinking=True)#, ephemeral=perms[3]==False)	
	
	#print( val )
	view = ui.View()
	view.add_item(AddUserButton())

	#do stuff
	#await intr.response.send_message(response)
	await intr.followup.send(f'{perms[0]} is farming stuff', view=view)
#	await intr.message.add_reaction("🤩")
	
def getToday():
	dateAndtime = str(datetime.datetime.now()).split(" ")
	tmp = dateAndtime[1].split(".")[0].split(":")
	minute = (float(tmp[0]) * 10000) + (float(tmp[1]) * 100) + float(tmp[2])
	return (dateAndtime[0], minute)

TodaysUsers = {}
TodaysUsers['today'] = getToday()[0]
def confirmUser(userID):
	global TodaysUsers
	tday = getToday()
	if not tday[0] in TodaysUsers['today'] : #The cooldown Time doesnt include date, so.......reset it on new day
		#TodaysUsers = {}
		TodaysUsers['today'] = tday[0]
		for user in TodaysUsers :
			if user == "today" : continue
			TodaysUsers[user] = tday[1] - 10  #Reset cooldowns on new day or else!!!
	if userID in TodaysUsers :
		userCooldown = tday[1]-TodaysUsers[userID]
		if userCooldown > 10 :
			TodaysUsers[userID] = tday[1]
			return 0
		else :
			return 10 - userCooldown
	else :
		TodaysUsers[userID] = tday[1]
		return 0

#@app_commands.checks.has_permissions(moderate_members=True)
async def checkInteractionPermissions(intr: discord.Interaction):
	userID = intr.user.id
	coolDown = confirmUser(f'{intr.user.global_name}#{userID}')
	#intr in a Channel = 'app_permissions', 'application_id', 'channel', 'channel_id', 'client', 'command', 'command_failed', 'context', 'created_at', 'data', 'delete_original_response', 'edit_original_response', 'entitlement_sku_ids', 'entitlements', 'expires_at', 'extras', 'followup', 'guild', 'guild_id', 'guild_locale', 'id', 'is_expired', 'is_guild_integration', 'is_user_integration', 'locale', 'message', 'namespace', 'original_response', 'permissions', 'response', 'token', 'translate', 'type', 'user', 'version'
	
	if intr.guild_id is None : return (userID, coolDown, True, True)  #We are in a DM and can do anything we want
	permissions = intr.permissions
	textable = permissions.send_messages == True
	imageable = permissions.attach_files == True
	return ( userID, coolDown, textable, imageable )

bot.run(BOT_TOKEN)