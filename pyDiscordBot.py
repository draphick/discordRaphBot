# Work with Python 3.7
# Migration commands: https://discordpy.readthedocs.io/en/latest/migrating.html
import discord
import requests
import urllib3
import json
import random
import re
from bs4 import BeautifulSoup
from googletrans import Translator
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from dotenv import load_dotenv

load_dotenv()
if os.environ['debug'] == "y":
    # Dev
    TOKEN = os.getenv('DISCORD_TOKEN_DEV')
    tagalogsheet = os.getenv('testsheet')
    gastracksheet = os.getenv('testsheet')
    addtracksheet = os.getenv('testsheet')
    workouttracksheet = os.getenv('workouttracksheet')
else:
    # PROD
    TOKEN = os.getenv('DISCORD_TOKEN_PROD')
    tagalogsheet = os.getenv('tagalogsheet')
    gastracksheet = os.getenv('gastracksheet')
    addtracksheet = os.getenv('addtracksheet')
    workouttracksheet = os.getenv('workouttracksheet')

botlink = os.getenv('botlink')
sonarrapi = os.getenv('sonarrapi')
sonarrbaseapi = os.getenv('sonarrbaseapi')
radarrapi = os.getenv('radarrapi')
radarrbaseapi = os.getenv('radarrbaseapi')
imgurauth = os.getenv('imgurauth')
requestbotid = os.getenv('requestbotid')
ownerid = os.getenv('ownerid')
giphyapi = os.getenv('giphyapi')

translator = Translator(service_urls=[
    'translate.google.com',
    'translate.google.tl',
])

urllib3.disable_warnings()
client = discord.Client()
authstuff = {'Authorization':'Client-ID ' + imgurauth}

def getalbum(endpoint):
    albumimages = {}
    r = requests.get(endpoint, verify=False, headers=authstuff)
    albumlist = json.loads(r.text)
    for x in albumlist['data']:
        emote = x['description']
        link = x['link']
        albumimages.update({emote:link})
    return albumimages

def getlist(endpoint):
    albumimages = {}
    r = requests.get(endpoint, verify=False)
    wordlistraw = json.loads(r.text)
    allwords = wordlistraw['words']
    draw = random.choice(allwords)
    return draw

def getplex(title, showmovie, year = None):
    answer = {}
    if showmovie == 'show':
        r = requests.get(sonarrbaseapi + sonarrapi , verify=False)
    elif showmovie == 'movie':
        r = requests.get(radarrbaseapi + radarrapi , verify=False)
    else:
        return
    allplex = json.loads(r.text)
    counter = 0
    for x in allplex:
        if title.lower() in re.sub(r'\W+', ' ',x['title'].lower()):
            if showmovie == 'show':
                counter = counter + 1
                newtitle = x['title'] + " on " + x['network'] + ' \n_' + str(x['episodeFileCount']) + " episode(s) already downloaded_"
                answer.update({counter:newtitle})
            if showmovie == 'movie' and year == x['year']:
                counter = counter + 1
                if x['downloaded']:
                    newtitle = x['title'] + ' (' + str(x['year']) + ')' + ' _is already downloaded._'
                    answer.update({counter:newtitle})
                else:
                    newtitle = x['title'] + ' (' + str(x['year']) + ')' + ' _is waiting to download._'
                    answer.update({counter:newtitle})
    return(answer)

def googleauth(sheet,sheettab = 'Sheet1'):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('cred_file.json', scope)
    gclient = gspread.authorize(creds)
    sheet = gclient.open(sheet).worksheet(sheettab)
    return(sheet)

def getrow(more,total,sheet,sheettab = 'Sheet1'):
    sheet = googleauth(sheet,sheettab)
    if more == 'last':
        returnrow = {}
        lastrowemptyrow = sheet.row_count
        lastrow = lastrowemptyrow -1
        maxrow = lastrow - total
        while maxrow < lastrow:
            rowvalue = sheet.row_values(lastrow)
            returnrow.update({lastrow:rowvalue})
            lastrow = lastrow - 1
        return(returnrow)
    elif more == 'only':
        returnrow = {}
        rowvalue = sheet.row_values(total)
        returnrow.update({total:rowvalue})
        return(returnrow)


def updatecell(row,column,value,sheet):
    sheet = googleauth(sheet)

    if column.lower() == 'date':
        col = 1
    elif column.lower() == 'time':
        col = 2
    elif column.lower() == 'food':
        col = 3
    elif column.lower() == 'drink':
        col = 4
    elif column.lower() == 'dosage':
        col = 5
    elif column.lower() == 'mr':
        col = 6
    elif column.lower() == 'duration':
        col = 7
    elif column.lower() == 'notes':
        col = 8

    sheet.update_cell(row,col,value)

def writerow(col1 = None, col2 = None, col3 = None, col4 = None, col5 = None, col6 = None, col7 = None, col8 = None, sheet = 'testsheet', sheettab = 'Sheet1'):
    sheet = googleauth(sheet,sheettab)

    if col1 == 'now':
        col1 = datetime.date.today().strftime("%Y/%m/%d")
    if col2 == 'now':
        col2 = datetime.datetime.now().strftime("%H:%M")
    lastrow = sheet.row_count
    rowdata = [col1, col2, col3, col4, col5, col6, col7, col8]
    sheet.insert_row(rowdata, lastrow, value_input_option='USER_ENTERED')
    data = sheet.row_values(lastrow)    

def acnhsearch(searchterm):
    search = searchterm.replace(" ", "+")
    url = "https://villagerdb.com/search?game=nh&q=" + search
    itemdata = {}
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'lxml')
    allresults = soup.find("div",{"id":"entity-browser"})["data-initial-state"]
    jsonresults = json.loads(allresults)
    totalcount = jsonresults['totalCount']
    maxresults = 5
    counter = 0
    for i in jsonresults['results']:
        if counter < maxresults:
            counter = counter + 1
            name = i['name']
            url = "https://villagerdb.com" + i['url']
            # thumb = "https://villagerdb.com" + i['image']['thumb']
            itemdata[name] = {}
            itemdata[name]['Website Link'] = url
            # itemdata[name]['Image'] = thumb            
    return itemdata
   
def acnhget(searchterm):
    search = searchterm.replace(" ", "-")
    url = "https://villagerdb.com/item/" + search
    r = requests.get(url, verify=False)
    if r.status_code == 404:
        itemdata = acnhsearch(searchterm)
    else: 
        itemdata = {}
        soup = BeautifulSoup(r.text, 'lxml')
        namespace = soup.select("h1")[0].text.strip()
        itemdata[namespace] = {}
        tab = soup.find("table",{"class":"table item-game-data"}).select("tbody tr")
        # imagebloc = soup.find("div",{"class":"entity-dropdown-init d-inline-block"})["data-image"]
        # jsonresults = json.loads(imagebloc)
        itemdata[namespace]['Website Link'] = url
        # itemdata[namespace]['Image'] = "https://villagerdb.com" + jsonresults['thumb']
        for row in tab:
            line = row.select("td")
            col1 = line[0].text.strip()
            itemdata[namespace][col1] = []
            if line[1].select("li, div"):
                for data in line[1].select("li, div"):
                    value = data.text.strip().replace("  ", "").replace("\n","")
                    itemdata[namespace][col1].append(value)
            else:
                value = line[1].text
                itemdata[namespace][col1].append(value)
    return itemdata

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

    # if all(c in "lo" for c in message.content.lower()):
    #     """
    #         If someone sends a message of only l and o
    #         such as LOLLLOLOLLOLOL
    #         or LOLLLLLL
    #         or LOL
    #         it will send a random giphy searching rofl or lol
    #     """
    #     searchterms = ['rofl', 'lol','laughing']
    #     search = random.choice(searchterms)
    #     allurls = []
    #     allrofl = requests.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=' + giphyapi + '&limit=10', verify=False)
    #     allgifs = allrofl.json()
    #     allgifs = allgifs['data']
    #     for gif in allgifs:
    #         allurls.append(gif['url'])
    #     rofl = random.choice(allurls)
    #     if not isinstance(message.channel, discord.abc.PrivateChannel):
    #         await message.delete()
    #     await message.channel.send(message.author.mention + " IS LAUGHING!!!")
    #     await message.channel.send(rofl)
    #     del allrofl

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

    rollregex = re.compile('^[d][0-9]{1,5}$')
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
    
    if message.content.lower().startswith('addtrack '):
        """
            This is used to quickly track some meds when I take them.
        """
        splitspace = message.content.lower().split(" ", 1)
        command = splitspace[1].split(" ", 1)
        if len(command) == 2:
            args = command[1].split("#")
            if 'add' in command:
                if len(args) != 8:
                    await message.channel.send("Invalid amount of columns, try again!  Remember these columns: ```\ndate\ntime\nfood\ndrink\ndosage\nmr\nduration\nnotes```")
                else:                    
                    writerow(args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],addtracksheet)
                    await message.channel.send("New row added!\n `addtrack view last#1` to check it out!")
                    allrows = getrow("last",1,addtracksheet)
                    for key,value in allrows.items():
                            await message.channel.send("Row: " + str(key) + "\n-- " + str(value))                            
            elif 'view' in command:
                if len(args) != 2:
                    await message.channel.send("Too many / not enough arguments.  Ex: \n`addtrack view only#26` \n`addtrack view last#5`")
                else:
                    allrows = getrow(args[0],int(args[1]),addtracksheet)
                    for key,value in allrows.items():
                        await message.channel.send("Row: " + str(key) + "\n-- " + str(value))
            elif 'update' in command:
                if len(args) != 3:
                    await message.channel.send("Too many / not enough arguments, you need to provide `sheet update row#columnname#newvlue`")
                updatecell(int(args[0]),args[1],args[2],addtracksheet)
                await message.channel.send("Update sent!")
                allrows = getrow("only",int(args[0]),addtracksheet)
                for key,value in allrows.items():
                        await message.channel.send("Row: " + str(key) + "\n-- " + str(value))
            else:
                await message.channel.send("Did you want to add, view, or update?\n If using `udpate` make sure to provide one of the columns:```\ndate\ntime\nfood\ndrink\ndosage\nmr\nduration\nnotes```")
        else:
            if 'one' in command:          
                writerow('now','now','none','water','15',None,None,None,addtracksheet)
                await message.channel.send("New row added!\n `addtrack view last#1` to check it out!")
                allrows = getrow("last",1,addtracksheet)
                for key,value in allrows.items():
                        await message.channel.send("Row: " + str(key) + "\n-- " + str(value))
            else:
                await message.channel.send("Did you want to add, view, or update?\n If using `udpate` make sure to provide one of the columns:```\ndate\ntime\nfood\ndrink\ndosage\nmr\nduration\nnotes```")

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

    if message.content.lower().startswith('!fatadd'):
        """
            doing some workout tracking
            gsheet query:
            ={
                QUERY(
                    RaphTracking!$A$1:$D,
                    "select C, sum(D) where C is not null and A = date '"&TEXT(TODAY(),"yyyy-mm-dd")&"' group by C order by sum(D) desc label sum(D) 'Reps'",
                    1
                )
            }
        """
        splitspace = message.content.lower().split(" ", 1)
        command = splitspace[1].split(" ")
        workouts = [
            "pushups",
            "situps",
            "squats",
            "pullups",
            "weight"
        ]
        if len(command) == 2:
            if command[0] not in workouts:
                await message.channel.send("Wrong workout type")
            else:
                writerow("now","now",command[0], command[1], None, None, None, None,workouttracksheet,message.author.name.lower() + "tracking")
                await message.channel.send("Adding to " + message.author.name + "s workout sheet " + str(command[1]) + " " + command[0])
        else:
            await message.channel.send("Missing or too many arguments.  Provide a workout type and value\n Example: `!fatadd pushup 5` \n Available workout types: pushups, pullups, situps, squats")

    if message.content.lower().startswith('!fatinfo'):
        """
            checking workout
        """
        allrows = getrow("last",5,workouttracksheet,message.author.name.lower())
        msg = "**FAT STATS BRO:** \n```"
        msg = msg + "\nExercise || Reps\n"
        for key,value in allrows.items():
            try:
                msg = msg + str(allrows[key][0]) + ":\n   " + str(allrows[key][1]) + "\n"
            except Exception as e:
                continue
        msg = msg + "```\n **STILL FAT BRO**"
        await message.channel.send(msg)

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

client.run(TOKEN)
