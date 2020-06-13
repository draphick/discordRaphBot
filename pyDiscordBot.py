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
        dl{emote} - Sends an emote from `https://imgur.com/a/2qRlGeI`
        pp{emote} - Sends an emote from `https://imgur.com/a/B1Zy4e7`
        dickbutt - Here's a dickbutt picture.
        rgbotlink - Show the link to add this bot to your own Discord server.
        rgrps {rock|paper|scissors} - Play rock paper scissorsself. eg `rgrps rock`
        rgrandom {space delimitied array} - Have the bot randomly make a selection from the list you provide.  eg. `rgrandom Raph Jerm Crista Bryan`
        d{1-99999} - Roll a {number} sided dice.  The number can be 5 digits long.
        !draw {movies|action} - Lets play Telestrations!  Modify these .json to add/delete options: `https://github.com/draphick/jsonfiles`
        ro{card|monster|item} {search terms} - Search the Ragnarok Mobile database.  eg. `romonster dokebi`
        acget {search terms} - Search villagerdb for items, villagers, recipes, anything.  eg `acget bamboo hat`
        tr {translate these words} - Translate english to Tagalog.  eg. `tr I'm hungry`""")

    if message.content.lower().startswith('dl'):
        """ 
            Send a Dragalia emote
            This commands going through an imgur album and
            pulls the image you request as an embedded emote
        """
        dlemotes = getalbum('https://api.imgur.com/3/album/2qRlGeI/images')
        if message.content.lower() in dlemotes:
            if not isinstance(message.channel, discord.abc.PrivateChannel):
                await message.delete()
            embed = discord.Embed(description=message.author.mention + " reacted with", color=0xFFC0CB)
            embed.set_image(url=dlemotes.get(message.content.lower()))
            await message.channel.send(embed=embed)
            del dlemotes
        else:
            msg = "Emote not found.  Find all emotes here: \n`https://imgur.com/a/2qRlGeI`\n\nYou can also find a list here of available emotes: \n     " + "\n     ".join(str(emote) for emote in dlemotes).format(message)
            await message.channel.send(msg)
            del dlemotes

    if message.content.lower().startswith('pp'):
        """ 
            Send a Panic Pals emote
            This commands going through an imgur album and
            pulls the image you request as an embedded emote
        """
        dlemotes = getalbum('https://api.imgur.com/3/album/B1Zy4e7/images')
        if message.content.lower() in dlemotes:
            if not isinstance(message.channel, discord.abc.PrivateChannel):
                await message.delete()
            embed = discord.Embed(description=message.author.mention + " reacted with", color=0xFFC0CB)
            embed.set_image(url=dlemotes.get(message.content.lower()))
            await message.channel.send(embed=embed)
            del dlemotes
        else:
            msg = "Emote not found.  Find all emotes here: \n`https://imgur.com/a/B1Zy4e7`\n\nYou can also find a list here of available emotes: \n     " + "\n     ".join(str(emote) for emote in dlemotes).format(message)
            await message.channel.send(msg)
            del dlemotes

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

    if message.content.lower().startswith('!draw'):
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

    if message.content.lower().startswith('rocard ') or message.content.lower().startswith('romonster ') or message.content.lower().startswith('roitem '):
        """
            Search the Ragnarokmobile database.  
            They didn't have an API at the time (not sure if they do now)
            Using request to get the website, then using beautifulsoup to
            parse through the html to find the values I needed.
        """
        splitmsg = message.content.lower().split(" ", 1)
        albumimages = {}
        r = requests.get("https://www.ragnarokmobile.net/search?q=" + splitmsg[1], verify=False)
        soup = BeautifulSoup(r.text, 'lxml')

        if len(soup.select("table.table tr")) > 0:
            for table_row in soup.select("table.table tr"):
                cells = table_row.findAll('td')
                link = cells[0].a["href"]
                image = cells[0].img["src"]
                name = cells[1].text
                if "rocard" == splitmsg[0] and "https://www.ragnarokmobile.net/card/" in link:
                    type = "**Card** - "
                    embed = discord.Embed(description=type + name + " - " + link, color=0xFFC0CB)
                    await message.channel.send(embed=embed)
                elif "romonster" == splitmsg[0] and "https://www.ragnarokmobile.net/monster/" in link:
                    type = "**Monster** - "
                    embed = discord.Embed(description=type + name + " - " + link, color=0xFFC0CB)
                    await message.channel.send(embed=embed)
                elif "roitem" == splitmsg[0] and "https://www.ragnarokmobile.net/item/" in link:
                    type = "**Item** - "
                    embed = discord.Embed(description=type + name + " - " + link, color=0xFFC0CB)
                    await message.channel.send(embed=embed)
        else:
            await message.channel.send("Searched for **" + splitmsg[1] + "** and found zero results.")

    if message.content.lower().startswith('acget'):
        """
            Search Villager DB for an item in Animal Crossing!
        """
        splittingmsg = message.content.lower().split(" ", 1)
        splitmsg = splittingmsg[1]
        results = acnhget(splitmsg)
        fullmessage = "Here's what I found: \n"
        if len(results) > 0:
            for key in results:
                # Item name
                countstring = len(key) + 10
                block = ""
                for x in range(countstring):
                    block = block + "-"
                fullmessage = fullmessage + "`[[   " + key.upper() + "   ]]" + '\n' + block + '\n`'
                for value in results[key]:
                    # Sub Level 1
                    fullmessage = fullmessage + '\t' + "**" + value + "**" + '\n'
                    if isinstance(results[key][value], list):
                        for i in results[key][value]:
                            # Sub level 2 if it's a list
                            fullmessage = fullmessage + '\t\t' +  i + '\n'
                    else:
                        # Sub level 2 if it's just a string
                        fullmessage = fullmessage + '\t\t' + results[key][value] + '\n'
        else:
            fullmessage = "Couldn't find anything looking for: \n\t" + splitmsg + "\nTry again."
        await message.channel.send(fullmessage)

    if message.content.lower() == ('noice'):
        """
            giphy noice 
        """
        if not isinstance(message.channel, discord.abc.PrivateChannel):
                await message.delete()
        msg = gifrandom("noice")
        await message.channel.send(msg)

    if message.content.lower() == ('thanks') or message.content.lower() == ('thanks!') or message.content.lower() == ('thanks!!') or message.content.lower() == ('thanks!!!'):
        """
            giphy thanks 
        """
        if not isinstance(message.channel, discord.abc.PrivateChannel):
                await message.delete()
        msg = gifrandom("thanks")
        await message.channel.send(msg)
          
########################## Some personal hidden bot commands
    if message.content.lower().startswith('rgservers'):
        """
            I wanted to be able to check to see what servers my bot is connected to.
        """
        await message.channel.send("A list of all connected servers:\n     " + "\n     ".join(str(servers) for servers in client.guilds))

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
                        await me2.send(message.author.mention + " requested - " + splitmsg[1] + " https://radarr.odrallag.com")
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
                    await me2.send(message.author.mention + " requested - " + splitmsg[1] + " https://sonarr.odrallag.com")
                    await message.add_reaction("\U00002714")
        else:
            await message.channel.send(message.author.mention + " Please specify if this is a `TV Show` or `Movie` by including `TV Show` or `Movie` in your request message.")
            await message.channel.send("Example request: \n<@&480191886670168094> 28 Days Later (2002) Movie\n<@&480191886670168094> Modern Family TV Show")
            urlsplit = splitmsg[1].replace(" ", "+")
            await message.channel.send("If you need help finding your TV Show or Movie name, try finding it here on IMDB:")
            await message.channel.send('https://www.imdb.com/find?q=' + urlsplit)
            await message.add_reaction("\U0000274E")
    
    if message.content.lower().startswith('addtrack'):
        getuser = message.author.name.lower()
        if getuser == 'raph':
            strength = 15
        elif getuser == 'jermz':
            strength = 10
        writerow('now','now','none','water',strength,None,None,None,addtracksheet,getuser + "tracking")
        await message.channel.send("New row added!")
        lastrow = getgsheet(addtracksheet,getuser + "tracking",True,True)
        allstats = {}
        print(lastrow)
        date = "\n    Date: " + str(lastrow[0])
        print(date)
        time = "\n    Time: " + str(lastrow[1])
        print(time)
        food = "\n    Food: " + str(lastrow[2])
        print(food)
        drink = "\n    Drink: " + str(lastrow[3])
        print(drink)
        strength = "\n    Strength: " + str(lastrow[4])
        print(strength)
        await message.channel.send("Added ---\n```" + date + time + food + drink + strength + "\n```")
        

        # allrows = getrow("last",1,addtracksheet)
        # for i in allrows:
        #     name = i['Exercise']
        #     total = i['Reps']
        #     allstats[name] = total
        # for key,value in allrows.items():
        #         await message.channel.send("Row: " + str(key) + "\n-- " + str(value))

    if message.content.lower().startswith('gastrack '):
        """
            Another one to track when I puchase gas for my car
        """
        splitspace = message.content.lower().split(" ", 1)
        command = splitspace[1].split(" ", 1)
        if len(command) == 2:
            args = command[1].split("#")
            if 'add' in command:
                if len(args) != 6:
                    await message.channel.send("Invalid amount of columns, try again!  Remember these columns: ```\nDate\nOdo\nTrip\nDash\nGal\nPrice```")
                else:
                    date = args[0]
                    odo = args[1]
                    trip = args[2]
                    gal = args[4]
                    price = args[5]
                    ppg=float(args[5])/float(args[4])
                    dash = args[5]
                    mpg=float(args[2])/float(args[4])
                    writerow(date,odo,trip,gal,"$"+str(price),"$"+str(round(ppg, 2)),dash,mpg,gastracksheet)
                    await message.channel.send("New row added!")
                    allrows = getrow("last",1,gastracksheet)
                    for key,value in allrows.items():
                        await message.channel.send("Row: " + str(key) + "\n-- " + str(value))
            elif 'view' in command:
                if len(args) != 2:
                    await message.channel.send("Too many / not enough arguments.  Ex: \n`gastrack view only#26` \n`gastrack view last#5`")
                else:
                    allrows = getrow(args[0],int(args[1]),gastracksheet)
                    for key,value in allrows.items():
                        await message.channel.send("Row: " + str(key) + "\n-- " + str(value))
            else:
                await message.channel.send("Did you want to add or view?\n Here are your columns:```\nDate\nOdo\nTrip\nDash\nGal\nPrice```")
        else:
            await message.channel.send("Did you want to add or view?\n Here are your columns:```\nDate\nOdo\nTrip\nDash\nGal\nPrice```")

    if message.content.lower().startswith('!fat'):
        workoutdata_basevalues = { 
            "username": message.author.name, 
            "goals": {
                "pushups": 100,
                "pullups": 100,
                "situps": 100,
                "squats": 100,
                "weight": 190
                },
            "gain_loss": "none",
            "worksheet_tracking": "tracking",
            "worksheet_stats": message.author.name
        }
        userfolder = get_user_folder(message.author.id)
        workoutfile = check_user_json_file(userfolder,'workouts')
        if workoutfile == True:
            workoutinfo = get_user_data(message.author.id,'workouts')
            if workoutinfo == False:
                create_user_json_data(message.author.id,'workouts',workoutdata_basevalues)
                workoutinfo = get_user_data(message.author.id,'workouts')
        workouts = workoutinfo['goals']

        if message.content.lower().startswith('!fatgoal'):
            try:
                splitspace = message.content.lower().split(" ", 1)
                command = splitspace[1].split(" ")
                action = command[0]
            except Exception as e:
                command = None
                action = None
                goalname = None
                print("Could not get commands")
                print(e)
            allactions = [
                "add",
                "remove",
                "update",
                "view"
            ]
            allgoalnames = workouts.keys()
            if action in allactions:
                try:
                    goalname = command[1]
                except Exception as e:
                    msg = "Missing goal name.  Are you looking for one of these?"
                    for workout in allgoalnames:
                            msg = msg + "\n   " + workout
                    goalname = False
                if goalname:
                    if action == "update":
                        try:
                            goalvalue = command[2]
                        except Exception as e:
                            goalvalue = False
                            pass
                        if goalvalue:
                            msg = "Updating your " + goalname + " goal to " + str(goalvalue)
                            workoutinfo['goals'][goalname] = int(goalvalue)
                            update_user_data(message.author.id,'workouts',workoutinfo)
                            updatedinfo = get_user_data(message.author.id,'workouts')
                        else:
                            msg =  "Missing a value you want to update.  I need a number to update " + goalname
                    elif action == "view":
                        msg = "Your current goal for " + goalname + " is: " + str(workouts[goalname])
                    elif action == "remove":
                        if goalname in workouts.keys():
                            del workoutinfo['goals'][goalname]
                            update_user_data(message.author.id,'workouts',workoutinfo)
                            msg = "Goal deleted!  Bye-bye to all your " + goalname
                            updatedinfo = get_user_data(message.author.id,'workouts')

                        else:
                            msg = "You don't have a goal named " + goalname
                    elif action == "add":
                        if goalname in workouts.keys():
                            msg = "Well looky here, you already have a goal named " + goalname
                            msg = msg + "\n Your goal is already set to: " + str(workouts[goalname])
                        else:
                            workoutinfo['goals'][goalname] = 100
                            update_user_data(message.author.id,'workouts',workoutinfo)
                            msg = "Whoa there, you must be getting strong.  Alright I've added " + goalname + " to your workouts with a goal of 100.  Take that!"
                            updatedinfo = get_user_data(message.author.id,'workouts')
                            gsheetquery =  """=IFERROR(
QUERY(
    tracking!$A1:$F,
    "select sum(D) where C = '"&INDEX(A:A, ROW())&"' and F = '{}' and A = date '"&TEXT(TODAY(),"yyyy-mm-dd")&"' group by C label sum(D)''", 0
),0
)""".format(message.author.name.lower())
                            writerow(goalname,gsheetquery,None,None,None,None, None, None,workouttracksheet, message.author.name.lower())
            else:
                msg = "Missing action. Available action types: "
                for missing in allactions:
                    msg = msg + "\n   " + missing
            await message.channel.send(msg)
        elif message.content.lower().startswith('!fatweight'):
            try:
                splitspace = message.content.lower().split(" ", 1)
                command = splitspace[1]
            except Exception as e:
                command = "none"
                print(e)
            print(command)
            if command == "gain":
                workoutinfo['gain_loss'] = "gain"
                update_user_data(message.author.id,'workouts',workoutinfo)
                updatedinfo = get_user_data(message.author.id,'workouts')
                msg = "Setting up to gain weight I see!  \nI set up your profile for weight gain."
            elif command == "loss":
                workoutinfo['gain_loss'] = "loss"
                update_user_data(message.author.id,'workouts',workoutinfo)
                updatedinfo = get_user_data(message.author.id,'workouts')
                msg = "I see you have already lost some weight!  I think?  Maybe?\n I set up your profile for weight loss."

            else:
                workoutinfo['gain_loss'] = "none"
                update_user_data(message.author.id,'workouts',workoutinfo)
                updatedinfo = get_user_data(message.author.id,'workouts')
                msg = "Alright, alright.  Keep it secret.  No weight gain/loss reported."
            await message.channel.send(msg)
            
            
        elif message.content.lower().startswith('!fatadd'):
            """
                doing some workout tracking
                gsheet query:
                =IFERROR(
                    QUERY(
                        tracking!$A1:$F,
                        "select sum(D) where C = '"&INDEX(A:A, ROW())&"' and F = 'raph' and A = date '"&TEXT(TODAY(),"yyyy-mm-dd")&"' group by C label sum(D)''", 0
                    ),0
                )
            """
            splitspace = message.content.lower().split(" ", 1)
            command = splitspace[1].split(" ")
            if len(command) == 2:
                if command[0] not in workouts.keys():
                    msg = "Wrong workout type, must be one of:"
                    for workout in workouts.keys():
                        msg = msg + "\n   " + workout
                    await message.channel.send(msg)
                else:
                    writerow("now","now",command[0], command[1], None, message.author.name.lower(), None, None,workouttracksheet,"tracking")
                    allstats = {}
                    allrows = getgsheet(workouttracksheet,message.author.name.lower())
                    msg = "Added to " + message.author.name + "'s workout sheet: " + command[0] + " " + str(command[1]) + "\n"
                    for i in allrows:
                        name = i['Exercise']
                        total = i['Reps']
                        allstats[name] = total
                    for name,total in allstats.items():
                        try:
                            if name == command[0]:
                                oldtotal = total - int(command[1])
                                if name == 'weight':
                                    msg = msg + "Current total " + name + ": **" + str(total) + "**"
                                    if workoutinfo['gain_loss'] == "loss":
                                        if total > workouts[name]:
                                            left = total - workouts[name]
                                            msg = msg + "\n You still have " + str(left) + " more pounds before you hit " + str(workouts[name])
                                        elif total <= workouts[name]:
                                            msg = msg + "\n You hit your " + name + " goal, congrats!  You hit that!!"
                                            yay = gifrandom('congrats')
                                            msg = msg + "\n" + yay
                                    elif workoutinfo['gain_loss'] == "gain":
                                        if total < workouts[name]:
                                            left = workouts[name] - total
                                            msg = msg + "\n You still have " + str(left) + " more pounds before you hit " + str(workouts[name])
                                        elif total >= workouts[name]:
                                            msg = msg + "\n You hit your " + name + " goal, congrats!  You hit that!!"
                                            yay = gifrandom('congrats')
                                            msg = msg + "\n" + yay
                                    else:
                                        msg = msg + "\n Are you trying to gain or lose weight?"
                                        msg = msg + "  You don't need to let me know, but if you want, let me know with the command: "
                                        msg = msg + "`!fatweight gain` or `!fatweight loss`"
                                else:
                                    msg = msg + "Current total " + name + ": **" + str(total) + "**"
                                    if total < workouts[name]:
                                        left = workouts[name] - total
                                        msg = msg + "\n You still have " + str(left) + " " + " left to do!"
                                    elif total >= workouts[name]:
                                        try:
                                            if oldtotal >= workouts[name]:
                                                msg = msg + "\n You already hit your goal.  Just stahhhpppp!"
                                            else:
                                                msg = msg + "\n You hit your " + name + " goal, congrats!"
                                                yay = gifrandom('congrats')
                                                msg = msg + "\n " + yay
                                        except Exception as e:
                                            print(e)                                        
                        except Exception as e:
                            print(e)
                    await message.channel.send(msg)
            else:
                msg = "Missing or too many arguments.  Provide a workout type and value\n Example: `!fatadd pushups 5` \n Available workout types: "
                for workout in workouts.keys():
                    msg = msg + "\n   " + workout
                await message.channel.send(msg)
        elif message.content.lower().startswith('!fatfood'):
            """
                doing some food tracking
            """
            foodgoal = 20
            splitspace = message.content.lower().split(" ", 1)
            ate = splitspace[1]
            getfoodstats = getgsheet(workouttracksheet,'meals',)
            foods = {}
            getuser = message.author.name.lower()
            for i in getfoodstats:
                name = i['Food'].lower()
                cost = i['Costs']
                foods[name] = cost
            if ate not in foods.keys():
                msg = "Wrong food type (" + ate + "), must be one of:"
                for foodname in foods.keys():
                    msg = msg + "\n   " + foodname
                await message.channel.send(msg)
            else:
                writerow("now","now",'food', foods[ate], ate, message.author.name.lower(), None, None,workouttracksheet, "tracking")
                getfatstats = getgsheet(workouttracksheet,getuser)
                allstats = {}
                for i in getfatstats:
                    name = i['Exercise']
                    total = i['Reps']
                    allstats[name] = total
                if allstats['food'] < foodgoal:
                    allotremaining = foodgoal - allstats['food']
                    msg = "Added to " + message.author.name + "'s workout sheet: **" + ate + "** for **" + str(foods[ate]) + "** points!"
                    msg = msg + "\nYou still have " + str(allotremaining) + " points left to eat!"
                elif allstats['food'] == foodgoal:
                    msg = "Added to " + message.author.name + "'s workout sheet: **" + ate + "** for **" + str(foods[ate]) + "** points!"
                    msg = "You hit your food goal, you _fool_!  Now you can't eat the rest of the day!"
                elif allstats['food'] > foodgoal:
                    msg = "Oh, hello fatso. You ate too much."
                    yay = gifrandom('fatso')
                    msg = msg + "\n" + yay
                await message.channel.send(msg)

        elif message.content.lower().startswith('!fatinfo'):
            """
                checking workout
            """
            getuser = message.author.name.lower()
            try:
                splitspace = message.content.lower().split(" ", 1)
                command = splitspace[1].split(" ")
                getuser = command[0]
            except Exception as e:
                pass
            try:
                getfatstats = getgsheet(workouttracksheet,getuser)
                allstats = {}
                for i in getfatstats:
                    name = i['Exercise']
                    total = i['Reps']
                    allstats[name] = total
                msg = "**PHAT STATS BRO:** \n```"
                msg = msg + "\n----\n"
                for name,total in allstats.items():
                    try:
                        if name in workouts.keys():
                            msg = msg + str(name) + ":\n   " + str(total) + "/" + str(workouts[name]) + "\n"
                        elif name == 'food':
                            msg = msg + str(name) + ":\n   " + str(total) + "/20\n"
                    except Exception as e:
                        print(e)
                        continue
                msg = msg + "```\n **STILL FAT BRO**"                
            except Exception as e:
                msg = "No user tracksheet data available for " + getuser
            await message.channel.send(msg)
        else:
            await message.channel.send("What're you looking for?  I have these fat options:\n`!fatinfo`\n`!fatadd`\n`!fatfood`\n`!fatweight`\n`!fatgoal`")
    if message.content.lower().startswith('qq'):
        print(message.guild.members)
        # workoutdata = { 
        #     "username": message.author.name, 
        #     "goals": {
        #         "pushups": 100,
        #         "pullups": 100,
        #         "situps": 100,
        #         "squats": 100,
        #         "weight": 190
        #         },
        #     "worksheet_tracking": "tracking",
        #     "worksheet_stats": "message.author.name"  
        # }

        # userfolder = get_user_folder(message.author.id)
        # workoutfile = check_user_json_file(userfolder,'workouts')
        # if workoutfile == True:
        #     workoutinfo = get_user_data(message.author.id,'workouts')
        #     if workoutinfo == False:
        #         create_user_json_data(message.author.id,'workouts',workoutdata)
        #         workoutinfo = get_user_data(message.author.id,'workouts')
        # await message.channel.send(workoutinfo['username'])


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
    check_watch_dir(WATCH_DIRECTORY)
    await asyncio.gather(asyncio.ensure_future(watch.run()))
client.run(TOKEN)


