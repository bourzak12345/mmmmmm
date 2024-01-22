import nextcord
from nextcord.ext import commands
from nextcord import Color, Embed


class utility(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author is self.bot.user:
      return
    member = None
    if message.content.startswith("zA"):
      if message.mentions:
        member = message.mentions[0]
      else:
        member = message.author
      avatar = member.avatar.url

      embed = Embed(title=f"**{member.display_name}**", color=Color.random())
      embed.set_image(url=avatar)
      await message.channel.send(embed=embed)

  @commands.command()
  async def send_dm(self, ctx, user: nextcord.User = None, *, message=None):
    if not ctx.author.guild_permissions.administrator:

      await ctx.send("You do not have permission to run this command")
      return
    if user is None or message is None:
      await ctx.send("`+send_dm <user> <message>`")
    await ctx.message.delete()

    try:
      embed = nextcord.Embed(title='Notification',
                             description=f'{message}',
                             color=nextcord.Color.red())
      await user.send(embed=embed)
    except nextcord.Forbidden:
      await ctx.send("I don't have permission to send DMs to that user.")
    except Exception as e:
      await ctx.send(f"An error occurred: {e}")


def setup(bot):
  bot.add_cog(utility(bot))
