#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import html
import os
import re
import webbrowser
from shutil import copyfile
from typing import List

import vk_api

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


def get_conversations_raw_html(conversations: List) -> str:
    conversation_divs = ''

    for conversation in conversations:
        conversation_divs += f'''
        <div class="conversation">
            <div class="avatar_conversations">
                <img src="{conversation['cover']}">
            </div>
            <div class="date right">{datetime.datetime.fromtimestamp(
                conversation['date']).strftime('%H:%M %d-%B-%Y ')}</div>
            <div class="username"><a href="{conversation['html_filename']}">{conversation['name']}</a></div>

            <div class="left">
                <div class="body">{conversation['body']}</div>
        
                <div class="attachments">
                    
                </div>
            </div>
            <div class="clear"></div>
        </div>
        '''

    return f"""
<!DOCTYPE html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link rel="stylesheet" type="text/css" href="styles.css" />
</head>

<body>
<div class="message_list">
    {conversation_divs}
</div>
</body>
</html>
"""


def render_conversations_page(conversations_data, target_dir) -> str:
    conversations = []
    for user, last_message, html_filename in sorted(
            conversations_data,
            key=lambda c: -c[1]['date'] if c[1] else 0):
        if 'type' in user and user['type'] == 'chat' and 'title' in user:
            name = user['title']
        elif 'first_name' in user:
            name = user['first_name'] + ' ' + user['last_name']
        else:
            name = 'Error'

        conversations.append({
            'cover': extract_cover_photo(user),
            'name': name,
            'date': last_message['date'],
            'body': last_message['body'],
            'html_filename': html_filename
        })
    conversations_html = os.path.join(target_dir, 'conversations.html')
    with open(conversations_html, 'w', encoding='utf-8') as f:
        f.write(get_conversations_raw_html(conversations))
    return conversations_html


class Main(object):
    def __init__(self):
        self.vk = vk_api.VkApi()

        self.users = {}

    def render(self, target_dir, dump) -> str:
        if dump['items']:
            last_timestamp = max(map(lambda item: item['date'], dump['items']))
            last_datetime = str(datetime.datetime.fromtimestamp(last_timestamp)).replace(':', '-')
        else:
            last_datetime = 'never'

        if str(dump['id']) in self.users:
            user = self.users[str(dump['id'])]
            if 'type' in user and user['type'] == 'chat':
                filename = '{0} {1} [c{2}].html'.format(
                    last_datetime, user['title'], user['id'])
            else:
                filename = '{0} {1} {2} [{3}].html'.format(
                    last_datetime, user['first_name'],
                    user['last_name'], user['id'])
        else:
            filename = '{0} {1}.html'.format(last_datetime, dump['id'])

        with open(os.path.join(target_dir, filename), 'w', encoding='utf-8') as f:
            f.write(start_file)
            f.write(info_template.format(sel=dump['sel']))

            for i in dump['items']:
                message = Message(i, self.users, dump['sel'], self.photo_urls)
                f.write(str(message))  # .encode('utf-8', errors='replace').decode("utf-8"))

            f.write(end_file)
        return filename

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

        conversations_data = []

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

            html_filename = self.render(target_dir, dump)

            conversations_data.append((
                dump['users'][str(dump['id'])],
                dump['items'][-1] if len(dump['items']) > 0 else None,
                html_filename,
            ))

        conversations_html = render_conversations_page(conversations_data, target_dir)
        webbrowser.open(conversations_html)
        print("\nВаши диалоги готовы. См папку " + target_dir)


def extract_cover_photo(user_or_chat):
    for key in ['photo_200', 'photo_100', 'photo_50']:
        if key in user_or_chat:
            return user_or_chat[key]
    return 'http://vk.com/images/deactivated_c.gif'


def render_to_html():
    """Отрисовать диалоги"""
    main = Main()
    main.run()
