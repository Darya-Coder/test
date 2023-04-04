import os
import vlc
import time
import obswebsocket
from obswebsocket import requests
import json

# Connect to OBS
ws = obswebsocket.obsws("172.16.3.56", 4455)
ws.connect()

# Get the text source in OBS
text_source_name = "text"
source = next(filter(lambda s: s['name'] == text_source_name, ws.call(obswebsocket.requests.GetSourcesList()).getSources()), None)
if source is None:
    raise ValueError(f"Source '{text_source_name}' not found in OBS")

# Get the list of video files in the directory
video_dir = "D:/Madhubala With English Subtitles"
videos = [f for f in os.listdir(video_dir) if os.path.isfile(os.path.join(video_dir, f)) and f.endswith(".mp4")]

# Initialize VLC player
instance = vlc.Instance("--no-xlib")

for video in videos:
    # Update the text source with the current video name
    ws.call(obswebsocket.requests.SetTextGDIPlusProperties(source["name"], video))

    # Play the video in VLC
    player = instance.media_player_new()
    media = instance.media_new(os.path.join(video_dir, video))
    player.set_media(media)
    player.play()

    # Wait for the video to finish and get the duration
    duration = player.get_length() / 1000
    time.sleep(duration)

    # Update the text source with the video duration
    ws.call(obswebsocket.requests.SetTextGDIPlusProperties(source["name"], f"{video} ({duration//60:02d}:{duration%60:02d})"))

    # Stop the player
    player.stop()

# Disconnect from OBS
ws.disconnect()
