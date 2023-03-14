# Work with Python 3.7
# Migration commands: https://discordpy.readthedocs.io/en/latest/migrating.html
import discord
import requests
import urllib3
import json
import random
import re
import asyncio
from bs4 import BeautifulSoup
from googletrans import Translator
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from hachiko.hachiko import AIOWatchdog, AIOEventHandler
client = discord.Client()

load_dotenv()
if os.environ['debug'] == "y":
    # Dev
    TOKEN = os.getenv('DISCORD_TOKEN_DEV')
    tagalogsheet = os.getenv('testsheet')
    gastracksheet = os.getenv('testsheet')
    addtracksheet = os.getenv('testsheet')
    workouttracksheet = os.getenv('workouttracksheet')
    WATCH_DIRECTORY = os.getenv('WATCH_DIRECTORY')
else:
    # PROD
    TOKEN = os.getenv('DISCORD_TOKEN_PROD')
    tagalogsheet = os.getenv('tagalogsheet')
    gastracksheet = os.getenv('gastracksheet')
    addtracksheet = os.getenv('addtracksheet')
    workouttracksheet = os.getenv('workouttracksheet')
    WATCH_DIRECTORY = os.getenv('WATCH_DIRECTORY')
    
botlink = os.getenv('botlink')
sonarrapi = os.getenv('sonarrapi')
sonarrbaseapi = os.getenv('sonarrbaseapi')
radarrapi = os.getenv('radarrapi')
radarrbaseapi = os.getenv('radarrbaseapi')
imgurauth = os.getenv('imgurauth')
requestbotid = os.getenv('requestbotid')
ownerid = os.getenv('ownerid')
giphyapi = os.getenv('giphyapi')
rollregex = re.compile('^[d][0-9]{1,5}$')
authstuff = {'Authorization':'Client-ID ' + imgurauth}

translator = Translator(service_urls=[
    'translate.google.com',
    'translate.google.tl',
])

urllib3.disable_warnings()

def gifrandom(search):
    allurls = []
    allrofl = requests.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=' + giphyapi + '&limit=10', verify=False)
    allgifs = allrofl.json()
    allgifs = allgifs['data']
    for gif in allgifs:
        allurls.append(gif['url'])
    rofl = random.choice(allurls)
    return rofl

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
                answer.update({counter: newtitle})
            if showmovie == 'movie' and year == x['year']:
                counter = counter + 1
                if x['downloaded'] == "true":
                    newtitle = x['title'] + ' (' + str(x['year']) + ')' + ' _is already downloaded._'
                    answer.update({counter: newtitle})
                else:
                    newtitle = x['title'] + ' (' + str(x['year']) + ')' + ' _is waiting to download._'
                    answer.update({counter: newtitle})
    return(answer)

def googleauth(sheet,sheettab = 'Sheet1'):
    # https://gspread.readthedocs.io/en/latest/
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('cred_file.json', scope)
    gclient = gspread.authorize(creds)
    spreadsheet = gclient.open(sheet)
    allsheets = [i.title for i in spreadsheet.worksheets()]
    if sheettab in allsheets:
        sheet = spreadsheet.worksheet(sheettab)
    else:
        sheet = spreadsheet.add_worksheet(title=sheettab, rows="1", cols="8") 
    return(sheet)

def getrow(more,total = None,sheet = None,sheettab = 'Sheet1'):
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
    elif more == 'all':
        rowvalue = sheet.get_all_values()
        return(rowvalue)

def getgsheet(sheet = 'testsheet',sheettab = 'Sheet1',row = None, last = False):
    sheet = googleauth(sheet,sheettab)
    if row:
        if last:
            # This will return the last written row as a list
            # ie: ['2020/06/10', '10:03', 'none', 'water', '15']
            allcolvalues = list(filter(None, sheet.col_values(1)))
            lastrownum = str(len(allcolvalues))
            rowvalue = sheet.row_values(lastrownum)
        else:
            # This will return the row requested as a list
            # ie: ['2020/06/10', '10:03', 'none', 'water', '15']
            rowvalue = sheet.row_values(row)
    else:
        # This will return an array of dictionaries using the header row (row 1) as the key and the column values as the values
        # ie: 
        # [
        #     {
        #         'date': 'today', 
        #         'time': 'now', 
        #         'action': 'sit', 
        #         'result': 'sat', 
        #         '': ''
        #         }, 
        #     {
        #         'date': 'tomorrow', 
        #         'time': 'later', 
        #         'action': 'stand', 
        #         'result': 'standing', 
        #         '': ''
        #         }
        # ]
        rowvalue = sheet.get_all_records()
    return(rowvalue)
    

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