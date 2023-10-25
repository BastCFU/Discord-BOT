from discord.ext import commands
import discord
import random
from collections import defaultdict
from datetime import datetime, timedelta

user_messages = defaultdict(list)
flood_protection_active = False
X = 5
Y = timedelta(minutes=1)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=intents  # Set up basic permissions
)

bot.author_id = 691526952015626262  # Change to your Discord ID

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    user = ctx.message.author
    await ctx.send(f'{user.name}') 

@bot.command()
async def d6(ctx):
    result = random.randint(1, 6)
    await ctx.send(result)

@bot.event
async def on_message(message):
    if message.content == "Salut tout le monde":
        await message.channel.send(f"Salut tout seul <@{message.author.id}>")
    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def admin(ctx, *, member_nickname: discord.Member = None):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    if not admin_role:
        permissions = discord.Permissions(
            manage_channels=True,
            kick_members=True,
            ban_members=True
        )
        admin_role = await ctx.guild.create_role(name="Admin", permissions=permissions, reason="Admin role creation")
        await ctx.send("Admin role created.")

    await member_nickname.add_roles(admin_role)
    await ctx.send(f"{member_nickname.display_name} t'es admin quoiquoibeh")


reason = [
    "salut t'es ban paske t'es moche",
    "ban pourquoi ? parce que feur",
]

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if not reason:
        reason = random.choice(reason)
    try:
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.display_name} for reason: {reason}")
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command()
@commands.has_permissions(administrator=True)
async def flood(ctx):
    global flood_protection_active
    if flood_protection_active:
        flood_protection_active = False
        await ctx.send("Désactivation tutututu transformers")
    else:
        flood_protection_active = True
        await ctx.send("Activation tutututu transformers")


@bot.event
async def on_message(message):
    global flood_protection_active
    if flood_protection_active:
        current_time = datetime.now()
        user_messages[message.author.id].append(current_time)
        user_messages[message.author.id] = [
            t for t in user_messages[message.author.id] if current_time - t <= Y
        ]
        if len(user_messages[message.author.id]) > X:
            await message.channel.send(f"<@{message.author.id}> Please slow down your messages!")
    await bot.process_commands(message)
    

token = "MTE2Njc4NjQ3ODA1NjE1MzE3OA.GUMeAR.CXCUjvLkZW0YEGphPkIaEL72z8BkB3_Bmgc6D4"
bot.run(token)  # Starts the bot