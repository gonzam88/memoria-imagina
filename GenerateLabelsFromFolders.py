import json
import csv
import random
import subprocess
import sys
import os

currDirectory = os.path.dirname(os.path.abspath(__file__))

# Loop all the folders in the videos folder
# Delete empty folders. Add folders with videos to the array

folders = []
for root, dirs, files in os.walk(os.path.join(currDirectory, "videos")):
    if len(files) > 0:
        # Add only the folder name to the array
        folders.append(root.split("/")[-1])
    else:
        print(f"Deleting empty folder: {root}")
        os.rmdir(root)

# Write the folders to a file
with open('labels.txt', 'w') as file:
    data = ','.join(map(str, folders))
    file.write(data)

print(f"Total folders: {len(folders)}")