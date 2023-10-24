import moviepy.editor as mp
import moviepy.audio.fx.all as afx
import json
import sys
import os

working_folder = sys.argv[1]
jsonFile = f"{working_folder}/story.json"

# Create necessary folders
newFolder = f"{working_folder}/export"
currDirectory = os.path.dirname(os.path.abspath(__file__))
folderPath = os.path.join(currDirectory, newFolder)
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

# Load story
with open(jsonFile, 'r') as file:
    nostalgic_story = json.load(file)

clips = []
# concatenate videos using moviepy
for i in range(len(nostalgic_story)):
    videoclip = mp.VideoFileClip(f"{working_folder}/video/{i}.mp4").fx(afx.audio_normalize).fx(afx.volumex, 0.05)
    audioclip = mp.AudioFileClip(f"{working_folder}/audio/{i}.mp3")


    # Mix original audio with new audio
    new_audioclip = mp.CompositeAudioClip([videoclip.audio, audioclip])
    # Set new audio
    videoclip = videoclip.set_audio(new_audioclip)

    # Set duration to shortest
    audioDuration = audioclip.duration
    videoDuration = videoclip.duration
    shortestDuration = min(audioDuration, videoDuration)
    videoclip = videoclip.subclip(0, shortestDuration)
    
    # Add to array
    clips.append(videoclip)

# Render
composition = mp.concatenate_videoclips(clips, method='compose')
composition.write_videofile(f"{working_folder}/export/composition.mp4", codec='libx264', 
                     audio_codec='aac', 
                     temp_audiofile='temp-audio.m4a', 
                     remove_temp=True)