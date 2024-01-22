# imports
import asyncio
import json
import os

import nextcord
from nextcord import ButtonStyle, Color, Embed, File
from nextcord.ext import commands, tasks
from nextcord.ui import Button, View

from keep_alive import keep_alive

keep_alive()
# startups
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='+', intents=intents)
bot.remove_command('help')

for fn in os.listdir("./cogs"):
  if fn.endswith(".py"):
    bot.load_extension(f"cogs.{fn[:-3]}")


@bot.event
async def on_ready():
  print("Kingdom Helper bot is connected")
  channel = bot.get_channel(1182755332280287232)
  await bot.change_presence(activity=nextcord.Activity(
      type=nextcord.ActivityType.playing, name="Late Night  | +help"))

  if channel:
    voice_client = await channel.connect()


def create_help_embed(ctx):
  embed = nextcord.Embed(title="Command Help",
                         description="Here are some available commands:",
                         color=nextcord.Color.red())
  embed.set_author(
      name=ctx.author.name,
      icon_url=
      'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
  )
  embed.set_footer(
      text=f"Requested by {ctx.author.name}",
      icon_url=
      "https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473"
  )
  embed.add_field(name="+ban",
                  value="Ban a user from the server.",
                  inline=False)
  embed.add_field(name="+unban",
                  value="Unban a user from the server.",
                  inline=False)
  embed.add_field(name="+jail", value="Jail a user.", inline=False)
  embed.add_field(name="+unjail", value="Unjail a user.", inline=False)
  embed.add_field(name="+vg", value="Verification for girls.", inline=False)
  embed.add_field(name="+vb", value="Verification for boys.", inline=False)
  embed.add_field(name="+warn", value="Warn a user.", inline=False)
  embed.add_field(name="+gstart", value="Start a giveaway!.", inline=False)

  return embed


@bot.command(name='help', help='Show a list of available commands.')
async def help(ctx):
  embed = create_help_embed(ctx)
  await ctx.send(embed=embed)


my_secret = os.environ['MTE4Mjc5MTI5Nzk1ODk1Mjk4Mw.G_nmM3.X70rcbVpM2Z5HnKdkvo1YdCmbS_fQbKwgjLg1k']
bot.run(my_secret)
