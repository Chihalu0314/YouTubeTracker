import googleapiclient.discovery
import webbrowser
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

def get_channel_videos(channel_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyDc-abfCYoP7CMrbVSDouqVnl_RA1mxRJU")

    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        eventType="live",
        type="video"
    )
    response = request.execute()

    return response['items']

def display_videos(videos):
    window = tk.Tk()
    window.title("YouTube Channel Videos")
    for video in videos:
        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True)

        title = video['snippet']['title']
        thumbnail_url = video['snippet']['thumbnails']['high']['url']
        video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"

        response = requests.get(thumbnail_url)
        img_data = response.content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

        thumbnail_label = tk.Label(frame, image=img, cursor="hand2")
        thumbnail_label.image = img
        thumbnail_label.pack()
        thumbnail_label.bind("<Button-1>", lambda e, url=video_url: webbrowser.open_new(url))

        title_label = tk.Label(frame, text=title, fg="blue", cursor="hand2", wraplength=img.width())
        title_label.pack()
        title_label.bind("<Button-1>", lambda e, url=video_url: webbrowser.open_new(url))

    window.mainloop()

def main():
    channel_id = "UC1DCedRgGHBdm81E1llLhOQ"
    videos = get_channel_videos(channel_id)

    if videos:
        display_videos(videos)
    else:
        print(f"現在、{channel_id}にはプレミア公開予定、プレミア公開中、ライブ配信予定、ライブ配信中の動画はありません。")

if __name__ == "__main__":
    main()
