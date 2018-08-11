import datetime
import json
import os
import threading
from urllib.request import urlopen, Request
from uuid import getnode as get_mac

from core.path_helper import data_path
from settings import VERSION

FIREBASE_URL = 'https://byevk0.firebaseio.com/'
LAUNCHED_FILE = data_path('.launched')


def send_stats():

    base_url = '%s/users/%s/' % (FIREBASE_URL, get_mac())
    now = str(datetime.datetime.utcnow()).split('.')[0]

    if not os.path.isfile(LAUNCHED_FILE):
        url = base_url + 'first_launch.json'
        payload = {now: VERSION}
        os.makedirs(data_path('.'), exist_ok=True)
        open(LAUNCHED_FILE, 'a').close()
    else:
        url = base_url + 'launches.json'
        payload = {now: VERSION}

    req = Request(url,
                  data=json.dumps(payload).encode('utf8'),
                  headers={'content-type': 'application/json'})
    req.get_method = lambda: 'PATCH'
    # Not in the MainThread!
    threading.Thread(target=urlopen, args=(req,), daemon=True).start()
