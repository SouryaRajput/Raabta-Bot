import discord
from discord.ext import commands
import datetime
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="r!", intents=intents)

TOKEN = "MTIyMjQ2OTYwMzM2MDI0NzkwMA.G0wKv5.f1dLFOF-EXnG61adUYgXn14Q1CygXZAIAV_xm8"


#auto response
@bot.event
async def on_ready():
  print("The Bot Is Now Online!")


def load_auto_responses():
  with open("autoresponse.json", "r") as file:
    return json.load(file)


def save_auto_responses(auto_responses):
  with open("autoresponse.json", "w") as file:
    json.dump(auto_responses, file, indent=4)


#set auto response
@bot.command()
async def set_autoresponse(ctx, trigger, *, response):
  auto_responses = load_auto_responses()
  auto_responses[trigger.lower()] = response
  save_auto_responses(auto_responses)
  await ctx.send(f"Auto-response for '{trigger}' set to: {response}")


#remove auto response
@bot.command()
async def remove_auto_response(ctx, keyword):
  auto_responses = load_auto_responses()
  if keyword.lower() in auto_responses:
    del auto_responses[keyword.lower()]
    save_auto_responses(auto_responses)
    await ctx.send(f"Auto-response for '{keyword}' removed.")
  else:
    await ctx.send(f"No auto-response found for '{keyword}'.")


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  auto_responses = load_auto_responses()
  for keyword, response in auto_responses.items():
    if keyword in message.content.lower():
      await message.channel.send(response)
      break
  await bot.process_commands(message)


#===============================================================


#auto Delete Messages
# Load auto delete keywords from JSON file
def load_auto_delete_keywords():
  with open("auto_delete.json", "r") as file:
    return json.load(file)


# Save auto delete keywords to JSON file
def save_auto_delete_keywords(auto_delete_keywords):
  with open("auto_delete.json", "w") as file:
    json.dump(auto_delete_keywords, file, indent=4)


@bot.command()
async def set_auto_delete(ctx, keyword):
  auto_delete_keywords = load_auto_delete_keywords()
  if keyword.lower() not in auto_delete_keywords:
    auto_delete_keywords.append(keyword.lower())
    save_auto_delete_keywords(auto_delete_keywords)
    await ctx.send(f"Auto-delete for '{keyword}' enabled.")
  else:
    await ctx.send(f"Auto-delete for '{keyword}' is already enabled.")


# Command to remove auto-delete keyword
@bot.command()
async def remove_auto_delete(ctx, keyword):
  auto_delete_keywords = load_auto_delete_keywords()
  if keyword.lower() in auto_delete_keywords:
    auto_delete_keywords.remove(keyword.lower())
    save_auto_delete_keywords(auto_delete_keywords)
    await ctx.send(f"Auto-delete for '{keyword}' disabled.")
  else:
    await ctx.send(f"Auto-delete for '{keyword}' is not enabled.")


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  auto_delete_keywords = load_auto_delete_keywords()
  for keyword in auto_delete_keywords:
    if keyword in message.content.lower():
      await message.delete()
      break

  await bot.process_commands(message)


#===============================================================


#main bot commands
#ban command
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
  if reason is None:
    reason = "No Reason Provided"
  await ctx.guild.ban(member, reason=reason)
  await ctx.send(f"{member.mention} has been banned for {reason}")
  await ctx.send_dm(f"You have been banned from {ctx.guild.name} for {reason}")


#unban command
@bot.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split("#")
  for ban_entry in banned_users:
    user = ban_entry.user
    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f"{user.mention} has been unbanned.")
      await ctx.send_dm(f"You have been unbanned from {ctx.guild.name}.")
      return


#kick command
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
  if reason is None:
    reason = "No Reason Provided"
  await ctx.guild.kick(member, reason=reason)
  await ctx.send(f"{member.mention} has been kicked for {reason}")
  await ctx.send_dm(f"You have been kicked from {ctx.guild.name} for {reason}")


#mute command
#second mute
@bot.command()
async def mute(ctx, member: discord.Member, timelimit):
  if "s" in timelimit:
    gettime = timelimit.strip("s")
    if int(gettime) > 2419000:
      await ctx.send("The Mute Time Amount Cannot Be Bigger Than 28 Days!")
    else:
      newtime = datetime.timedelta(seconds=int(gettime))
      await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
      await ctx.send(
          f"{member.mention} has been muted for {str(gettime)} seconds!")
      await ctx.send_dm(
          f"You have been muted in {ctx.guild.name} for {str(gettime)} seconds!"
      )

#minute mute
  elif "m" in timelimit:
    gettime = timelimit.strip("m")
    if int(gettime) > 40320:
      await ctx.send("The Mute Time Amount Cannot Be Bigger Than 28 Days!")
  else:
    newtime = datetime.timedelta(minutes=int(gettime))
    await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    await ctx.send(
        f"{member.mention} has been muted for {str(gettime)} minutes!")
    await ctx.send_dm(
        f"You have been muted in {ctx.guild.name} for {str(gettime)} minutes!")
#hour mute
  if "h" in timelimit:
    gettime = timelimit.strip("h")
    if int(gettime) > 672:
      await ctx.send("The Mute Time Amount Cannot Be Bigger Than 28 Days!")
    else:
      newtime = datetime.timedelta(hours=int(gettime))
  else:
    newtime = datetime.timedelta(hours=int(gettime))
    await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    await ctx.send(f"{member.mention} has been muted for {str(gettime)} hours!"
                   )
    await ctx.send_dm(
        f"You have been muted in {ctx.guild.name} for {str(gettime)} hours!")

#day mute
  if "d" in timelimit:
    gettime = timelimit.strip("d")
    if int(gettime) > 28:
      await ctx.send("The Mute Time Amount Cannot Be Bigger Than 28 Days!")
  else:
    newtime = datetime.timedelta(days=int(gettime))
    await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    await ctx.send(f"{member.mention} has been muted for {str(gettime)} days!")
    await ctx.send_dm(
        f"You have been muted in {ctx.guild.name} for {str(gettime)} days!")


#unmute command
@bot.command()
async def unmute(ctx, member: discord.Member):
  await member.edit(timed_out_until=None)
  await ctx.send(f"{member.mention} has been unmuted")
  await ctx.send_dm(f"You have been unmuted in {ctx.guild.name}")


#welcome command
#set welcome channel
welcome_channels = {}


@bot.command()
async def set_welcome_channel(ctx, channel: discord.TextChannel):
  welcome_channels[ctx.guild.id] = channel
  await ctx.send(f"Welcome channel set to {channel.mention}")


welcome_message = None


#set welcome message
@bot.command()
async def set_welcome_message(ctx, *, message: str):
  global welcome_message
  welcome_message = message
  await ctx.send("Welcome message has been updated.")


#welcome msg
@bot.event
async def on_member_join(member):
  welcome_channel = discord.utils.get(member.guild.channels, name='welcome')
  welcome_message = "Welcome {0.mention} to the server!"

  if welcome_channel:
    await welcome_channel.send(welcome_message.format(member))


#role add command
@bot.command()
async def role_add(ctx, member: discord.Member, role: discord.Role):
  await member.add_roles(role)
  await ctx.send(f"{member.mention} has been given the {role.name} role.")


#role remove command
@bot.command()
async def role_remove(ctx, member: discord.Member, role: discord.Role):
  await member.remove_roles(role)
  await ctx.send(
      f"{member.mention} has been removed from the {role.name} role.")


#join dm
@bot.command()
async def set_join_message(ctx, *, message: str):
  global join_message
  join_message = message
  await ctx.send("Join message has been updated.")


#leave dm
@bot.command()
async def set_leave_message(ctx, *, message: str):
  global leave_message
  leave_message = message
  await ctx.send("Leave message has been updated.")


#ticket command
#set ticket message
@bot.command()
async def set_ticket_message(ctx, *, message: str):
  global ticket_message
  ticket_message = message
  await ctx.send("Ticket message has been updated.")

  #ticket category command
  @bot.command()
  async def set_ticket_category(ctx, category: discord.CategoryChannel):
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name="Tickets")
    if not category:
      category = await guild.create_category("Tickets")
    ticket_channel = await guild.create_text_channel(
        f"ticket-{ctx.author.name}", category=category)


#ticket channel
@bot.command()
async def set_ticket_channel(ctx, channel: discord.TextChannel):
  global ticket_channel
  ticket_channel = channel
  await ctx.send(f"Ticket channel set to {channel.mention}")


#ticket log channel
@bot.command()
async def set_ticket_log_channel(ctx, channel: discord.TextChannel):
  global ticket_log_channel
  ticket_log_channel = channel
  guild = ctx.guild
  channel = discord.utils.get(guild.channels, name="ticket-logs")
  if not channel:
    channel = await guild.create_text_channel("ticket-logs")
  await ctx.send(f"Ticket log channel set to {channel.mention}")


#ticket message
@bot.command()
async def ticket(ctx):
  ticket_message = "Thank you for contacting support!"
  "\nPlease describe your issue in detail and a member of our team will be with you shortly."
  embed = discord.Embed(title="Ticket",
                        description=ticket_message,
                        color=0x00ff00)
  embed.set_footer(text="Support Team")

  await ctx.send(embed=embed)


bot.run(TOKEN)
