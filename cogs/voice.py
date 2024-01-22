import nextcord
from nextcord.ext import commands
import asyncio


class voice(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def join(self, ctx):
    role = nextcord.utils.get(ctx.author.roles, id=398609805004111873)
    if not role:
      await ctx.reply("**You do not have permission to run this command**",
                      delete_after=15)
      return
    if ctx.author.voice and ctx.author.voice.channel:
      channel = ctx.author.voice.channel
      await channel.connect()
      while True:
        await asyncio.sleep(0)
    else:
      await ctx.send("**You are not in a voice channel.**", delete_after=15)
      return


def setup(bot):
  bot.add_cog(voice(bot))
