import subprocess
import json
import sys
import os

working_folder = sys.argv[1]
jsonFile = f"{working_folder}/story.json"

# Create necessary folders
newFolder = f"{working_folder}/audio"
currDirectory = os.path.dirname(os.path.abspath(__file__))
folderPath = os.path.join(currDirectory, newFolder)
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

with open(jsonFile, 'r') as file:
    nostalgic_story = json.load(file)

# print(nostalgic_story)


# Create a say command for each phrase and export to a file
speechVoice = "Princess"
speechSpeed = "120"

for i in range(len(nostalgic_story)):
    phrase = nostalgic_story[i]["phrase"]
    tag = nostalgic_story[i]["tag"]
    args = ["say", "-v", speechVoice, "-r", speechSpeed, phrase, "-o", f"{newFolder}/{i}.aiff"]
    # print(args)
    subprocess.run(args)

for i in range(len(nostalgic_story)):
    # Convert to mp3
    # ffmpeg -i audio/0.aiff -acodec libmp3lame audio/0.mp3
    args = [
        "ffmpeg",
        "-i",
        f"{newFolder}/{i}.aiff",
        "-acodec",
        "libmp3lame",
        f"{newFolder}/{i}.mp3",
    ]
    subprocess.run(args)
    args = ["rm", f"{newFolder}/{i}.aiff"]
    subprocess.run(args)