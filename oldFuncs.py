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
        getuser = message.author.name.lower()
        print(getuser + " ran a fat command " + message.content.lower())
        print(str(datetime.datetime.now().strftime("%H:%M:%S")))

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
                msg = "You've reset your reported weight gain/loss preference.  Your secret is safe with me!"
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
                command = splitspace[1]
                getuser = command
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
            msg = """What're you looking for?  I have these fat options:
            `!fatinfo` - Get your current stats
            `!fatadd {workoutname}` - Add to your current workouts
            `!fatfood {s|m|l}` - Add some food you ate
            `!fatweight {gain|loss}` - Setup your current weight goal (to gain weight or lose weight)
            `!fatgoal {add|remove|view} {workoutname} {goal}` - Add/remove/view your current workout goals."""
            await message.channel.send(msg)
        print(getuser + " finished a fat command " + message.content.lower())
        print(str(datetime.datetime.now().strftime("%H:%M:%S")))