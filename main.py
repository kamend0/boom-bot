import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import environ
import time

env = environ.Env()
environ.Env.read_env()

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!!', intents = intents)


@client.event
async def on_ready():
    print("\nBot launched successfully!\n")

@client.event
async def on_voice_state_update(member, before, after):
    if member.name == "boom-bot":
        return
    else:
        if not before.channel and after.channel:
            source = FFmpegPCMAudio('comedy-sound.mp3')
            voice.play(source)

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        global voice
        voice = await channel.connect()        
    else:
        await ctx.send(ctx.author.name + ": You have to join a voice channel first.")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        # await ctx.send("Left the voice channel.")
    else:
        await ctx.send(ctx.author.name + ": I'm not in a voice channel.")


client.run(env("DISCORD_TOKEN"))