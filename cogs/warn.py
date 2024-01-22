import nextcord
from nextcord.ext import commands
from nextcord import Embed, Color
import aiosqlite
import asyncio
import datetime
from main import *


class warn(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    self.bot.db = await aiosqlite.connect('tokyo.db')
    await asyncio.sleep(3)
    async with self.bot.db.cursor() as cursor:
      await cursor.execute('''
              CREATE TABLE IF NOT EXISTS warn (user INTEGER, reason TEXT)''')
    await self.bot.db.commit()
    print("warn database has been connected")

  async def addwarn(self, ctx, reason, user):
    async with self.bot.db.cursor() as cursor:
      await cursor.execute("INSErt INTO warn (user, reason) VALUES (?, ?)",
                           (user.id, reason))
    await self.bot.db.commit()

  # warning command
  @commands.command()
  async def warn(self, ctx, user_id: int = None, *, reason=None):
    allowed_roles = [
        1183531782801477773, 1183524854285209721, 1183524811230674955,
        1183524776866754720, 1182822068568477766, 1183533552156020766,
        1183191058574745640, 1139268098906673324, 1123215434808827974,
        1068358173376909413, 1166376601131438140,         1168892055427240008
    ]
    if not any(role.id in allowed_roles for role in ctx.author.roles):
      await ctx.send("**You do not have permission to run this command**",
                     delete_after=15)
      return
    if user_id is None or reason is None:
      await ctx.send(
          "**I need an user id and a reason in order to run this command: `Syntax: +warn member.id reason`**",
          delete_after=15)
      return
    user = ctx.guild.get_member(user_id)
    warn_log = ctx.guild.get_channel(1184599500006887485)
    if not warn_log:
      await ctx.send("⚠️log not found, please inform the developer")
      return
    if not user:
      await ctx.send("🤔No member with that id has been found", delete_after=10)
      return
    await self.addwarn(ctx, reason, user)
    warn_embed = Embed(
        description=
        f"{user.mention} has been successfully **WARNED** by {ctx.author.mention} for `{reason}`",
        color=Color.green())
    warn_embed.set_author(name="Late Night    Moderation")
    await ctx.send(embed=warn_embed)
    command_date = datetime.datetime.now().strftime("%d/%m/%y")
    warn_log_message = Embed(title=" 📃 Warn Logs", color=Color.random())
    warn_log_message.add_field(name=" 👤 Username",
                               value=f"`{user.display_name}`",
                               inline=True)
    warn_log_message.add_field(name=" 🆔 User ID",
                               value=f"`{user_id}`",
                               inline=True)
    warn_log_message.add_field(name=" 🔒 Warned By",
                               value=f"{ctx.author.mention}",
                               inline=True)
    warn_log_message.add_field(name=" 🚫 Warn reason",
                               value=f"`{reason}`",
                               inline=True)
    warn_log_message.add_field(name=' 💿 Date of warn',
                               value=f"`{command_date}`",
                               inline=True)
    warn_log_message.set_author(name=ctx.author.name,
                                icon_url=ctx.author.avatar.url)
    warn_log_message.set_footer(
        text="Late Night  Verification Moderation",
        icon_url=
        'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
    )
    warn_log_message.set_thumbnail(
        url=
        "https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473"
    )
    await warn_log.send(embed=warn_log_message)

    warn_dm_message = Embed(title=" 📃 Warn Alert", color=Color.red())
    warn_dm_message.add_field(name=" 👤 Username",
                              value=f"`{user.display_name}`",
                              inline=True)
    warn_dm_message.add_field(name=" 🆔 User ID",
                              value=f"`{user_id}`",
                              inline=True)
    warn_dm_message.add_field(name=" 🔒 Warned By",
                              value=f"{ctx.author.mention}",
                              inline=True)
    warn_dm_message.add_field(name=" 🚫 Warn reason",
                              value=f"`{reason}`",
                              inline=True)
    warn_dm_message.add_field(name=' 💿 Date of warn',
                              value=f"`{command_date}`",
                              inline=True)
    warn_dm_message.set_author(name=ctx.author.name,
                               icon_url=ctx.author.avatar.url)
    warn_dm_message.set_footer(
        text=" Late Night   Moderation",
        icon_url=
        'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
    )
    warn_dm_message.set_thumbnail(
        url=
        "https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473"
    )
    warn_dm_message.set_image(
        url=
        "https://media.discordapp.net/attachments/1190408666705313822/1190422346998235156/GG.jpg?ex=65a1be34&is=658f4934&hm=7536064f023bca06e7321eee9fe7ffe641a21161d3e05de12f637137041f428d&=&format=webp&width=840&height=473"
    )

    await user.send(embed=warn_dm_message)

  # remove warn command
  @commands.command()
  async def removewarn(self, ctx, user_id: int = None):
    allowed_roles = [
        1183531782801477773, 1183524854285209721, 1183524811230674955,
        1183524776866754720, 1182822068568477766, 1183533552156020766,
        1183191058574745640, 1139268098906673324, 1123215434808827974,
        1068358173376909413, 1166376601131438140,         1168892055427240008
    ]
    if not any(role.id in allowed_roles for role in ctx.author.roles):
      await ctx.send("**You do not have permission to run this command**",
                     delete_after=15)
      return
    if user_id is None:
      await ctx.send(
          "I need an user id in order to run this command: `Syntax: +removewarn member.id`",
          delete_after=15)
      return
    user = ctx.guild.get_member(user_id)
    warn_log = ctx.guild.get_channel(1184599500006887485)
    if not warn_log:
      await ctx.send("⚠️log not found, please inform the developer")
      return
    if not user:
      await ctx.send("🤔No member with that id has been found", delete_after=10)
      return
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT reason FROM warn WHERE user = ?",
                           (user.id, ))
      data = await cursor.fetchone()
      if data:
        await cursor.execute("DELETE FROM warn WHERE user = ?", (user.id, ))
        await bot.db.commit()
        warn_embed = Embed(
            description=f"{user.mention}'s warnings has been cleared",
            color=Color.blue())
        warn_embed.set_author(name="Late Night   Moderation")
        await ctx.send(embed=warn_embed)
        warn_log_message = Embed(
            description=
            f"{user.mention}'s warnings has been cleared by {ctx.author.mention}",
            color=Color.blue())
        warn_log_message.set_author(name="Late Night  moderation",
                                    icon_url=bot.user.avatar.url)
        warn_log_message.set_footer(text="Deleted from the database")
        await warn_log.send(embed=warn_log_message)
      else:
        await ctx.send("This user does not have any warns", delete_after=15)
    await bot.db.commit()

  # warn list
  @commands.command()
  async def warns(self, ctx, user_id: int = None):
    allowed_roles = [
        1183531782801477773, 1183524854285209721, 1183524811230674955,
        1183524776866754720, 1182822068568477766, 1183533552156020766,
        1183191058574745640, 1139268098906673324, 1123215434808827974,
        1068358173376909413, 1166376601131438140,         1168892055427240008
    ]
    if not any(role.id in allowed_roles for role in ctx.author.roles):
      await ctx.send("**You do not have permission to run this command**",
                     delete_after=15)
      return
    if user_id is None:
      await ctx.send(
          "I need an user id and a reason in order to run this command: `Syntax: +warns member.id`",
          delete_after=15)
      return
    user = ctx.guild.get_member(user_id)
    async with self.bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM warn WHERE user = ?", (user.id, ))
      data = await cursor.fetchall()
      if data:
        warn_history = Embed(title=f"{user.name}'s warn history",
                             color=Color.blue())
        warn_history.set_author(name="Late Night   moderation")
        warn_history.set_thumbnail(
            url=
            "https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473"
        )
        warnum = 0
        for table in data:
          warnum += 1
          warn_history.add_field(name=f"Warn {warnum}",
                                 value=f"Reason: {table[1]}",
                                 inline=False)
        await ctx.send(embed=warn_history)
      else:
        await ctx.send("This user does not have any warns", delete_after=15)
    await self.bot.db.commit()


def setup(bot):
  bot.add_cog(warn(bot))
