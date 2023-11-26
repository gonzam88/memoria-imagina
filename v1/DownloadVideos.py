import json
import csv
import random
import subprocess
import sys
import os


working_folder = sys.argv[1]
jsonFile = f"{working_folder}/story.json"

# Create necessary folders
newFolder = f"{working_folder}/video"
currDirectory = os.path.dirname(os.path.abspath(__file__))
folderPath = os.path.join(currDirectory, newFolder)
if not os.path.exists(folderPath):
    os.makedirs(folderPath)


with open(jsonFile, 'r') as file:
    nostalgic_story = json.load(file)

with open('kinetics700.csv', 'r') as file:
    csv_reader = csv.reader(file)
    kinetics = [row for row in csv_reader]

# Loop story and find the corresponding video
for i in range(len(nostalgic_story)):
    file_path = f"{newFolder}/{i}.mp4"
    if os.path.exists(file_path):
        print("The file exists.")
        continue

    tag = nostalgic_story[i]["tag"]
    print(f" Tag: {tag}")

    # Use a list comprehension to filter the array based on the search value in the first column
    filtered_data = [row for row in kinetics if row[0] == tag]

    # Use a random result
    random_element = random.choice(filtered_data)
    videoId = random_element[1]
    print(random_element)
    print(videoId)
    start = random_element[2]
    end = random_element[3]

    # Download the video
    args = [
        "yt-dlp",
        videoId,
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


