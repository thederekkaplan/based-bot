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
	await ctx.send(f'{user}\'s <:based:758844015767584799> count: {getcount(str(user.id))}')

@bot.command()
async def lb(ctx):
	leaderboard = sorted(count.items(), key=lambda x: x[1], reverse=True)
	print(leaderboard[0][0])
	await ctx.send(f'{bot.get_user(int(leaderboard[0][0])).mention} is the most based')

@bot.listen('on_message')
async def on_message(msg):
	if('<:based:758844015767584799>' in msg.content):
		await msg.add_reaction('<:based:758844015767584799>')
	elif('based on what' in msg.content.lower()):
		await msg.channel.send(f'{msg.author.mention} based on based')
	elif('based?' in msg.content.lower()):
		await msg.channel.send(f'{msg.author.mention} Based.')
	elif('unbased' in msg.content.lower()):
		await msg.add_reaction('🇺')
		await msg.add_reaction('🇳')
		await msg.add_reaction('🇧')
		await msg.add_reaction('🇦')
		await msg.add_reaction('🇸')
		await msg.add_reaction('🇪')
		await msg.add_reaction('🇩')
	elif('based' in msg.content.lower()):
		await msg.add_reaction('🇧')
		await msg.add_reaction('🇦')
		await msg.add_reaction('🇸')
		await msg.add_reaction('🇪')
		await msg.add_reaction('🇩')

bot.run(secret.payload.data.decode('UTF-8'))