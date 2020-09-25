#!/usr/bin/env python3
import discord
import typing
from discord.ext import commands
from google.cloud import secretmanager

bot = commands.Bot('$');

count = dict()

manager = secretmanager.SecretManagerServiceClient()

secret = manager.access_secret_version('projects/commanding-way-273100/secrets/discord/versions/latest')

def increment(key):
	if(key in count):
		count[key] += 1
	else:
		count[key] = 1

def decrement(key):
	if(key in count):
		count[key] -= 1
	else:
		count[key] = 0

def getcount(key):
	if(key in count):
		return count[key]
	else:
		return 0

@bot.event
async def on_ready():
	print('logged in as {0.user}'.format(bot))

@bot.command()
@commands.is_owner()
async def logout(ctx):
	await ctx.message.add_reaction('👋')
	await bot.logout()

@bot.event
async def on_reaction_add(reaction, user):
	if reaction.emoji.id == 758844015767584799:
		increment(str(reaction.message.author.id))

@bot.event
async def on_reaction_remove(reaction, user):
	if reaction.emoji.id == 758844015767584799:
		decrement(str(reaction.message.author.id))

@bot.command()
async def based(ctx, user: discord.Member=None):
	if user == None:
		user = ctx.message.author
	await ctx.send(f'{user}\'s based count: {getcount(str(user.id))}')

@bot.event
async def on_message(msg):
	if(msg.content.lower() == 'based'):
		await msg.channel.send(f'{msg.author.mention}, based!')
	if(msg.content.lower() == 'based on what' or msg.content.lower() == 'based on what?'):
		await msg.channel.send(f'{msg.author.mention}, based on based')
	await bot.process_commands(msg)

bot.run(secret.payload.data.decode('UTF-8'))