from pyFuncs import *


class OnMyWatch:
    def __init__(self):
        self.observer = Observer()

    async def run(self):
        evh = Handler()
        watch = AIOWatchdog(WATCH_DIRECTORY, event_handler=evh)
        watch.start()
        print ("Observer started.  Watching: " + WATCH_DIRECTORY)
        try:
            while True:
                await asyncio.sleep(1)
        except:
            watch.stop()
            print("Observer Stopped")

class Handler(AIOEventHandler):
    """Subclass of asyncio-compatible event handler."""

    paths_changed:list = []

    async def on_created(self, event):
        print('Created:', event.src_path)  # add your functionality here

    async def on_deleted(self, event):
        print('Deleted:', event.src_path)  # add your functionality here

    async def on_moved(self, event):
        print('Moved:', event.src_path)  # add your functionality here

    async def on_modified(self, event):
        global client
        print('Modified:', event.src_path)  # add your functionality here
        if not event.is_directory:

            if event.src_path in self.paths_changed:
                self.paths_changed.remove(event.src_path)
            else:
                self.paths_changed.append(event.src_path)

                await asyncio.sleep(1)
                if event.src_path in self.paths_changed:
                    self.paths_changed.remove(event.src_path)

def check_watch_dir(users_path):
    if not os.path.exists(users_path):
        print("Watch dir missing.\nCreating: " + users_path)
        os.mkdir(users_path)
    else:
        print(users_path + " already exists.")

def get_user_folder(userID):
    user_data_path = WATCH_DIRECTORY + str(userID)
    if not os.path.exists(user_data_path):
        os.mkdir(user_data_path)
    return user_data_path
def check_user_json_file(userfolder,fileName):
    user_json_path = userfolder + "/" + fileName + ".json"
    if not os.path.exists(user_json_path):
        open(user_json_path, 'a').close()
    return True
def create_user_json_data(userID,fileName,datadump):
    user_data_path = WATCH_DIRECTORY + str(userID)
    user_json_path = user_data_path + "/" + fileName + ".json"    
    jsonload = json.dumps(datadump)
    with open(user_json_path, 'w') as jsonfile:
        jsonfile.write(jsonload)
        jsonfile.close()

def get_user_data(userID,fileName):
    user_data_path = WATCH_DIRECTORY + str(userID) + '/' + fileName + '.json'
    try:
        with open(user_data_path, 'r') as jsonfile:
            user_info = json.load(jsonfile)
            jsonfile.close()
    except Exception as e:
        print("load_user_info error occurred loading json " + str(e))
        return False
    return user_info


def update_user_data(userID,fileName,user_data):
    user_data_path = WATCH_DIRECTORY + str(userID) + '/' + fileName + '.json'
    with open(user_data_path, 'w+') as jsonfile:
        json.dump(user_data, jsonfile, indent=4, sort_keys=True)
        jsonfile.close()
