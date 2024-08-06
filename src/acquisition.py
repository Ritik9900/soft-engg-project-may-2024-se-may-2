import pandas as pd
from pytube import Playlist, YouTube
from langchain_community.document_loaders import YoutubeLoader

def scrapePlaylistData(playlist_url):
    data = []

    Playlist = Playlist(playlist_url)
    playlist_title = Playlist.title
    playlist_videos = Playlist.video_urls

    for video in playlist_videos:
        yt_video = YouTube(video)
        data.append({'title': yt_video.title, 'url': video})

    return playlist_title, pd.DataFrame(data)

def extractVideoTranscript(video_url):
    loader = YoutubeLoader.from_youtube_url(
        youtube_url=video_url,
        add_video_info=False
    )
    return loader.load()