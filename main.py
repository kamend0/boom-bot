from audioop import tostereo
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import environ
import random
from aliases import * # Contains dict of discord name:alias lookups
# from sounds import * # Contains dict of command:filename sound lookups
from gtts import gTTS
import os


env = environ.Env()
environ.Env.read_env()

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!!', intents = intents)

announcementFileName = "tempAnnouncement.mp3"

sounds_dir = "./sounds/"
sound_files = [f for f in os.listdir(sounds_dir) if '.mp3' in f]
sound_file_commands = [sf.replace('.mp3', '') for sf in sound_files]

# bot_modes = ["announcer", "random", "sound"]
global bot_mode
bot_mode = "announcer"
global announce_sound
announce_sound = "boom.mp3"

help_message = """
    Boom bot plays sounds. Commands:
    !!join - join the voice channel you are in.
    !!leave - leave whatever voice channel the bot is in.
    !!play sound - where "sound" is an available sound clip.
    !!sounds - show available sound clips.
    !!toggleUseful - switch between bot playing random meme sound when someone joins chat, and their name/alias.
    !!isUseful - is the bot announcing people's names that join chat?
    !!say "text" - say the text you provide.
"""


##### EVENT HANDLING #####

@client.event
async def on_ready():
    print('-'*100 + "\nBot launched successfully!\n" + '-'*100)

@client.event
async def on_voice_state_update(member, before, after):
    if member.name == "boom-bot" or not voice:
        return

    # Play sound if user connects to VC, or joins channel bot is in from another
    if (not before.channel and after.channel) or \
        ((before.channel != after.channel) and \
            after.channel == channel):
        if (bot_mode == "announcer"):
            voice.play(FFmpegPCMAudio(sounds_dir + random.choice(sound_files)))
        else:
            try:
                name_of_who_joined = aliases[member.name]
            except:
                name_of_who_joined = member.name
            
            # Voice clip often jumps the gun, so add in a pause at the beginning
            announcement_message = "......" + name_of_who_joined + " joined voice chat"

            try:
                gTTS(text = announcement_message,
                    lang = 'en',
                    slow = False).save(announcementFileName)
                source = FFmpegPCMAudio(announcementFileName)
                voice.play(source)
            except Exception as e:
                print('\n!!! ' + '-'*100 + ' !!!' +
                    "\nSome error with TTS process occurred. See exception text below.\n" +
                    '!!! ' + '-'*100 + ' !!!' +
                    '\n\n' + str(e) + '\n\n' +
                    '!!! ' + '-'*100 + ' !!!\n')


##### COMMANDS #####

@client.command(pass_context = True)
async def join(ctx):
    global channel
    global voice

    # Switching channels
    try:
        if voice and (channel != ctx.message.author.voice.channel):
            await ctx.guild.voice_client.disconnect()
            # global channel
            channel = ctx.message.author.voice.channel
            # global voice
            voice = await channel.connect()
        elif (channel == ctx.message.author.voice.channel):
            await ctx.send(ctx.author.name + ": I'm already in your voice channel.")
        # Left previously, now returning
        else:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            if bot_mode == "random":
                await ctx.send("Bot is set to play random stupid sounds.")
            elif bot_mode == "sound":
                await ctx.send("Bot is set to play '", + announce_sound, "' when someone enters VC.")
            else:
                await ctx.send("Bot is set to be useful and announce who joined VC.")
    # Initial join
    except:
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            if bot_mode == "random":
                await ctx.send("Bot is set to play random stupid sounds.")
            elif bot_mode == "sound":
                await ctx.send("Bot is set to play '", + announce_sound, "' when someone enters VC.")
            else:
                await ctx.send("Bot is set to be useful and announce who joined VC.")
        else:
            await ctx.send(ctx.author.name + ": You have to join a voice channel first.")

@client.command(pass_context = True)
async def leave(ctx):
    global channel
    global voice

    if (voice):
        await ctx.guild.voice_client.disconnect()
        channel = False
        voice = False
    else:
        await ctx.send(ctx.author.name + ": I'm not in a voice channel.")

@client.command(pass_context = True)
async def sounds(ctx):
    await ctx.send("Available sounds (type \"!!play sound\"):\n" + ', '.join(sound_file_commands))

# @client.command(pass_context = True)
# async def toggleUseful(ctx):
#     global meme_mode
#     meme_mode = not meme_mode
#     if meme_mode:
#         await ctx.send("Bot will play stupid sounds.")
#     else:
#         await ctx.send("Bot will be useful and announce who joined VC.")

# @client.command(pass_context = True)
# async def isUseful(ctx):
#     if meme_mode:
#         await ctx.send("Bot is set to play stupid sounds.")
#     else:
#         await ctx.send("Bot is set to be useful.")

@client.command(pass_context = True)
async def helpme(ctx):
    await ctx.send(help_message)

@client.command(pass_context = True)
async def set(ctx, arg):
    global bot_mode
    global announce_sound

    if (arg.lower() in ["announcer", "random"]):
        bot_mode = arg.lower()
        await ctx.send("Bot set to " + bot_mode + " mode.")
    elif (arg.lower() in sound_file_commands):
        bot_mode = "sound"
        announce_sound = arg.lower() + ".mp3"
        await ctx.send("Bot set to play " + announce_sound + " when someone joins VC.")

@client.command(pass_context = True)
async def status(ctx):
    if (bot_mode in ["announcer", "random"]):
        await ctx.send("Bot is set to " + bot_mode + " mode.")
    elif (bot_mode in sound_file_commands):
        await ctx.send("Bot set to play " + announce_sound + " when someone joins VC.")
    else:
        await ctx.send("Something is wrong, tell Kollin.")

@client.command(pass_context = True)
async def say(ctx, args):
    try:
        gTTS(text = args,
            lang = 'en',
            slow = True).save(announcementFileName)
        source = FFmpegPCMAudio(announcementFileName)
        voice.play(source)
    except:
        await ctx.send(ctx.author.name + ": Sorry, something went wrong. Please try again, or tell Kollin to fix me.")

@client.command(pass_context = True)
async def play(ctx, arg):
    if (ctx.voice_client):
        if (channel != ctx.message.author.voice.channel):
            await ctx.send(ctx.author.name + ": I'm not in your voice channel.")
        else:
            if arg.lower() == "any":
                voice.play(FFmpegPCMAudio(sounds_dir + random.choice(sound_files)))
            else:
                try:
                    voice.play(FFmpegPCMAudio(sounds_dir + arg.lower() + '.mp3'))
                except:
                    await ctx.send(ctx.author.name + ": I don't have that sound. Current options:" + 
                                    '\n' + ', '.join(sound_file_commands) + ", or 'any' for a random one.")
    else:
        await ctx.send(ctx.author.name + ": I'm not in a voice channel.")


client.run(env("DISCORD_TOKEN"))