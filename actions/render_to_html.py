#!/usr/bin/python3
# -*- coding: utf-8 -*-
import html
import datetime
import os

import re
import vk_api
from shutil import copyfile

from core.download import get_photo_attach, get_video_attach, IMAGE_PATTERN

try:
    import simplejson as json
except ImportError:
    import json

start_file = """
<!DOCTYPE html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link rel="stylesheet" type="text/css" href="styles.css" />
</head>

<body>
<div class="message_list">
"""

end_file = """
</div>
</body>
</html>
"""

message_template = """
<div class="message">
    <div class="avatar">
        <img width="32" height="32" src="{avatar}"/>
    </div>

    <div class="date right"><a name="{id}" href="http://vk.com/im?msgid={id}&amp;sel={sel}">#{id} {date}</a></div>
    <div class="username"><a href="http://vk.com/id{user_id}">{user_name}</a></div>

    <div class="left">
        <div class="body">{body}</div>

        <div class="attachments">
            {fwd}{attachments}
        </div>
    </div>
    <div class="clear"></div>
</div>
"""

fwd_template = """
<div class="fwd_message">
    <div class="avatar">
        <img width="32" height="32" src="{avatar}"/>
    </div>

    <div class="username username_fwd"><a href="http://vk.com/id{user_id}">{user_name}</a></div>
    <div class="date date_fwd"><a href="http://vk.com/im?msgid={id}&amp;sel={sel}">{date}</a></div>
    <div class="clear"></div>

    <div class="left">
        <div class="body">{body}</div>

        <div class="fwd_attachments">
            {fwd}{attachments}
        </div>
    </div>
    <div class="clear"></div>
</div>
"""

info_template = """
<div class="message">
    <a href="http://vk.com/im?sel={sel}">Link</a>
</div>
"""

photo_template = """
<div class="im-img"><a href="{fullsize}"><img src="{thumbnail}" /></a></div>
"""

video_template = """
<a href="{link}"><img src="{thumbnail}" /><br />{title} ({duration} sec)</a>
"""

CSS_FILE_PATH = './static/styles.css'


class Message(object):
    def __init__(self, raw, users, sel, photo_urls_path=None, template=message_template):
        self.raw = raw
        self.users = users
        self.sel = sel
        self.template = template
        self.photo_urls = photo_urls_path

    def get_body(self):
        body = html.escape(self.raw['body']).replace('\n', '<br/>')
        return body

    def __str__(self):
        try:
            if 'from_id' in self.raw:
                from_user = self.users[str(self.raw['from_id'])]
            elif 'user_id' in self.raw:
                from_user = self.users[str(self.raw['user_id'])]
        except:
            from_user = {
                'photo_50': 'http://vk.com/images/deactivated_c.gif',
                'id': '0',
                'first_name': 'DELETED',
                'last_name': ''
            }

        date = datetime.datetime.fromtimestamp(self.raw['date'])
        fwd_messages = []

        for i in self.raw.get('fwd_messages', []):
            fwd_messages.append(Message(i, self.users, self.sel, self.photo_urls, fwd_template))

        attachments = []

        for attach in self.raw.get('attachments', ()):
            if attach['type'] == 'photo':
                photo = get_photo_attach(attach['photo'])
                # 2. save only vk photos
                # if self.photo_urls:
                #     if photo['fullsize'] in self.photo_urls:
                #         cached = '../' + self.photo_urls[photo['fullsize']]
                #         photo = {'thumbnail': cached, 'fullsize': cached}
                attachments.append(
                    photo_template.format(**photo)
                )
            elif attach['type'] == 'video':
                video = get_video_attach(attach['video'])
                attachments.append(
                    video_template.format(**video)
                )
            else:
                attachments.append('<div>{}</div>'.format(attach['type']))

        values = {
            'id': self.raw.get('id', ''),
            'sel': self.sel,
            'avatar': from_user['photo_50'],
            'date': date.strftime('%d.%m.%Y %H:%M'),
            'user_id': from_user['id'],
            'user_name': ' '.join([from_user['first_name'],
                                   from_user['last_name']]),
            'body': self.get_body(),
            'attachments': ''.join(attachments),
            'fwd': '\n'.join(str(i) for i in fwd_messages)
        }

        return self.template.format(**values)


class Main(object):
    def __init__(self):
        self.vk = vk_api.VkApi()

        self.users = {}

    def render(self, target_dir, dump):
        if dump['items']:
            last_timestamp = max(map(lambda item: item['date'], dump['items']))
            last_datetime = str(datetime.datetime.fromtimestamp(last_timestamp)).replace(':', '-')
        else:
            last_datetime = 'never'

        if str(dump['id']) in self.users:
            user = self.users[str(dump['id'])]
            filename = '{0}/{1} {2} {3} [{4}].html'.format(
                target_dir, last_datetime, user['first_name'], user['last_name'], user['id'])
        else:
            filename = '{0}/{1} {2}.html'.format(target_dir, last_datetime, dump['id'])

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(start_file)
            f.write(info_template.format(sel=dump['sel']))

            for i in dump['items']:
                message = Message(i, self.users, dump['sel'], self.photo_urls)
                f.write(str(message))  # .encode('utf-8', errors='replace').decode("utf-8"))

            f.write(end_file)

    def run(self):
        dumps_dir = './dumps/'
        listdir = os.listdir(dumps_dir)

        if len(listdir) == 1:
            idx = 1
        else:
            print('\nВыберите пользователя:')
            for x, item in enumerate(listdir, 1):
                print('{}. {}'.format(x, item))

            idx = int(input('> '))

        owner_dir = os.path.join(listdir[idx - 1], 'conversations')
        target_dir = os.path.join('./html/', owner_dir)
        os.makedirs(target_dir, exist_ok=True)
        copyfile(CSS_FILE_PATH, target_dir + '/styles.css')

        self.path = os.path.join(dumps_dir, owner_dir)

        self.photo_urls = None

        print('Selected {}'.format(self.path))

        for dir_name in os.listdir(self.path):
            print('Render %s' % dir_name)

            photo_urls_path = os.path.join(self.path, dir_name, 'photo_urls.json')
            if os.path.exists(photo_urls_path):
                with open(photo_urls_path, 'r', encoding='utf-8') as f:
                    self.photo_urls = json.load(f)

            with open(os.path.join(self.path, dir_name, 'im.json'), 'r', encoding='utf-8') as f:
                # 1. save all images
                json_str = f.read().replace('\n', '')
                image_urls = re.findall(IMAGE_PATTERN, json_str)
                for image_url in image_urls:
                    if image_url in self.photo_urls:
                        json_str = json_str.replace(
                            image_url,
                            os.path.join('..', '..', '..', self.photo_urls[image_url]).replace('\\', '/'))

            dump = json.loads(json_str)
            self.users = dump['users']

            if dump['id'] > 2e9:
                sel = "c%s" % (dump['id'] - 2e9)
            else:
                sel = dump['id']

            dump.update({'sel': sel})

            self.render(target_dir, dump)

        print("\nВаши диалоги готовы. Перейдите в папку " + target_dir + " или вбейте в браузер")
        print("file://" + os.path.abspath(target_dir))


def render_to_html():
    """Отрисовать диалоги"""
    main = Main()
    main.run()
