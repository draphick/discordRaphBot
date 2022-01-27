# Work with Python 3.7
# Migration commands: https://discordpy.readthedocs.io/en/latest/migrating.html
from pyFuncs import *
from pyJsonread import *

watch = OnMyWatch()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.lower() == "rghelp":
        await message.channel.send("""Here are all the commands I have:
        rghelp - Provides this help tool tip.
        rgbotlink - Show the link to add this bot to your own Discord server.
        rgrps {rock|paper|scissors} - Play rock paper scissorsself. eg `rgrps rock`
        rgrandom {space delimitied array} - Have the bot randomly make a selection from the list you provide.  eg. `rgrandom Raph Jerm Crista Bryan`
        d{1-99999} - Roll a {number} sided dice.  The number can be 5 digits long.
        rgdraw {movies|action} - Lets play Telestrations!  Modify these .json to add/delete options: `https://github.com/draphick/jsonfiles`
        tr {translate these words} - Translate english to Tagalog.  eg. `tr I'm hungry`""")



    if message.content.lower().startswith('dickbutt'):
        """ 
            Here's a picture of a dickbutt  
            Nothing special here, just added for kicks.
        """

        embed = discord.Embed(description=message.author.mention + " wants you to look at this dick butt.", color=0xFFC0CB)
        embed.set_image(url="https://images-na.ssl-images-amazon.com/images/I/41q1QAln%2BQL.jpg")
        await message.channel.send(embed=embed)

    if message.content.lower().startswith('rgrandom'):
        """ 
            Given multiple choices, pick one at randoms and reply back
        """
        fullstr = message.content.lower()
        splitmsg = fullstr.split()
        splitmsg.remove('rgrandom')
        if len(splitmsg) < 2:
            await message.channel.send("You need to provide more than one random choice.  eg. rgrandom vote1 vote2 vote3")
        else:
            await message.channel.send("Random choice made: " + random.choice(splitmsg))

    if message.content.lower().startswith('rgrps'):
        """
            Play rock paper scissors!
        """
        rps = [
            "rock",
            "paper",
            "scissors"
        ]
        splitmsg = message.content.split()
        cpu = random.choice(rps)
        if len(splitmsg) < 2:
            await message.channel.send("To play you need to select rock|paper|scissors.  eg. `rgrps rock`")
        elif splitmsg[1] == "rock":
            if cpu == "rock":
                await message.channel.send("YOU TIED!" + "\nComputer picked: " + cpu)
            if cpu == "paper":
                await message.channel.send("YOU LOSE!" + "\nComputer picked: " + cpu)
            if cpu == "scissors":
                await message.channel.send("YOU WIN!" + "\nComputer picked: " + cpu)
        elif splitmsg[1] == "paper":
            if cpu == "paper":
                await message.channel.send("YOU TIED!" + "\nComputer picked: " + cpu)
            if cpu == "scissors":
                await message.channel.send("YOU LOSE!" + "\nComputer picked: " + cpu)
            if cpu == "rock":
                await message.channel.send("YOU WIN!" + "\nComputer picked: " + cpu)
        elif splitmsg[1] == "scissors":
            if cpu == "scissors":
                await message.channel.send("YOU TIED!" + "\nComputer picked: " + cpu)
            if cpu == "rock":
                await message.channel.send("YOU LOSE!" + "\nComputer picked: " + cpu)
            if cpu == "paper":
                await message.channel.send("YOU WIN!" + "\nComputer picked: " + cpu)
        else:
            await message.channel.send("You didn't pick rock paper or scriccors. Try again.")

    if message.content.lower().startswith('rgbotlink'):
        """
            Link to invite this bot to your own server
        """
        await message.channel.send("https://discordapp.com/oauth2/authorize?client_id=507254510033305600&scope=bot&permissions=0")

    if message.content.lower().startswith('rgdraw'):
        """
            This will DM you something random to draw if you're bored.
        """
        splitmsg = message.content.split()
        if len(splitmsg) < 2:
            await message.channel.send(message.author.mention + " You need to choose: `movies` or `action`.  eg. `!draw movies`")
            draw = "You need to choose: `movies` or `action`.  eg. `!draw movies`"
        elif splitmsg[1] == "movies":
            await message.channel.send(message.author.mention + " is drawing something!")
            draw = "Let's do it!  You have to draw: " + getlist("https://raw.githubusercontent.com/draphick/jsonfiles/master/draw.movies.json")
        elif splitmsg[1] == "action":
            await message.channel.send(message.author.mention + " is drawing something!")
            draw = "Let's do it!  You have to draw: " + getlist("https://raw.githubusercontent.com/draphick/jsonfiles/master/draw.actions.json")
        else:
            await message.channel.send(message.author.mention + " You need to choose: `movies` or `action`.  eg. `!draw movies`")
            draw = "You need to choose: `movies` or `action`.  eg. `!draw movies`"
        await message.author.send(draw)

    if rollregex.match(message.content.lower()):
        """
            Roll some digital dice.  You can roll up to a 10,000 sided dice.
        """
        fullstr = message.content.lower()
        justnumber = fullstr.replace("d", "")
        dice = int(justnumber)
        await message.channel.send(message.author.mention + " rolled a: " + "**" + str(random.randint(1, dice)) + "**")


          
########################## Some personal hidden bot commands
    if message.content.lower().endswith('#') or message.content.lower().startswith('tr '):
        """
            Translate Tagalog to English or vice versa
            This will also log in a gSheet each time it is able to successfully translate something
        """
        if message.content.lower().endswith('#'):
            splittingmsg = message.content.lower().split("#", 1)
            splitmsg = splittingmsg[0]
        else:
            splittingmsg = message.content.lower().split("tr ", 1)
            splitmsg = splittingmsg[1]
        detect = translator.detect(splitmsg)
        if detect.lang == 'en':
            translatethis = translator.translate(splitmsg, dest='tl', src='en')
            msg = translatethis.text
            if msg.lower() in splitmsg.lower():
                await message.channel.send("No Tagalog translation found for - " + splitmsg)
            else:
                await message.channel.send(msg)  
                writerow('now','now','ENGLISH',splitmsg,msg,message.author.mention,None,None,tagalogsheet)
                # send msg (english translation) send splitmsg (tagalog message)
        elif detect.lang == 'tl':
            translatethis = translator.translate(splitmsg, dest='en', src='tl')
            msg = translatethis.text
            if msg.lower() in splitmsg.lower():
                await message.channel.send("No English translation found for - " + splitmsg)
            else:
                await message.channel.send(msg + " - `Attempted Tagalog translation.`")  
                # send msg (tagalog translation) send splitmsg (english message)
                writerow('now','now','TAGALOG',splitmsg,msg,message.author.mention,None,None,tagalogsheet)

        else:
            await message.channel.send("Did not detect english or tagalog.  Try again.")  

    if message.content.startswith(requestbotid):
        """
            The $requestbotid is a role on my server that I created
            for users to ping when they want to request a movie
            or TV show on my Plex server.
            Right now it's _not_ auto doing the download for me.  It will
            just send a DM to me with who requested it and what they requested.
            I didn't wanted it auto downloading in case users are
            requesting full 20 season shows or movies that would be
            too difficult to find on an NZB tracker.
        """
        splitmsg = message.content.lower().split(">", 1)
        me2 =  await client.fetch_user(ownerid)
        if "--force" in splitmsg[1]:
            await message.add_reaction("\U00002714")
            await message.channel.send(message.author.mention + " **Ouch**.  Don't gotta force it in me that hard. Okay, okay! I'll tell Raph to add!")
            await me2.send(message.author.mention + " **FORCE** requested - " + splitmsg[1] + " \nhttps://radarr.odrallag.com\nhttps://sonarr.odrallag.com")
            return
        if "tv show" in splitmsg[1] or "movie" in splitmsg[1]:
            match = re.match(r'.*([1-3][0-9]{3})', splitmsg[1])
            if "movie" in splitmsg[1]:
                if match is None:
                    urlsplitmov = splitmsg[1].replace("movie", "")
                    urlsplit = urlsplitmov.replace(" ", "+")
                    await message.channel.send(message.author.mention + " If you are requesting a movie, please provide the (full) year of the movie.  If you need help finding the year, let me IMDB that for you:")
                    await message.channel.send('https://www.imdb.com/find?q=' + urlsplit)
                    await message.channel.send("Example request: \n<@&480191886670168094> 28 Days Later (2002) Movie")
                    await message.add_reaction("\U0000274E")
                else:
                    urlsplitmov = splitmsg[1].replace("movie", "")
                    urlsplitmov = urlsplitmov.replace(match.group(1), "")
                    urlsplitmov = re.sub(r'\W+', ' ',str(urlsplitmov))
                    radarrreturn = getplex(urlsplitmov.rstrip().strip(), 'movie', int(match.group(1)))
                    countitems = 0
                    for key,val in radarrreturn.items():
                        countitems = countitems + 1
                    if countitems > 0:
                        await message.channel.send("**Uh oh!**  I found " + str(countitems) + " already in Plex or queued up to download.  Is this what you're looking for?")
                        for key,val in radarrreturn.items():
                            await message.channel.send(val)
                        await message.channel.send("If this is not what you're looking for, request it again but force it by adding _--force_ at the end of your request.  Like this:\n" + message.content + " --force")
                    else:
                        await message.channel.send(message.author.mention + " Awesome, I'll try looking for that movie!")
                        await me2.send(message.author.mention + " requested - " + splitmsg[1] + " https://radarr.odrallag.com/add/new?term="+ splitmsg[1])
                        await message.add_reaction("\U00002714")
                    # How to use reaction: https://www.reddit.com/r/discordapp/comments/8j1ywl/discordpy_how_to_use_add_reaction/
            else:
                urlsplitmov = splitmsg[1].replace("tv show", "")
                urlsplitmov = re.sub(r'\W+', ' ',str(urlsplitmov))
                sonarrreturn = getplex(urlsplitmov.rstrip().strip(), 'show')
                countitems = 0
                for key,val in sonarrreturn.items():
                    countitems = countitems + 1
                if countitems > 0:
                    await message.channel.send("**Uh oh!**  I found " + str(countitems) + " already in Plex or queued up to download.  Is this what you're looking for?")
                    for key,val in sonarrreturn.items():
                        await message.channel.send(val)
                    await message.channel.send("If this is not what you're looking for, request it again but force it by adding _--force_ at the end of your request.  Like this:\n" + message.content + " --force")
                else:
                    await message.channel.send(message.author.mention + " Awesome, I'll try looking for that show!!")
                    await me2.send(message.author.mention + " requested - " + splitmsg[1] + " https://sonarr.odrallag.com/add/new?term="+ splitmsg[1])
                    await message.add_reaction("\U00002714")
        else:
            await message.channel.send(message.author.mention + " Please specify if this is a `TV Show` or `Movie` by including `TV Show` or `Movie` in your request message.")
            await message.channel.send("Example request: \n<@&480191886670168094> 28 Days Later (2002) Movie\n<@&480191886670168094> Modern Family TV Show")
            urlsplit = splitmsg[1].replace(" ", "+")
            await message.channel.send("If you need help finding your TV Show or Movie name, try finding it here on IMDB:")
            await message.channel.send('https://www.imdb.com/find?q=' + urlsplit)
            await message.add_reaction("\U0000274E")
    
    if message.content.lower().startswith('rtrack'):
        if message.author.name.lower()  != 'raph':
            await message.channel.send("Wait, you're not Raph.  You can't do this.")
        else:
            splitspace = message.content.lower().split(" ", 1)
            args = splitspace[1].split(" ", 1)
            if len(args) == 2:
                writerow('now','now',args[0],args[1],None,None,None,None,addtracksheet,"raphtracking")
                ttype = "\n    Tracking: " + args[0]
                print(ttype)
                tnotes = "\n    Notes: " + args[1]
                print(tnotes)
                await message.channel.send("New row added!\n```" + ttype + tnotes + "\n```")
            else:
                writerow('now','now',args[0],None,None,None,None,None,addtracksheet,"raphtracking")
                await message.channel.send("New row added!")
                ttype = "\n    Tracking: " + args[0]
                print(ttype)
                tnotes = "\n    Notes: None"
                print(tnotes)
                await message.channel.send("```" + ttype + tnotes + "\n```")
            
    if message.content.lower().startswith('jtrack'):
        if message.author.name.lower()  != 'jermz':
            await message.channel.send("Wait, you're not Jerm.  You can't do this.")
        else:
            splitspace = message.content.lower().split(" ", 1)
            args = splitspace[1].split(" ", 1)
            if len(args) == 2:
                writerow('now','now',args[0],args[1],None,None,None,None,addtracksheet,"jermztracking")
                ttype = "\n    Tracking: " + args[0]
                print(ttype)
                tnotes = "\n    Notes: " + args[1]
                print(tnotes)
                await message.channel.send("New row added! ---\n```" + ttype + tnotes + "\n```")
            else:
                writerow('now','now',args[0],None,None,None,None,None,addtracksheet,"jermztracking")
                await message.channel.send("New row added!")
                ttype = "\n    Tracking: " + args[0]
                print(ttype)
                tnotes = "\n    Notes: None"
                print(tnotes)
                await message.channel.send("Added ---\n```" + ttype + tnotes + "\n```")

    if message.content.lower().startswith('qq'):
        print(message.guild.members)
 


@client.event
async def on_ready():
    
    if os.environ['debug'] == "y":
        print("Logged in DEV")
    else:
        print("Logged in PROD")
    print(client.user.name)
    print(client.user.id)
    print('Bot set to: ' + TOKEN)
    print('------')
    # Get list of servers and memembers
    # for guild in client.guilds:
    #     print("Server: " + str(guild))
    #     for member in guild.members:
    #         print("        " + str(member))
    check_watch_dir(WATCH_DIRECTORY)
    await asyncio.gather(asyncio.ensure_future(watch.run()))
client.run(TOKEN)


