from os import name
import nextcord
from nextcord.ext import commands
from nextcord import Embed, Color
from datetime import timedelta
import asyncio
import random


class giveaway(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.active_giveaways = {}

  async def end_giveaway(self, channel, reroll=False, message_id=None):
    if channel.id not in self.active_giveaways:
      return
    giveaway_info = self.active_giveaways[channel.id]
    if reroll and message_id:
        message_id = message_id
    else:
        message_id = giveaway_info["message_id"]
    prize = giveaway_info["prize"]

    message = await channel.fetch_message(message_id)
    reactions = [reaction for reaction in message.reactions if str(reaction.emoji) == "🎉"]
    participants = await reactions[0].users().flatten()
    bot_participated = self.bot.user in participants
    if bot_participated:
        participants.remove(self.bot.user)

    if len(participants) > 0:
        winner = random.choice(participants)
        await channel.send(f"🎉 Congratulations, {winner.mention}! You've won **{prize}**!")
    else:
        await channel.send(**"No one entered the giveaway. Better luck next time!**")

    del self.active_giveaways[channel.id]

  @commands.command()
  async def gstart(self, ctx, duration: int = None, prize: str = None):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("**You do not have permission to use this command.**")
        return
    if duration is None or prize is None:
      await ctx.send("**Syntax Error** try again: `+gstart duration (in minute) prize`")
      return
    if ctx.channel.id in self.active_giveaways:
      await ctx.send("**There's already an active giveaway in this channel.**")
      return

    giveaway_embed = Embed(title="Giveaway Started 🎉!", color=Color.random())
    giveaway_embed.set_author(name="Late Night   Giveaway", icon_url='https://images-ext-2.discordapp.net/external/FawhovT4g3hiJqWKlWiidbZ4Ln2kh1AztsBuB8RLXRA/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.webp?format=webp&width=473&height=473')
    giveaway_embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/FawhovT4g3hiJqWKlWiidbZ4Ln2kh1AztsBuB8RLXRA/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.webp?format=webp&width=473&height=473")
    giveaway_embed.add_field(name="Hosted By", value=ctx.author.mention, inline=False)
    giveaway_embed.add_field(name="Duration", value=f"{duration} minutes", inline=False)
    giveaway_embed.add_field(name="Prize", value=f"`{prize}`", inline=False)
    giveaway_embed.set_footer(text="🍸  Late Night   Community")
    message = await ctx.send(embed=giveaway_embed)
    await message.add_reaction("🎉")
    self.active_giveaways[ctx.channel.id] = {
        "message_id": message.id,
        "end_time": ctx.message.created_at + timedelta(seconds=duration),
        "prize": prize
    }
    await asyncio.sleep(duration*60)
    await self.end_giveaway(ctx.channel)
    
  @commands.command()
  async def greroll(self, ctx, giveaway_message_id: int = None):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You do not have permission to use this command.")
        return
    if giveaway_message_id is None:
      embed = Embed(description="You need to provide the message ID", color=Color.red())
      embed.set_image(url="https://media.discordapp.net/attachments/1190408666705313822/1190411011304476782/KILUA.jpg?ex=65a1b3a5&is=658f3ea5&hm=5146eeeecd1e64d70fee9bcd214d6f948d1a5a38b2ec5e05cac8b0a9e137f844&=&format=webp&width=840&height=473")
      await ctx.send(embed=embed)
      return
    if giveaway_message_id not in self.active_giveaways:
      await ctx.send("This is not a giveaway message ID.")
      return
    await self.end_giveaway(ctx.channel, reroll=True, message_id=giveaway_message_id)

  @commands.command()
  async def gend(self, ctx, giveaway_message_id: int = None):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You do not have permission to use this command.")
        return
    if giveaway_message_id is None:
      embed = Embed(description="You need to provide the message ID", color=Color.red())
      embed.set_image(url="https://media.discordapp.net/attachments/1190408666705313822/1190411011304476782/KILUA.jpg?ex=65a1b3a5&is=658f3ea5&hm=5146eeeecd1e64d70fee9bcd214d6f948d1a5a38b2ec5e05cac8b0a9e137f844&=&format=webp&width=840&height=473")
      await ctx.send(embed=embed)
      return
    if giveaway_message_id not in self.active_giveaways:
      await ctx.send("This is not a giveaway message ID.")
      return
    
    await self.end_giveaway(ctx.channel, message_id=giveaway_message_id)

def setup(bot):
  bot.add_cog(giveaway(bot))