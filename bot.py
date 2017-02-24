#!/usr/bin/python
# -*- coding: utf-8 -*-

from gmailapi import GmailApi
import json
import sys
import base64
from slackclient import SlackClient
from consts import (
    SLACK_TOKEN,
    JSON_PATH,
    USERNAME,
    CHANNEL,
    EMOJI,
    QUERY
)


def get_mail():
    f = open(JSON_PATH)
    auth_info = json.load(f)

    user = 'me'
    api = GmailApi(auth_info)
    # 初回実行時は認証が求められます。
    query = QUERY

    maillist = api.getMailList(user, query)
    if maillist['resultSizeEstimate'] > 0:
        mail_id = maillist["messages"][0]['id']
        content = api.getMailContent(user, mail_id)
        mail = parse_mail(content)
        api.doMailAsRead(user, mail_id)
        return mail
    else:
        return False


def parse_mail(content):
    mail = {}

    raw_body = content['payload']['parts'][0]['body']['data']
    mail['body'] = base64.urlsafe_b64decode(raw_body).decode('utf-8')
    mail['snippet'] = content['snippet']

    headers = content['payload']['headers']
    for header in headers:
        if header['name'] == 'From':
            mail['from'] = header['value']
        elif header['name'] == 'To':
            mail['to'] = header['value']
        elif header['name'] == 'Subject':
            mail['subject'] = header['value']
        elif header['name'] == 'Date':
            mail['date'] = header['value']

    return mail


def send_slack(title, text):
    sc = SlackClient(SLACK_TOKEN)
    attachments = [{
        'title': title,
        'fallback': text,
        'icon_emoji': EMOJI,
        'text': text
    }]
    sc.api_call(
        "chat.postMessage",
        channel=CHANNEL,
        username=USERNAME,
        attachments=attachments,
        icon_emoji=EMOJI
    )

if __name__ == "__main__":
    mail = get_mail()
    if mail:
        print("メール受信")
        print(mail['date'])
        print(mail['subject'])
        text = mail['date'] + '\n' + mail['body']
        send_slack(mail['subject'], text)
    else:
        print("未読メールなし")
