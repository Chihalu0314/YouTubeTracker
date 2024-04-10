import datetime
import time
import webbrowser
from googleapiclient.discovery import build
from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

# YouTube Data APIキーを設定します
api_key = "AIzaSyDc-abfCYoP7CMrbVSDouqVnl_RA1mxRJU"

# YouTube Data APIクライアントを作成します
youtube = build('youtube', 'v3', developerKey=api_key)

# 特定のチャンネルIDを設定します
channel_id = "UC1DCedRgGHBdm81E1llLhOQ"

# 更新する時間を設定します
update_times = [6, 12, 16, 19, 20, 20.5]

def get_videos():
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        eventType="live",
        type="video"
    )
    response = request.execute()

    if not response["items"]:
        print(f"現在、{channel_id}にはプレミア公開予定、プレミア公開中、ライブ配信予定、ライブ配信中の動画はありません")
    else:
        for item in response["items"]:
            print(f"タイトル: {item['snippet']['title']}")
            print(f"サムネイル: {item['snippet']['thumbnails']['default']['url']}")
            print(f"動画リンク: https://www.youtube.com/watch?v={item['id']['videoId']}\n")

def update_videos():
    while True:
        now = datetime.datetime.now()
        if now.hour + now.minute / 60 in update_times:
            get_videos()
            time.sleep(60)  # 同じ時間に複数回更新しないように1分間スリープします
        time.sleep(10)  # 10秒ごとに時間をチェックします

update_videos()
