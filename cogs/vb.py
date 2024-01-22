import nextcord
from nextcord import Embed, Color
from nextcord.ext import commands
import random
import aiosqlite
import asyncio
import datetime
from contextlib import suppress


class vb(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    try:
      self.bot.db = await aiosqlite.connect('tokyo.db')
    except aiosqlite.OperationalError as e:
      print(f"Error connecting to the database: {e}")
      return
    await asyncio.sleep(3)
    async with self.bot.db.cursor() as cursor:
      await cursor.execute(
          "CREATE TABLE IF NOT EXISTS verification(admin_id INTEGER, count INTEGER DEFAULT 0)"
      )
    await self.bot.db.commit()
    print("verification list database has been connected")

  # verification boys
  @commands.command(administrator=True)
  @commands.has_permissions()
  async def vb(self, ctx, user_id: int = None):
    allowed_roles = [
        1183531782801477773, 1183524854285209721, 1183524811230674955,
        1183524776866754720, 1182822068568477766, 1183533552156020766,
        1183191058574745640, 1139268098906673324, 1123215434808827974,
        1068358173376909413, 1166376601131438140,         1168892055427240008
    ]

    if not any(role.id in allowed_roles for role in ctx.author.roles):
      perm_error = Embed(
          description="**Maendkch Role a Sat Bch t9ed Tverify**",
          color=Color.red())
      await ctx.send(embed=perm_error, delete_after=15)
      return
    if user_id is None:
      usererror = Embed(description="User?", color=Color.red())
      await ctx.send(embed=usererror)
      return

    verified = 1182819201128353863
    role = nextcord.utils.get(ctx.guild.roles, id=verified)
    unverified = 1182822505094860831
    role_unverified = nextcord.utils.get(ctx.guild.roles, id=unverified)

    if role is None:
      error = Embed(
          title="Error",
          description=
          f'❗❗❓ Role **Verified** is not found, Report this error to the developer',
          color=Color.red())
      error.set_author(name="Command Error", icon_url=self.bot.user.avatar.url)
      error.set_footer(text="Late Night  Verification",
                       icon_url=self.bot.user.avatar.url)
      await ctx.send(embed=error)

    user = ctx.guild.get_member(user_id)

    if not user:
      usererror = Embed(description="**User not found on this server**",
                        color=Color.red())
      await ctx.send(embed=usererror)
      return

    if role in user.roles:
      embed = Embed(
          description=f"**{user.display_name}** is **already verified**",
          color=Color.red())
      embed.set_author(name="Failed to Verify")
      embed.set_footer(text="Late Night  Verification", icon_url=user.avatar.url)
      await ctx.send(embed=embed, delete_after=20)
      return

    else:
      if role_unverified in user.roles:
        await user.remove_roles(role_unverified)
      await user.add_roles(role)
      vf_message = Embed(
          description=f" ✅ **{user.display_name}** has been verified ",
          color=Color.green())
      vf_message.set_author(name="Moderation Mail")
      vf_message.set_footer(text=f"Verified by: {ctx.author.display_name}",
                            icon_url=ctx.author.avatar.url)
      await ctx.send(embed=vf_message)

      command_date = datetime.datetime.now().strftime("%d/%m/%y")
      joined_at = user.joined_at.strftime("%d/%m/%y")

      verification_log_channel = nextcord.utils.get(ctx.guild.text_channels,
                                                    name="📰・verification-logs")
      if verification_log_channel:
        verification_log_message = Embed(title=" 📃 Verification Logs",
                                         color=Color.random())
        verification_log_message.add_field(name=" 👤 Username",
                                           value=f"`{user.display_name}`",
                                           inline=True)
        verification_log_message.add_field(name=" 🆔 User ID",
                                           value=f"`{user_id}`",
                                           inline=True)
        verification_log_message.add_field(name=" 👥 Date of joining",
                                           value=f"`{joined_at}`",
                                           inline=True)
        verification_log_message.add_field(name=" ✅ Verified By",
                                           value=f"{ctx.author.mention}",
                                           inline=False)
        verification_log_message.add_field(name=' 💿 Date of verification',
                                           value=f"`{command_date}`",
                                           inline=False)
        verification_log_message.set_author(name=ctx.author.name,
                                            icon_url=ctx.author.avatar.url)
        verification_log_message.set_thumbnail(
            url=
            "https://images-ext-2.discordapp.net/external/FawhovT4g3hiJqWKlWiidbZ4Ln2kh1AztsBuB8RLXRA/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.webp?format=webp&width=473&height=473"
        )
        await verification_log_channel.send(embed=verification_log_message)

      dm_vf_message = Embed(
          description=
          f"🎉Congratulations🎉\n You are now **Verified**✅ in **{ctx.guild.name}** by {ctx.author.mention}!!\n ✨Hope you have fun with us!✨",
          color=Color.purple())
      dm_vf_message.set_author(name=f"           {ctx.guild.name}")
      dm_vf_message.set_image(
          url=
          "https://media.discordapp.net/attachments/1190408666705313822/1190408891587100693/welcome.jpg?ex=65a1b1ac&is=658f3cac&hm=0179559875520fca9f39d85fc407f25a879e265aaab038e127b5e64bec29fefd&=&format=webp&width=840&height=473"
      )
      dm_vf_message.set_thumbnail(
          url=
          "https://images-ext-2.discordapp.net/external/FawhovT4g3hiJqWKlWiidbZ4Ln2kh1AztsBuB8RLXRA/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.webp?format=webp&width=473&height=473"
      )

      dm_vf_message.set_footer(text="Late Night  Verification")
      with suppress(nextcord.Forbidden):
        await user.send(embed=dm_vf_message)


def setup(bot):
  bot.add_cog(vb(bot))
