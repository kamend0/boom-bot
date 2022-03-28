import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import environ
import random
from aliases import * # Contains dict of discord name:alias lookups
from gtts import gTTS

env = environ.Env()
environ.Env.read_env()

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!!', intents = intents)

announcementFileName = "tempAnnouncement.mp3"

sound_files = ['comedy-sound.mp3', 'bruh.mp3', 'aughhh.mp3']
sound_file_commands = ['boom', 'bruh', 'augh']
sounds = dict(zip(sound_file_commands, sound_files))

meme_mode = True


### EVNET HANDLING ###

@client.event
async def on_ready():
    print("\nBot launched successfully!\n")

@client.event
async def on_voice_state_update(member, before, after):
    if member.name == "boom-bot":
        return

    if not before.channel and after.channel:
        if meme_mode:
            voice.play(FFmpegPCMAudio(random.choice(sound_files)))
        else:
            try:
                name_of_who_joined = aliases[member.name]
            except:
                name_of_who_joined = member.name

            announcement_message = "..." + name_of_who_joined + " joined."

            try:
                gTTS(text = announcement_message,
                    lang = 'en',
                    slow = True).save(announcementFileName)
                source = FFmpegPCMAudio(announcementFileName)
                voice.play(source)
            except Exception as e:
                print('\n!!! ' + '-'*100 + ' !!!' +
                    "\nSome error with TTS process occurred. See exception text below.\n" +
                    '!!! ' + '-'*100 + ' !!!' +
                    '\n\n' + str(e) + '\n\n' +
                    '!!! ' + '-'*100 + ' !!!\n')


### COMMANDS ###

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        global voice
        voice = await channel.connect()
        await ctx.send("Bot is set to play stupid sounds.")     
    else:
        await ctx.send(ctx.author.name + ": You have to join a voice channel first.")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send(ctx.author.name + ": I'm not in a voice channel.")

@client.command(pass_context = True)
async def toggleUseful(ctx):
    global meme_mode
    meme_mode = not meme_mode
    if meme_mode:
        await ctx.send("Bot will play stupid sounds.")
    else:
        await ctx.send("Bot will be useful and announce who joined VC.")

@client.command(pass_context = True)
async def isUseful(ctx):
    if meme_mode:
        await ctx.send("Bot is set to play stupid sounds.")
    else:
        await ctx.send("Bot is set to be useful.")

@client.command(pass_context = True)
async def play(ctx, arg):
    if (ctx.voice_client):
        if arg.lower() == "any":
            voice.play(FFmpegPCMAudio(random.choice(sound_files)))
        else:
            try:
                voice.play(FFmpegPCMAudio(sounds[arg]))
            except:
                await ctx.send(ctx.author.name + ": I don't have that sound. Current options:" + 
                                '\n' + ', '.join(sound_file_commands) + ", or 'any' for a random one.")
    else:
        await ctx.send(ctx.author.name + ": I'm not in a voice channel.")


client.run(env("DISCORD_TOKEN"))