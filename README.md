# Abstract

gmailのメールを受信し、slackに通知を行う

# Environment

+ python 3.5.0
+ google-api-python-client 1.6.2
+ slackclient 1.0.5

# Setup

以下のコマンドでパッケージをインストール

`
pip install -r requirements.txt
`

[python向けのgoogle APIの解説](https://developers.google.com/gmail/api/quickstart/python)にアクセスしclient_secret.jsonを取得

client_secret.jsonは同ディレクトリに置く

[slack apiの解説](https://api.slack.com/web)にアクセスし、slackのtokenを取得

consts.pyを以下のコマンドで作成

`
cp consts.py.example consts.py
`

consts.py内の定数（slack tokenなど）を設定

# Usage

以下のコマンドで実行

`
python bot.py
`

初期設定のconsts.pyのQUERYは「is:unread」なので「未読メール」で最新の一件をslackに通知する。
QUERYを修正して任意のものに変更可能。
定期実行したい場合はcronなどを設定。

