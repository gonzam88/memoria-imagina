import json
import csv
import random
import subprocess
import sys
import os

currDirectory = os.path.dirname(os.path.abspath(__file__))


with open('kinetics700.csv', 'r') as file:
    csv_reader = csv.reader(file)
    kinetics = [row for row in csv_reader]
    print(kinetics[1])

# Loop kinetics from the second row
for i in range(1, len(kinetics)):
    tag = kinetics[i][0]
    
    folder = os.path.join(currDirectory, "videos", tag)
    if not os.path.exists(folder):
        print(f"Creating folder: {folder}")
        os.makedirs(folder)

    videoId = kinetics[i][1]
    filename = f"{videoId}.mp4"
    file_path = os.path.join(folder, filename)
    if os.path.exists(file_path):
        print("The file exists. Skipping")
        continue

    print(f" Downloading: {i}/{len(kinetics)} - {videoId}")
    start = kinetics[i][2]
    end = kinetics[i][3]
    url = f"https://www.youtube.com/watch?v={videoId}"
    # Download the video
    args = [
        "yt-dlp",
        url,
        "-f",
        "18",
        "--downloader",
        "ffmpeg",
        "--downloader-args",
        f"ffmpeg_i:-ss {start} -to {end}",
        "--output",
        file_path,
    ]
    print(args)
    subprocess.run(args)