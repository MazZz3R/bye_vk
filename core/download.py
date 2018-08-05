"""
Thanks to https://github.com/Rast1234/vkd/blob/master/Download.py
"""
import json
import os
from os.path import join, exists, isfile, splitext
import sys
import logging
from os import makedirs
import re

try:
    import urllib2

    urlopen = urllib2.urlopen
    from urllib import urlencode
except ImportError:
    from urllib.request import urlopen
    import urllib.parse

    urlencode = urllib.parse.urlencode

PHOTO_SIZES = (
    'photo_75', 'photo_130', 'photo_604',
    'photo_807', 'photo_1280', 'photo_2560'
)

IMAGE_PATTERN = re.compile(
    'https?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|jpeg|gif|png|tiff|bmp|svg|xbm)',  # (?:\?ava=1)?',
    re.IGNORECASE)
#   |- proto -|--------- domain -----------|--- path ---|-------------- extension -------------|--- params ?ava=1 ---|


def download(url_list, root_dir):
    url_to_filename = dict()

    for url, name, subdir in url_list:
        if name is None:
            name = url.split('/')[-1]
        filename = join(root_dir, subdir, name)
        makedirs(join(root_dir, subdir), exist_ok=True)
        try:
            u = urlopen(url)
        except OSError:
            continue

        # file might exist, so add (1) or (2) etc
        counter = 1
        if exists(filename) and isfile(filename):
            name, ext = splitext(filename)
            filename = name + " ({})".format(counter) + ext
        while exists(filename) and isfile(filename):
            counter += 1
            name, ext = splitext(filename)
            filename = name[:-4] + " ({})".format(counter) + ext
        logging.info(u"Start dl: {}".format(filename))
        f = open(filename, 'wb')
        meta = u.info()
        file_size = int(meta.get_all("Content-Length")[0])
        sys.stdout.write("Downloading: %s (%s kb)\n" % (filename.encode('ascii', 'ignore'), file_size / 1024))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1)
            sys.stdout.write(status)

        f.close()
        logging.info(u" End  dl: {}".format(filename))
        url_to_filename[url] = filename

    return url_to_filename


def get_photo_attach(photo):
    thumbnail = photo['photo_130']
    fullsize = None

    for i in PHOTO_SIZES[::-1]:
        if i in photo:
            fullsize = photo[i]
            break

    return {'thumbnail': thumbnail, 'fullsize': fullsize}


def get_video_attach(video):
    thumbnail = video['photo_130']

    for i in PHOTO_SIZES[::-1]:
        if i in video:
            thumbnail = video[i]
            break
    link = 'https://vk.com/video%d_%d' % (video['owner_id'], video['id'])
    title = video['title']
    duration = video['duration']
    return {'thumbnail': thumbnail, 'link': link, 'title': title,
            'duration': duration}


def escape(name):
    """Escape the filename"""
    result = str(re.sub('[^+=\-()$!#%&,.\w\s]', '_', name, flags=re.UNICODE).strip())
    # print("\t{}\n\t{}".format(name, result))
    return result[:250]


def download_all_photos(path, wall):
    # 1. save all images
    photo_urls = list(map(
        lambda url: (url, url.split('/')[-1], '',),
        re.findall(IMAGE_PATTERN, json.dumps(wall))
    ))
    # 2. save only vk photos
    # for post in wall["items"]:
    #     if "attachments" not in post:
    #         continue
    #     for attach in post["attachments"]:
    #         if attach["type"] == "photo":
    #             url_to_download = get_photo_attach(attach["photo"])['fullsize']
    #             photo_urls.append((url_to_download, url_to_download.split('/')[-1], ''))
    url_to_filename = download(photo_urls, os.path.join(path, 'photos'))
    url_path = os.path.join(path, 'photo_urls.json')
    with open(url_path, 'w', encoding='utf-8') as f:
        json.dump(url_to_filename, f, separators=(',', ':'), ensure_ascii=False)
