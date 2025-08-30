import discord
from discord.ext import commands
import os
import random

# --- Setup Bot ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = 1406918069963460728  # Replace with your server ID


# --- Command Handlers ---
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"✅ Synced {len(synced)} commands")
    except Exception as e:
        print(f"❌ Sync failed: {e}")


# --- Fun Commands ---
@bot.tree.command(name="hello", description="Say hello to the bot!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"👋 Hello {interaction.user.mention}!")


@bot.tree.command(name="roll", description="Roll a dice (1-6).")
async def roll(interaction: discord.Interaction):
    number = random.randint(1, 6)
    await interaction.response.send_message(f"🎲 You rolled a **{number}**!")


@bot.tree.command(name="coinflip", description="Flip a coin.")
async def coinflip(interaction: discord.Interaction):
    result = random.choice(["Heads", "Tails"])
    await interaction.response.send_message(f"🪙 The coin landed on **{result}**!")


@bot.tree.command(name="say", description="Make the bot say something.")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)


@bot.tree.command(name="joke", description="Get a random joke.")
async def joke(interaction: discord.Interaction):
    jokes = [
        "Why don’t skeletons fight each other? Because they don’t have the guts.",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field.",
    ]
    await interaction.response.send_message(random.choice(jokes))


# --- Moderation Commands ---
@bot.tree.command(name="kick", description="Kick a member from the server")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👢 {member} was kicked. Reason: {reason}", ephemeral=True)


@bot.tree.command(name="ban", description="Ban a member from the server")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"🔨 {member} was banned. Reason: {reason}", ephemeral=True)


@bot.tree.command(name="unban", description="Unban a member")
async def unban(interaction: discord.Interaction, user_id: int):
    user = await bot.fetch_user(user_id)
    await interaction.guild.unban(user)
    await interaction.response.send_message(f"✅ {user} was unbanned.", ephemeral=True)


@bot.tree.command(name="clear", description="Clear messages in a channel")
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"🧹 Cleared {amount} messages!", ephemeral=True)


# --- Profile & Activity Commands ---
@bot.tree.command(name="setactivity", description="Change the bot's activity")
async def setactivity(interaction: discord.Interaction, activity: str):
    await bot.change_presence(activity=discord.Game(name=activity))
    await interaction.response.send_message(f"✅ Activity set to: {activity}", ephemeral=True)


@bot.tree.command(name="setnick", description="Change the bot's nickname in this server")
async def setnick(interaction: discord.Interaction, nickname: str):
    await interaction.guild.me.edit(nick=nickname)
    await interaction.response.send_message(f"✅ Nickname changed to: {nickname}", ephemeral=True)


@bot.tree.command(name="setavatar", description="Change the bot's avatar (paste an image URL)")
async def setavatar(interaction: discord.Interaction, url: str):
    async with bot.http._HTTPClient__session.get(url) as resp:
        if resp.status != 200:
            return await interaction.response.send_message("❌ Failed to fetch image.", ephemeral=True)
        data = await resp.read()
        await bot.user.edit(avatar=data)
        await interaction.response.send_message("✅ Avatar updated!", ephemeral=True)


# --- Run Bot ---
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ Bot token not found! Set it in Railway Variables.")

bot.run(TOKEN.strip())
