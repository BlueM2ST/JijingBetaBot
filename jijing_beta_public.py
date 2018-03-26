# -*- coding: utf-8 -*-
# Author: @BlueM1ST
# App Name: Jijing beta bot
# Python 3.x support only, written in 3.5.2
# Purpose: A bot for beta testing. The more public base version.

import discord
from discord.ext import commands
from random import randint
import asyncio

description = 'Jijing Beta Bot'
bot = commands.Bot(command_prefix='!', description=description)
bot.remove_command("help")
bot.server = bot.servers

# these values will need to be changed for every new server
BUGLIST_CHANNEL_ID = 'ID'
BUGLIST_CHANNEL_NAME = 'beta_buglist'

TESTING_CHANNEL_ID = 'ID'
TESTING_CHANNEL_NAME = 'game_testing'

GENERAL_CHANNEL_ID = 'ID'
GENERAL_CHANNEL_NAME = 'general'

ADMIN_CHANNEL_ID = 'ID'
ADMIN_CHANNEL_NAME = 'admin'

mainIssuelist = []
betaDatabase = 'testBetaFile.txt'
gameName = 'test'
BOTTOKEN = 'TOKEN'

# ======================================= based on specific chat sequences ==========================================
likeList = ['cat', 'anime', 'vn', 'visual novel', 'bot', 'love', 'discord', 'youtube', 'twitter', 'book',
            'ham', 'poster', 'phone', 'tree', 'website', 'kitten', 'dog', 'puppy', 'game', 'mmd', 'miku']
# runs when a message is posted in the chat
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        pass

    if ('hello' in message.content.lower() or 'hi' in message.content.lower()) and 'jijing' in message.content.lower():
        msg = 'Uh, hi, {0.author.mention}'.format(message)
        await bot.send_message(message.channel, msg)

    elif message.content.lower().startswith('jijing status'):
        msg = 'I\'m fine, {0.author.mention}, I suppose.'.format(message)
        await bot.send_message(message.channel, msg)

    elif message.content.lower().startswith('goodbot') or message.content.lower().startswith('good bot'):
        msg = 'Mhm.'
        await bot.send_message(message.channel, msg)

    elif message.content.lower().startswith('badbot') or message.content.lower().startswith('bad bot'):
        msg = 'Er...'
        await bot.send_message(message.channel, msg)

    elif ('favourite' in message.content.lower() or 'best' in message.content.lower()) and ('song' in message.content.lower()
         or 'music' in message.content.lower()) \
         and 'jijing' in message.content.lower() and ('you' in message.content.lower()
         or 'the' in message.content.lower()):
        msg = 'My favourite song is https://www.youtube.com/watch?v=Aa3rgnV6WY8&list=RDAa3rgnV6WY8'
        await bot.send_message(message.channel, msg)

    elif 'you' in message.content.lower() and ('like' in message.content.lower()
            or 'watch' in message.content.lower() or 'enjoy' in message.content.lower()) \
            and 'jijing' in message.content.lower() \
            and [w for w in likeList if w in message.content.lower()]:
        msg = 'I like {}.'.format(str([w + 's' for w in likeList if w in message.content.lower()])[1:-1])
        msg = msg.replace('\'', '')
        msg = msg.replace(',', ' and')
        await bot.send_message(message.channel, msg)

    # will allow commands to also run while it checks in this message block
    await bot.process_commands(message)


# ========================================= initialize =======================================================


bot.all_ready = False
bot._is_all_ready = asyncio.Event(loop=bot.loop)
async def wait_until_all_ready():
    """Wait until the entire bot is ready."""
    await bot._is_all_ready.wait()
bot.wait_until_all_ready = wait_until_all_ready


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for server in bot.servers:
        bot.server = server
        if bot.all_ready:
            break

        print("Something went wrong and {} had to restart! But I'm back here in {} now!"
              .format(bot.user.name, server.name))

    # sets which game the bot is playing
    await bot.change_presence(game=discord.Game(name='beta testing!'))

# ===============================================================================================================
#
#                                       --BETA TESTER COMMANDS--
#
# ===============================================================================================================

# ======================================== For test Beta ===================================================
# help command
@commands.has_role('Beta Group')
@bot.command(pass_context=True, hidden=True)
async def betahelp(ctx):
    channel = ctx.message.channel
    member = ctx.message.author
    # ======= deletes the message, prints a warning ================
    if str(channel) != TESTING_CHANNEL_NAME:
        await bot.delete_message(ctx.message)
        if str(channel) != TESTING_CHANNEL_NAME and member.nick != 'None':
            await bot.say('Please don\'t post beta commands here, {}.'.format(member.nick))
        elif str(channel) != TESTING_CHANNEL_NAME:
            await bot.say('Please don\'t post beta commands here, {}.'.format(member.name))

    # ========= all the commands for help ============
    general = 'Must be in the format:\n'\
              '```' \
              '!beta <error code (0-5)> <chapter> <error line> <desc>' \
              '```\n' \
              '```!edit <report ID> <modification> <new value>```\n'
    code = 'Value <code> must be between:\n```0 and 5```\n'
    errorcodes = 'And the codes are:\n' \
                 '```' \
                 '0 : might be an issue\n1 : could be done/worded better\n' \
                 '2 : typo\n3 : untranslated line\n' \
                 '4 : game error/problem\n5 : crash or game-breaking error' \
                 '```\n' \
                 'For easy lookup, use !errorcodes\n\n'
    chapter = 'Value <chapter> must be one of these values:\n'\
                '```' \
              'prologue | chapter1 | chapter2 | chapter3 | chapter4 | chapter5 | chapter6 | ' \
              'chapter7 | chapter8 | chapter9 | end | extra ' \
              '```\n'
    line = 'Value <line> must be:\n' \
           '```1 or greater, but less than 50000```\n'
    modifications = 'Value <modification> can be:\n' \
                    '```' \
                    'del     : deletes a report (no need for <new value>)\n' \
                    'code    : replaces an error code\n' \
                    'chapter : replaces the chapter\n' \
                    'line    : replaces the line\n' \
                    'desc    : replaces the description in full' \
                    '```\n' \
                    'For easy lookup, use !modifications\n\n'
    example = 'For example:\n' \
              '```!beta 2 chapter1 38 There is a typo on this line ' \
              'of \'teh\' and it should be \'the\'.' \
              '```\n' \
              '```' \
              '!edit 12345 del\n' \
              '!edit 12345 line 100' \
              '```\n'
    # the bot says these commands
    await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID), 'All information for the Cryste beta is here:\n'
                + general + code + errorcodes + chapter + line + modifications + example)


# ====================================================================================================================
#
#                                     ==============BETA TESTING===============
#
# ====================================================================================================================

@commands.has_role('Beta Group')
@bot.command(pass_context=True, hidden=True)
async def beta(ctx, code='', chapter='', line='', *, description=''):
    try:
        member = ctx.message.author
        message = ctx.message
        channel = message.channel

        # ====== deletes the message, RAISES AN EXCEPTION and error message if format is wrong ==========
        if line == '' or description == '' or code == '' or chapter == '':
            if str(channel) != TESTING_CHANNEL_NAME and member.nick != 'None':
                await bot.delete_message(ctx.message)
                await bot.say('Please don\'t post beta commands here, {}.'.format(member.nick))
            elif str(channel) != TESTING_CHANNEL_NAME:
                await bot.delete_message(ctx.message)
                await bot.say('Please don\'t post beta commands here, {}.'.format(member.name))
            raise ValueError

        # ======= deletes the message, prints a warning ================
        if str(channel) != TESTING_CHANNEL_NAME:
            await bot.delete_message(ctx.message)
            if str(channel) != TESTING_CHANNEL_NAME and member.nick != 'None':
                await bot.say('Please don\'t post beta commands here, {}.'.format(member.nick))
            elif str(channel) != TESTING_CHANNEL_NAME:
                await bot.say('Please don\'t post beta commands here, {}.'.format(member.name))

        # ====== make sure the basic format is correct ===========
        checkIfCodeIsInt = int(code)
        if checkIfCodeIsInt > 5 or checkIfCodeIsInt < 0:
            await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID), 'Value <code> must be between 0 and 5')
            return
        chapterList = ['prologue', 'chapter1', 'chapter2', 'chapter3', 'chapter4', 'chapter5', 'chapter6',
                       'chapter7', 'chapter8', 'chapter9', 'end', 'extra']
        set = False
        for value in chapterList:
            if chapter == value:
                set = True
            else:
                pass
        if set != True:
            await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                'Value <chapter> must be one of these values:\n'
                '```prologue | chapter1 | chapter2 | chapter3 | chapter4 | chapter5 | chapter6 |'
                'chapter7 | chapter8 | chapter9 | end | extra ```')
            return

        checkIfLineIsInt = int(line)
        if checkIfLineIsInt <= 0 or checkIfLineIsInt >= 50000:
            await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                   'Value <line> must be more than 0 and less than 50000')
            return

        description = description.replace('\n', '')

        # ==========if the list is empty, try to repopulate it============
        if not mainIssuelist:
            print('Database is empty for {}, attempting to repopulate.'.format(gameName))
            betaFile = open(betaDatabase, 'r', encoding='utf-8')
            read = betaFile.readlines()
            for thisline in read:
                # line = []
                # line.append(thisline)
                mainIssuelist.append(thisline)
            print('Repopulated {} memory database.\n'.format(gameName))

        # ==========check if the line+chapter has already been reported==============
        set = False
        for value in mainIssuelist:
            value = value.split('<|>')
            try:
                if value[4] == line and chapter in value[3]:
                    checkMessage = 'This line has already been set as an issue by {} with description: ' \
                                   '```{}``` '.format(value[1], value[5])
                    await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID), checkMessage)
                    set = True
                else:
                    pass
            except IndexError:
                await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID), 'Error.')
                pass
        # if it has been reported, ask if they want to report a new issue on this line
        if set is True:
            await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),'Type \'yes\' to report a new issue on '
                                                                           'this line, you have 5 seconds.')
            msg = await bot.wait_for_message(author=member, content='yes', timeout=15)
            if msg == None:
                return

        # ======== open the file for appending lines to it ==================
        # make the id
        while True:
            id = str(randint(10000, 99999))
            # if this id is already in use, make a new one
            if id in mainIssuelist:
                continue
            else:
                break
        betaFile = open(betaDatabase, 'a', encoding='utf-8')
        # if no nickname is set
        if member.nick == None:
            issueMessage = '#{} {} issue set by {} with code {} in {} on line {} with desc: {}\n'\
                .format(id, gameName, member.name, code, chapter, line, description)
            betaFile.write(id + '<|>' + member.name +'<|>'+ code +'<|>'+ chapter +'<|>'+ line +'<|>'
                                 + description + '\n')
            # append it to memory
            mainIssuelist.append(id + '<|>' + member.name + '<|>' + code + '<|>' + chapter + '<|>' + line
                                       + '<|>' + description + '\n')
        # by default, if a nickname is set, it will use it.
        else:
            issueMessage = '#{} {} issue set by {} with code {} in {} on line {} with desc: {}\n' \
                .format(id, gameName, member.nick, code, chapter, line, description)
            betaFile.write(id + '<|>' + member.nick +'<|>'+ code +'<|>'+ chapter +'<|>'+ line +'<|>'
                                 + description + '\n')
            # append it to memory
            mainIssuelist.append(id + '<|>' + member.nick +'<|>'+ code +'<|>'+ chapter +'<|>'+ line +'<|>'
                                       + description + '\n')

        # =========== finishing up ==================
        await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID), issueMessage)
        betaFile.close()

        # =========== message the buglist channel =======
        say = ''
        for issue in mainIssuelist:
            issue = issue.split('<|>')
            say += '#{} {} issue set by {} with code {} in {} on line {} with desc: {}\n'\
                .format(issue[0], gameName, issue[1], issue[2], issue[3], issue[4], issue[5])
        # delete the old message
        await bot.purge_from(channel=bot.get_channel(id=BUGLIST_CHANNEL_ID), limit=200)

        # Discord limits a post to 2000 characters
        if say == '':
            say = 'Empty database.'
            # make the new message
            await bot.send_message(discord.Object(id=BUGLIST_CHANNEL_ID), say)
        else:
            charmax = 1700
            currentCount = 0
            localCount = 0
            messageLast = True
            currentMessage = ''
            messageList = say.split('\n')
            for line in messageList:
                messageLast = True
                currentCount += len(line)
                localCount += len(line)
                if currentCount > charmax:
                    await bot.send_message(discord.Object(id=BUGLIST_CHANNEL_ID), currentMessage)
                    currentMessage = ''
                    currentCount = localCount
                    messageLast = False
                currentMessage += line + '\n'
                localCount = 0
            if messageLast == True:
                await bot.send_message(discord.Object(id=BUGLIST_CHANNEL_ID), currentMessage)

        return
    except ValueError:
        await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID), 'Must be in the format:\n'
                                '```!beta <error code (0-5)> <chapter> <error line> <desc>```')
        return


# ==================================== edit values in database =====================================================
@commands.has_role('Beta Group')
@bot.command(pass_context=True, hidden=True)
async def edit(ctx, id='', use='', *,new=''):
    member = ctx.message.author
    message = ctx.message
    channel = message.channel
    try:
        if id == '':
            raise ValueError

        # ======= deletes the message, prints a warning ================
        if str(channel) != TESTING_CHANNEL_NAME:
            await bot.delete_message(ctx.message)
            if str(channel) != TESTING_CHANNEL_NAME and member.nick != 'None':
                await bot.say('Please don\'t post beta commands here, {}.'.format(member.nick))
            elif str(channel) != TESTING_CHANNEL_NAME:
                await bot.say('Please don\'t post beta commands here, {}.'.format(member.name))

        # ====== check to make sure there are allowable values ========
        if use != 'del' and use != 'delete' and new == '':
            await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID), 'There must be a value in <new>.')
            return

        # ==========if the list is empty, try to repopulate it============
        if not mainIssuelist:
            print('Database is empty for {}, attempting to repopulate.'.format(gameName))
            betaFile = open(betaDatabase, 'r', encoding='utf-8')
            read = betaFile.readlines()
            for thisline in read:
                mainIssuelist.append(thisline)
            print('Repopulated {} memory database.\n'.format(gameName))

        # if the user of this command actually submitted the report
        # you can't edit a report you didn't submit yourself

        # This will be false if the code for the ID was not run, otherwise that code will end the command
        idMatch = False
        count = 0
        for line in mainIssuelist:
            splitLine = line.split('<|>')
            if id == splitLine[0]:

                # ============== if it gets here, then the id exists and the user has permission ===============
                if splitLine[1] == member.name or splitLine[1] == member.nick:

                    if use == 'del' or use == 'delete':
                        del mainIssuelist[count]
                        say = 'Report deleted.'

                    elif use == 'code':
                        try:
                            checkIfCodeIsInt = int(new)
                            if checkIfCodeIsInt > 5 or checkIfCodeIsInt < 0:
                                await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                                       'Value <code> must be between 0 and 5')
                                return
                            splitLine[2] = new
                            mainIssuelist[count] = '<|>'.join(splitLine)
                            say = 'Code updated.'

                        except ValueError:
                            await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                                   'Value <code> must be between 0 and 5')
                            return

                    elif use == 'chapter':
                        chapterList = ['prologue', 'chapter1', 'chapter2', 'chapter3', 'chapter4', 'chapter5',
                                       'chapter6', 'chapter7', 'chapter8', 'chapter9', 'end', 'extra']
                        set = False
                        for value in chapterList:
                            if new == value:
                                set = True
                            else:
                                pass
                        if set != True:
                            await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                                   'Value <chapter> must be one of these values:\n'
                                                   '```prologue | chapter1 | chapter2 | chapter3 | chapter4 | chapter5 |'
                                                   ' chapter6 | chapter7 | chapter8 | chapter9 | end | extra```')
                            return
                        splitLine[3] = new
                        mainIssuelist[count] = '<|>'.join(splitLine)
                        say = 'Chapter updated.'

                    elif use == 'line':
                        try:
                            checkIfLineIsInt = int(new)
                            if checkIfLineIsInt <= 0 or checkIfLineIsInt >= 50000:
                                await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                                       'Value <line> must be a number more than 0 and less than 50000')
                                return
                        except ValueError:
                            await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                                   'Value <line> must be a number more than 0 and less than 50000')
                            return
                        splitLine[4] = new
                        mainIssuelist[count] = '<|>'.join(splitLine)
                        say = 'Line updated.'

                    elif use == 'desc' or use == 'description':
                        splitLine[5] = new
                        mainIssuelist[count] = '<|>'.join(splitLine)
                        say = 'Description updated.'

                    else:
                        await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                               'This <modification> does not exist.')
                        return

                    # write the new modified list to the database
                    betaFile = open(betaDatabase, 'w', encoding='utf-8')
                    write = ''
                    for value in mainIssuelist:
                        write += value
                    betaFile.write(write)
                    betaFile.close()
                    if say == '':
                        say = 'Error.'
                    await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID), say)

                    # =========== message the buglist channel =======
                    say = ''
                    for issue in mainIssuelist:
                        issue = issue.split('<|>')
                        say += '#{} {} issue set by {} with code {} in {} on line {} with desc: {}\n' \
                            .format(issue[0], gameName, issue[1], issue[2], issue[3], issue[4], issue[5])
                    # delete the old message
                    await bot.purge_from(channel=bot.get_channel(id=BUGLIST_CHANNEL_ID), limit=100)

                    # Discord limits a post to 2000 characters
                    if say == '':
                        say = 'Empty database.'
                        # make the new message
                        await bot.send_message(discord.Object(id=BUGLIST_CHANNEL_ID), say)
                    else:
                        charmax = 1700
                        currentCount = 0
                        localCount = 0
                        messageLast = True
                        currentMessage = ''
                        messageList = say.split('\n')
                        for line in messageList:
                            messageLast = True
                            currentCount += len(line)
                            localCount += len(line)
                            if currentCount > charmax:
                                await bot.send_message(discord.Object(id=BUGLIST_CHANNEL_ID), currentMessage)
                                currentMessage = ''
                                currentCount = localCount
                                messageLast = False
                            currentMessage += line + '\n'
                            localCount = 0
                        if messageLast == True:
                            await bot.send_message(discord.Object(id=BUGLIST_CHANNEL_ID), currentMessage)
                    return

                else:
                    await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                           'You do not have permission to modify this report.')
                    return

            else:
                count += 1
                pass

        if idMatch == False:
            await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID), 'ID {} does not exist.'.format(id))
            return

    except ValueError:
        await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                               'Must be in the form: ```!edit <report ID> <modification> <new value>```.')
        return

# ==================================== EXTRA COMMANDS =========================================================
@commands.has_role('Beta Group')
@bot.command()
async def errorcodes():
    msg = '```0 : might be an issue\n1 : could be done/worded better\n2 : typo\n3 : untranslated line\n' \
          '4 : game error/problem\n5 : crash or game-breaking error```'
    await bot.say(msg)


@commands.has_role('Beta Group')
@bot.command()
async def modifications():
    msg = 'Value <modification> can be:\n' \
                    '```' \
                    'del     : deletes a report (no need for <new value>)\n' \
                    'code    : replaces an error code\n' \
                    'chapter : replaces the chapter\n' \
                    'line    : replaces the line\n' \
                    'desc    : replaces the description in full' \
                    '```\n'
    await bot.say(msg)


# ===============================================================================================================
#
#                                       --ADMIN COMMANDS--
#
# ===============================================================================================================


# ==================================== edit values in database =====================================================
# same as !edit, but it will work on any report, not just the ones submitted by the author.
@commands.has_role('Admin_like')
@bot.command(pass_context=True, hidden=True)
async def editca(ctx, id='', use='', *,new=''):
    member = ctx.message.author
    message = ctx.message
    channel = message.channel
    try:
        if id == '':
            raise ValueError

        # ======= deletes the message, prints a warning ================
        if str(channel) != TESTING_CHANNEL_NAME:
            await bot.delete_message(ctx.message)
            if str(channel) != TESTING_CHANNEL_NAME and member.nick != 'None':
                await bot.say('Please don\'t post beta commands here, {}.'.format(member.nick))
            elif str(channel) != TESTING_CHANNEL_NAME:
                await bot.say('Please don\'t post beta commands here, {}.'.format(member.name))

        # ====== check to make sure there are allowable values ========
        if use != 'del' and use != 'delete' and new == '':
            await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID), 'There must be a value in <new>.')
            return

        # ==========if the list is empty, try to repopulate it============
        if not mainIssuelist:
            print('{} memory database is empty, attempting to repopulate.'.format(gameName))
            betaFile = open(betaDatabase, 'r', encoding='utf-8')
            read = betaFile.readlines()
            for thisline in read:
                mainIssuelist.append(thisline)
            print('Repopulated {} memory database.\n'.format(gameName))

        # if the user of this command actually submitted the report
        # you can't edit a report you didn't submit yourself

        # This will be false if the code for the ID was not run, otherwise that code will end the command
        idMatch = False
        count = 0
        for line in mainIssuelist:
            splitLine = line.split('<|>')
            if id == splitLine[0]:

                if use == 'del' or use == 'delete':
                    del mainIssuelist[count]
                    say = 'Report deleted.'

                elif use == 'code':
                    try:
                        checkIfCodeIsInt = int(new)
                        if checkIfCodeIsInt > 5 or checkIfCodeIsInt < 0:
                            await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                                   'Value <code> must be between 0 and 5')
                            return
                        splitLine[2] = new
                        mainIssuelist[count] = '<|>'.join(splitLine)
                        say = 'Code updated.'

                    except ValueError:
                        await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                               'Value <code> must be between 0 and 5')
                        return

                elif use == 'chapter':
                    chapterList = ['prologue', 'chapter1', 'chapter2', 'chapter3', 'chapter4', 'chapter5',
                                   'chapter6']
                    set = False
                    for value in chapterList:
                        if new == value:
                            set = True
                        else:
                            pass
                    if set != True:
                        await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                               'Value <chapter> must be one of these values:\n'
                                               '```prologue | chapter1 | chapter2 | chapter3 | chapter4 | chapter5 | chapter6```')
                        return
                    splitLine[3] = new
                    mainIssuelist[count] = '<|>'.join(splitLine)
                    say = 'Chapter updated.'

                elif use == 'line':
                    try:
                        checkIfLineIsInt = int(new)
                        if checkIfLineIsInt <= 0 or checkIfLineIsInt >= 50000:
                            await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                                   'Value <line> must be a number more than 0 and less than 50000')
                            return
                    except ValueError:
                        await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                               'Value <line> must be a number more than 0 and less than 50000')
                        return
                    splitLine[4] = new
                    mainIssuelist[count] = '<|>'.join(splitLine)
                    say = 'Line updated.'

                elif use == 'desc' or use == 'description':
                    splitLine[5] = new
                    mainIssuelist[count] = '<|>'.join(splitLine)
                    say = 'Description updated.'

                else:
                    await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                                           'This <modification> does not exist.')
                    return

                # write the new modified list to the database
                betaFile = open(betaDatabase, 'w', encoding='utf-8')
                write = ''
                for value in mainIssuelist:
                    write += value
                betaFile.write(write)
                betaFile.close()
                if say == '':
                    say = 'Error.'
                await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID), say)

                # =========== message the buglist channel =======
                say = ''
                for issue in mainIssuelist:
                    issue = issue.split('<|>')
                    say += '#{} {} issue set by {} with code {} in {} on line {} with desc: {}\n' \
                        .format(issue[0], gameName, issue[1], issue[2], issue[3], issue[4], issue[5])
                # delete the old message
                await bot.purge_from(channel=bot.get_channel(id=BUGLIST_CHANNEL_ID), limit=100)

                # Discord limits a post to 2000 characters
                if say == '':
                    say = 'Empty database.'
                    # make the new message
                    await bot.send_message(discord.Object(id=BUGLIST_CHANNEL_ID), say)
                else:
                    charmax = 1700
                    currentCount = 0
                    localCount = 0
                    messageLast = True
                    currentMessage = ''
                    messageList = say.split('\n')
                    for line in messageList:
                        messageLast = True
                        currentCount += len(line)
                        localCount += len(line)
                        if currentCount > charmax:
                            await bot.send_message(discord.Object(id=BUGLIST_CHANNEL_ID), currentMessage)
                            currentMessage = ''
                            currentCount = localCount
                            messageLast = False
                        currentMessage += line + '\n'
                        localCount = 0
                    if messageLast == True:
                        await bot.send_message(discord.Object(id=BUGLIST_CHANNEL_ID), currentMessage)
                return

            else:
                count += 1
                pass

        if idMatch == False:
            await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID), 'ID {} does not exist.'.format(id))
            return

    except ValueError:
        await bot.send_message(discord.Object(id=TESTING_CHANNEL_ID),
                               'Must be in the form: ```!editca <report ID> <modification> <new value>```.')
        return

# =============================================================================================================
@commands.has_role('Admin')
@bot.command(pass_context=True)
async def delchannelmessages(ctx, limit=1):
    try:
        message = ctx.message
        channel = message.channel
        limit = int(limit)
        await bot.purge_from(channel=channel, limit=limit)
    except Exception:
        await bot.send_message(discord.Object(id=ADMIN_CHANNEL_ID), 'To delete every message in a channel, you'
                                                                    'must use this format: !delchannelmessages <limit>')

# ================================================ Prints a static invite ========================================
@bot.command()
async def invite():
    await bot.say('Here you go: INVITE HERE')

# =========================================== displays an update message ========================================
@commands.has_role('Admin')
@bot.command()
async def update():
    await bot.say('Oh, an update?')

# ========================================= used to log out of the bot ==========================================
@commands.has_role('Admin')
@bot.command()
async def disconnectbot():
    await bot.logout()

# ================================================= run the bot ==================================================
# runs the bot with its ticket
bot.run(BOTTOKEN)
