import nextcord
from nextcord.ext import commands
from nextcord import Color, Embed
import datetime
import aiosqlite
import asyncio
from config import Config


class moderation(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    self.bot.db = await aiosqlite.connect('tokyo.db')
    await asyncio.sleep(3)
    print("jail database has been connected")
    async with self.bot.db.cursor() as cursor:
      await cursor.execute('''
                CREATE TABLE IF NOT EXISTS jailed_id (jailed_id INTEGER)''')
    await self.bot.db.commit()

  async def insert_jailed_member(self, member_id):
    async with aiosqlite.connect('tokyo.db') as db:
      await db.execute("INSERT INTO jailed_id (jailed_id) VALUES (?)",
                       (member_id, ))
      await db.commit()

  # Jail command
  @commands.command()
  async def jail(self, ctx, member_id: int = None, *, reason=None):
    allowed_roles = [
        1183531782801477773, 1183524854285209721, 1183524811230674955,
        1183524776866754720, 1182822068568477766, 1183533552156020766,
        1183191058574745640, 1139268098906673324, 1123215434808827974,
        1068358173376909413, 1166376601131438140,         1168892055427240008
    ]
    if not any(role.id in allowed_roles for role in ctx.author.roles):
      perm_error = Embed(description="**Maendkch Rolz bch t9ed Tjaili!**",
                         color=Color.red())
      await ctx.send(embed=perm_error, delete_after=15)
      return
    if member_id is None:
      await ctx.send("`+jail user.id reason`")
      return
    if reason is None:
      await ctx.send(
          "**Reason Required** please provide a reason | `+jail member.id reason`",
          delete_after=20)
      return
    jail_role = ctx.guild.get_role(1183191510871703552)
    jail_log = ctx.guild.get_channel(1183192040138342551)
    if not jail_role or not jail_log:
      await ctx.send("⚠️Role or log not found, Please inform the developer")
      return
    member = ctx.guild.get_member(member_id)
    if not member:
      await ctx.send("🤔No member with that id has been found", delete_after=10)
      return
    await member.edit(roles=[jail_role])
    jailed = Embed(
        description=
        f"{member.mention} has been successfully **jailed** by {ctx.author.mention} | reason: `{reason}`",
        color=Color.green())
    jailed.set_author(
        name="Late Night  Moderation",
        icon_url=
        'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
    )
    jailed.set_footer(text=f"{ctx.author.display_name}",
                      icon_url=ctx.author.avatar.url)
    await ctx.send(embed=jailed)

    command_date = datetime.datetime.now().strftime("%d/%m/%y")
    jail_log_message = Embed(title=" 📃 Jail Logs", color=Color.random())
    jail_log_message.add_field(name=" 👤 Username",
                               value=f"`{member.display_name}`",
                               inline=False)
    jail_log_message.add_field(name=" 🆔 User ID",
                               value=f"`{member_id}`",
                               inline=True)
    jail_log_message.add_field(name=" 📃 Reason",
                               value=f"`{reason}`",
                               inline=False)
    jail_log_message.add_field(name=' 💿 Date of jail',
                               value=f"`{command_date}`",
                               inline=False)
    jail_log_message.set_author(name=ctx.author.name,
                                icon_url=ctx.author.avatar.url)
    jail_log_message.set_footer(
        text="Late Night  Moderation",
        icon_url=
        'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
    )
    jail_log_message.set_thumbnail(
        url=
        "https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473"
    )
    await jail_log.send(embed=jail_log_message)
    user = ctx.guild.get_member(member_id)

    jail_dm_message = Embed(title=" 📃 Jail Alert:", color=Color.red())
    jail_dm_message.add_field(name=" 👤 Username",
                              value=f"`{user.display_name}`",
                              inline=True)
    jail_dm_message.add_field(name=" 🆔 User ID",
                              value=f"`{member_id}`",
                              inline=True)
    jail_dm_message.add_field(name=" 🚫 Jail reason",
                              value=f"`{reason}`",
                              inline=True)
    jail_dm_message.add_field(name=' 💿 Date of Jail',
                              value=f"`{command_date}`",
                              inline=True)
    jail_dm_message.add_field(
        name="' 🚧・Jailed",
        value=
        "[🚧・Jailed](https://ptb.discord.com/channels/1139968946536189963/1183192121835003925",
    )
    jail_dm_message.set_author(name=ctx.author.name,
                               icon_url=ctx.author.avatar.url)
    jail_dm_message.set_footer(
        text="Late Night  Moderation",
        icon_url=
        'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
    )
    jail_dm_message.set_thumbnail(
        url=
        "https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473"
    )
    jail_dm_message.set_image(
        url=
        "https://media.discordapp.net/attachments/1190408666705313822/1190416275491520542/LOSE_R.jpg?ex=65a1b88c&is=658f438c&hm=a96be789d636ddca54a9e39979c4c4f0322e0f7299818bb7270e01be5652e9a0&=&format=webp&width=840&height=473"
    )

    await user.send(embed=jail_dm_message)

    await self.insert_jailed_member(member.id)

  @commands.Cog.listener()
  async def on_member_join(self, member):
    async with aiosqlite.connect('tokyo.db') as db:
      cursor = await db.execute(
          "SELECT jailed_id FROM jailed_id WHERE jailed_id=?", (member.id, ))
      jailed_member = await cursor.fetchone()
      if jailed_member:
        jail_role = member.guild.get_role(1183191510871703552)
        if jail_role:
          await member.add_roles(jail_role)
        unverified = 1182822505094860831
        await member.remove_roles(unverified)

  # unjail db
  async def delete_jailed_member(self, member_id):
    async with aiosqlite.connect('tokyo.db') as db:
      await db.execute("DELETE FROM jailed_id WHERE jailed_id=?",
                       (member_id, ))
      await db.commit()

  # unjail command

  @commands.command()
  async def unjail(self, ctx, member_id: int = None):
    allowed_roles = [
        1183531782801477773, 1183524854285209721, 1183524811230674955,
        1183524776866754720, 1182822068568477766, 1183533552156020766,
        1183191058574745640, 1139268098906673324, 1123215434808827974,
        1068358173376909413, 1166376601131438140,         1168892055427240008
    ]
    if not any(role.id in allowed_roles for role in ctx.author.roles):
      perm_error = Embed(
          description="You do not have permission to run this command",
          color=Color.red())
      perm_error.set_author(
          name='Permission Error',
          icon_url=
          'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
      )
      perm_error.set_footer(
          text="Moderation Only Command",
          icon_url=
          'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
      )
      await ctx.send(embed=perm_error, delete_after=15)
      return
    if member_id is None:
      await ctx.send("`+unjail user.id`")
      return
    jail_role = ctx.guild.get_role(1183191510871703552)
    verified_role = ctx.guild.get_role(1182819201128353863)
    jail_log = ctx.guild.get_channel(1183192040138342551)
    if not jail_role or not jail_log or not verified_role:
      await ctx.send("⚠️Role or log not found, please inform the developer")
      return
    member = ctx.guild.get_member(member_id)
    if not member:
      await ctx.send("**🤔No member with that id has been found**",
                     delete_after=10)
      return
    if jail_role in member.roles:
      await member.remove_roles(jail_role)
      await member.add_roles(verified_role)
      embed = Embed(
          description=
          f"{member.mention} has been removed from jail by {ctx.author.mention}",
          color=Color.green())
      embed.set_author(
          name="Late Night  Moderation",
          icon_url=
          'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
      )
      embed.set_footer(text=f"{ctx.author.display_name}",
                       icon_url=ctx.author.avatar.url)
      await ctx.send(embed=embed)
      await self.delete_jailed_member(member.id)
      jail_log_message = Embed(title=" 📃 Unjail Logs", color=Color.random())
      jail_log_message.add_field(name=" 👤 Username",
                                 value=f"`{member.display_name}`",
                                 inline=True)
      jail_log_message.add_field(name=" 🆔 User ID",
                                 value=f"`{member_id}`",
                                 inline=True)
      jail_log_message.add_field(name=" 🔓 Unjailed By",
                                 value=f"{ctx.author.mention}",
                                 inline=False)
      jail_log_message.set_author(name=ctx.author.name,
                                  icon_url=ctx.author.avatar.url)
      jail_log_message.set_footer(
          text="Late Night  Moderation",
          icon_url=
          'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
      )
      jail_log_message.set_thumbnail(
          url=
          "https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473"
      )
      await jail_log.send(embed=jail_log_message)
    else:
      await ctx.send(f"**{member.mention} is already out of jail 🔓**")
    member = ctx.guild.get_member(member_id)
    jail_dm_message = Embed(title=" 📃 Unjail Alert:", color=Color.red())
    jail_dm_message.add_field(name=" 👤 Username",
                              value=f"`{member.display_name}`",
                              inline=True)
    jail_dm_message.add_field(name=" 🆔 User ID",
                              value=f"`{member_id}`",
                              inline=True)
    jail_dm_message.add_field(name=" 🔓 Unjailed By",
                              value=f"{ctx.author.mention}",
                              inline=True)
    jail_dm_message.add_field(
        name="You have been Successfully unjailed in Late Night  community",
        value="Welcome Back",
        inline=True)
    jail_dm_message.set_footer(
        text="Late Night  Moderation",
        icon_url=
        'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
    )
    jail_dm_message.set_thumbnail(
        url=
        "https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473"
    )
    jail_dm_message.set_image(
        url=
        "https://media.discordapp.net/attachments/1190408666705313822/1190411011304476782/KILUA.jpg?ex=65a1b3a5&is=658f3ea5&hm=5146eeeecd1e64d70fee9bcd214d6f948d1a5a38b2ec5e05cac8b0a9e137f844&=&format=webp&width=840&height=473"
    )

    await member.send(embed=jail_dm_message)


# ban commund

  @commands.command()
  async def ban(self, ctx, member_id: int = None, *, reason=None):
    allowed_roles = [
        1183531782801477773, 1183524854285209721, 1183524811230674955,
        1183524776866754720, 1182822068568477766, 1183533552156020766,
        1183191058574745640, 1139268098906673324, 1123215434808827974,
        1068358173376909413, 1166376601131438140,         1168892055427240008
    ]
    if not any(role.id in allowed_roles for role in ctx.author.roles):
      perm_error = Embed(description="**Required Perm**", color=Color.red())
      perm_error.set_footer(
          text="**Admin Only Command**",
          icon_url=
          'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
      )
      await ctx.send(embed=perm_error, delete_after=15)
      return
    if member_id is None:
      await ctx.send("`Please specify a member id`", delete_after=10)
      return
    if reason is None:
      await ctx.send(
          "**Reason Required** please provide a reason | `+ban member.id reason`",
          delete_after=20)
      return

    member = ctx.guild.get_member(member_id)

    try:
      msg_dm = Embed(
          title="Moderation Mail",
          description=
          f"You have been banned from **Late Night   Community** for `{reason}`",
          color=Color.red())
      msg_dm.set_image(
          url=
          "https://media.discordapp.net/attachments/1190408666705313822/1190425600465318028/c2a351509060e23d.jpg?ex=65a1c13c&is=658f4c3c&hm=15c12f959d103de668d17d6373fbb83093736f39e53ab36d76f115a77299bb53&=&format=webp&width=840&height=473"
      )
      msg_dm.set_thumbnail(
          url=
          "https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473"
      )

      await member.send(embed=msg_dm)
    except nextcord.errors.Forbidden:
      pass

    await member.ban(reason=reason)
    ban_message = Embed(
        description=
        f"{member.mention} has been banned by {ctx.author.mention} for `{reason}`",
        color=Color.random())
    ban_message.set_footer(text=ctx.author.name,
                           icon_url=ctx.author.avatar.url)
    await ctx.send(embed=ban_message)

    log_message = Embed(title=" 📃 Ban Logs", color=Color.red())
    log_message.set_thumbnail(
        url=
        "https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473"
    )
    log_message.add_field(name=" 👤 Banned User",
                          value=f"`{member.display_name}`",
                          inline=True)
    log_message.add_field(name=" 🔨 Banned By",
                          value=f"{ctx.author.mention}",
                          inline=False)
    log_message.add_field(name=' 💿 Reason', value=f"`{reason}`", inline=False)
    log_message.set_author(name=ctx.author.name,
                           icon_url=ctx.author.avatar.url)
    log_message.set_footer(
        text="Ban Log",
        icon_url=
        'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
    )
    ban_log = nextcord.utils.get(ctx.guild.text_channels, name="📃・bans")
    await ban_log.send(embed=log_message)

  # unban command
  @commands.command()
  async def unban(self, ctx, user_id: int = None):
    allowed_roles = [
        1183531782801477773, 1183524854285209721, 1183524811230674955,
        1183524776866754720, 1182822068568477766, 1183533552156020766,
        1183191058574745640, 1139268098906673324, 1123215434808827974,
        1068358173376909413, 1166376601131438140,         1168892055427240008
    ]
    if not any(role.id in allowed_roles for role in ctx.author.roles):
      perm_error = Embed(
          description="You do not have permission to run this command",
          color=Color.red())
      perm_error.set_author(
          name='Permission Error',
          icon_url=
          'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
      )
      perm_error.set_footer(
          text="Moderation Only Command",
          icon_url=
          'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
      )
      await ctx.send(embed=perm_error, delete_after=15)
      return

    if user_id is None:
      await ctx.send("`+unban user.id`")
      return
    try:
      user = await self.bot.fetch_user(user_id)
      if user:
        await ctx.guild.unban(user)
        unban_message = Embed(
            description=
            f"User with ID `{user_id}` has been unbanned by {ctx.author.mention}",
            color=Color.green())
        unban_message.set_footer(text=f"{ctx.author.display_name}",
                                 icon_url=ctx.author.avatar.url)
        await ctx.send(embed=unban_message)

        log_message = Embed(title=" 📃 Unban Logs", color=Color.green())
        log_message.set_thumbnail(
            url=
            "https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473"
        )
        log_message.add_field(name=" 🆔 Unbanned User ID",
                              value=f"`{user_id}`",
                              inline=True)
        log_message.add_field(name=" 🔨 Unbanned By",
                              value=f"{ctx.author.mention}",
                              inline=True)
        log_message.set_author(name=ctx.author.name,
                               icon_url=ctx.author.avatar.url)
        log_message.set_footer(
            text="Unban Log",
            icon_url=
            'https://images-ext-2.discordapp.net/external/pTMYj2IaPHX9UBZeWqA7gl24rR368XuZNP0OZDmIT8U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1182791297958952983/900b00142af7b9347ff73dd03f2866ce.png?format=webp&quality=lossless&width=473&height=473'
        )
        log_channel = nextcord.utils.get(ctx.guild.text_channels,
                                         name="📃・unbans")
        await log_channel.send(embed=log_message)
      else:
        await ctx.send("🤔 User with that ID does not exist.", delete_after=10)
    except nextcord.errors.NotFound:
      await ctx.send(
          "⚠️ User with that ID is not found in this server or not banned.",
          delete_after=10)


def setup(bot):
  bot.add_cog(moderation(bot))
