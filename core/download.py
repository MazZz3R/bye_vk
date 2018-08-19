"""
Thanks to https://github.com/Rast1234/vkd/blob/master/Download.py
"""
import json
import logging
import os
import random
import re
import sys
from os import makedirs
from os.path import join, exists, isfile
from typing import Dict, Tuple, List

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

CONSOLE_LENGTH = 79
PROGRESS_SCALE_PHOTO = 'Скачивание фотографий из '
PROGRESS_SCALE_DOCS = 'Скачивание документов типа '
PROGRESS_STRING = '0 % ............. 25 % ............. 50 % .............. 75 % ........... 100 %'


def download_photo(url_list, root_dir, photo_source_genitive):
    sys.stdout.write(PROGRESS_SCALE_PHOTO + photo_source_genitive + '\n')
    return download_files(root_dir, url_list)


def download_docs(url_list, root_dir: str, doc_type: str):
    sys.stdout.write(PROGRESS_SCALE_DOCS + doc_type + '\n')
    return download_files(root_dir, url_list)


# returns dict {url: saved_path}
def download_files(root_dir: str, url_list: List[Tuple[str, str, str]]) -> Dict[str, str]:
    url_to_filename = dict()
    urls_count = len(url_list)
    processed_count = 0
    printed_char_idx = -1

    for url, name, subdir in url_list:
        target_char_idx = (CONSOLE_LENGTH * processed_count) // urls_count
        while printed_char_idx < target_char_idx:
            printed_char_idx += 1
            sys.stdout.write(PROGRESS_STRING[printed_char_idx])
            sys.stdout.flush()

        # if name is None:
        #     name = url.split('/')[-1]
        name = escape(url if not name else name)
        filename = join(root_dir, subdir, name)
        makedirs(join(root_dir, subdir), exist_ok=True)

        if exists(filename) and isfile(filename):
            # print('pass ' + filename)
            url_to_filename[url] = filename
            processed_count += 1
            continue
        # Uncomment to force downloading
        # counter = 1
        # # file might exist, so add (1) or (2) etc
        # if exists(filename) and isfile(filename):
            # name, ext = splitext(filename)
            # filename = name + " ({})".format(counter) + ext
        # while exists(filename) and isfile(filename):
        #     counter += 1
        #     name, ext = splitext(filename)
        #     filename = name[:-4] + " ({})".format(counter) + ext
        try:
            u = urlopen(url)
        except OSError:
            continue

        logging.info(u"Start dl: {}".format(filename))
        try:
            f = open(filename, 'wb')
            meta = u.info()
            file_size = int(meta.get_all("Content-Length")[0])
            logging.debug("Downloading: %s (%s kb)\n" % (filename.encode('ascii', 'ignore'), file_size / 1024))

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                # status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                # status = status + chr(8) * (len(status) + 1)
                # sys.stdout.write(status)

            f.close()
            logging.info(u" End  dl: {}".format(filename))
            url_to_filename[url] = filename
            processed_count += 1
        except BaseException as ex:
            logging.error("Error " + filename)
            logging.error(str(ex))

    while printed_char_idx < CONSOLE_LENGTH - 1:
        printed_char_idx += 1
        sys.stdout.write(PROGRESS_STRING[printed_char_idx])
    sys.stdout.write('\n')
    sys.stdout.flush()
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


KEEP_CHARS = (' ', '.', '_')


def escape(name, with_hash=False):
    """Escape the filename"""
    # result = str(re.sub('[^+=\-()$!#%&,.\w\s]', '_', name, flags=re.UNICODE).strip())
    result = "".join(c for c in name if c.isalnum() or c in KEEP_CHARS).rstrip()
    if with_hash:
        result += '%08x' % random.randrange(16 ** 8)
    # print("\t{}\n\t{}".format(name, result))
    return result[:250]


def download_all_photos(path, wall, photo_source_genitive):
    # 1. save all images
    photo_urls = list(map(
        lambda url: (url, None, '',),
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
    url_to_filename = download_photo(photo_urls, os.path.join(path, 'photos'), photo_source_genitive)
    url_path = os.path.join(path, 'photo_urls.json')

    saved_url_to_filename = dict()

    if os.path.exists(url_path) and os.path.isfile(url_path):
        with open(url_path, 'r', encoding='utf-8') as f:
            saved_url_to_filename = json.load(f)

    for url, filename in url_to_filename.items():
        saved_url_to_filename[url] = filename

    with open(url_path, 'w', encoding='utf-8') as f:
        json.dump(saved_url_to_filename, f,
                  separators=(',', ':'), ensure_ascii=False)
