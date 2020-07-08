import discord
from discord.ext import commands
import EAN
import requests
import image_output

DISCORD_TOKEN = ""



bot = commands.Bot(command_prefix='!')


@bot.command()
async def tokens(ctx):
	command_parts = ctx.message.content.split(" ")[1:]

	#parse command
	if len(command_parts) == 1:
		url = command_parts[0]

	else:
		return


	#let the user know the command went through
	await ctx.send('Working on your request...')


	#get tokens from domain services
	findings = EAN.get_all_tokens(url)


	loop = 0
	if len(findings) > 0:
		for finding_data in findings:
			
			if loop >= 3:
				continue
			else:
				loop += 1


			token  = finding_data['token'].strip()
			url    = finding_data['url'].strip()
			source = finding_data['source']


			image_output.save_image(source, token)

			message_to_send = "%s found in %s" % (token, url)

			file = discord.File("output.jpg", filename="zoinks.jpg")
			await ctx.send(message_to_send, file=file)

	else:
		#if no tokens have been leaked
		await ctx.send("No Tokens Found")

bot.run(DISCORD_TOKEN)
