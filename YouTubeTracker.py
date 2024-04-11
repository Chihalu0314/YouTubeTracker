import googleapiclient.discovery
import webbrowser
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from datetime import datetime
import pytz

# APIキーを設定（適切な値に置き換えてください）
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyDc-abfCYoP7CMrbVSDouqVnl_RA1mxRJU")

def get_channel_name(channel_id):
    request = youtube.channels().list(
        part="snippet",
        id=channel_id
    )
    response = request.execute()
    return response['items'][0]['snippet']['title']

def get_channel_videos(channel_id):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        eventType="upcoming",
        type="video",
        maxResults=50
    )
    response = request.execute()
    return response['items']

def time_since(dt):
    """
    現在時刻との差を計算し、適切な文字列を返します。
    """
    now = datetime.now(pytz.timezone("Asia/Tokyo"))
    diff = now - dt
    if diff.days > 0:
        return f"{diff.days}日前に開始"
    elif diff.seconds // 3600 > 0:
        return f"{diff.seconds // 3600}時間前に開始"
    else:
        return f"{diff.seconds // 60}分前に開始"

def display_videos(videos, channel_name):
    window = tk.Tk()
    window.title(f"{channel_name}のYouTubeチャンネル動画")
    window.geometry("950x600")
    window.resizable(False, False)

    canvas = tk.Canvas(window, width=950, height=600)
    scroll_y = tk.Scrollbar(window, orient="vertical", command=canvas.yview)

    frame = tk.Frame(canvas)
    max_img_width, max_img_height = 220, 150

    if not videos:
        label = tk.Label(frame, text=f"現在、{channel_name}にはプレミア公開予定、プレミア公開中、ライブ配信予定、ライブ配信中の動画はありません。", font=("Helvetica", 16))
        label.grid(row=0, column=0, sticky="w")
    else:
        for index, video in enumerate(videos):
            row = index // 4  # 横に4つ表示
            column = index % 4
            
            title = video['snippet']['title']
            thumbnail_url = video['snippet']['thumbnails']['high']['url']
            video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
            published_at = video['snippet']['publishedAt']
            published_at_datetime = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Tokyo"))

            if "ライブ" in title or "配信中" in title:  # キーワードによる判断
                published_at_str = time_since(published_at_datetime)
            else:
                published_at_str = published_at_datetime.strftime("%m月%d日%H時に公開予定")

            response = requests.get(thumbnail_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((max_img_width, max_img_height), Image.Resampling.LANCZOS)  # 修正箇所
            photo = ImageTk.PhotoImage(img)


            thumbnail_label = tk.Label(frame, image=photo, cursor="hand2")
            thumbnail_label.image = photo  # 参照を保持
            thumbnail_label.grid(row=row*3, column=column, padx=5, pady=5)
            thumbnail_label.bind("<Button-1>", lambda e, url=video_url: webbrowser.open_new(url))

            title_label = tk.Label(frame, text=title, fg="blue", cursor="hand2", wraplength=max_img_width, font=("Helvetica", 12))
            title_label.grid(row=row*3+1, column=column, sticky="nw")
            title_label.bind("<Button-1>", lambda e, url=video_url: webbrowser.open_new(url))

            # 公開日時または配信開始からの経過時間を表示
            published_at_label = tk.Label(frame, text=published_at_str, fg="black", wraplength=max_img_width, font=("Helvetica", 10))
            published_at_label.grid(row=row*3+2, column=column, sticky="nw")

    canvas.create_window(0, 0, anchor='nw', window=frame)
    canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)
                
    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')

    window.mainloop()

def main():
    channel_id = "UCNsidkYpIAQ4QaufptQBPHQ"
    channel_name = get_channel_name(channel_id)
    videos = get_channel_videos(channel_id)
    display_videos(videos, channel_name)

if __name__ == "__main__":
    main()
