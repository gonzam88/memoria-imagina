import json
import csv
import random
import subprocess
import sys
import os
import moviepy.editor as mp
import moviepy.audio.fx.all as afx
from openai import OpenAI


currDirectory = os.path.dirname(os.path.abspath(__file__))
speechVoices = ["Allison", "Victoria", "Samantha"]

# Load labels file
labels = []
with open('labels.txt', 'r') as file:
    labels = file.read().split(',')


def CreateAudioFile(label):
    # Create audio file
    fileRouteAiff = os.path.join(currDirectory, "audios", label + ".aiff")
    fileRouteMp3 = os.path.join(currDirectory, "audios", label + ".mp3")
    # Open script file
    scriptFile = os.path.join(currDirectory, "scripts", label + ".txt")
    text = ""
    with open(scriptFile, 'r') as file:
        text = file.read()
    # Create audio file (aiff)
    args = [
        "say",
        "-v",
        random.choice(speechVoices),
        text,
        "-o",
        fileRouteAiff,
    ]
    subprocess.run(args)
    # Convert to mp3
    args = [
        "ffmpeg",
        "-i",
        fileRouteAiff,
        "-acodec",
        "libmp3lame",
        fileRouteMp3,
    ]
    subprocess.run(args)
    # Remove aiff
    args = ["rm", fileRouteAiff]
    subprocess.run(args)

def CreateCompiledVideo(label):
    # Create compiled video file
    # Get all the videos from the label folder
    # Path to the folder containing videos
    videos_folder = os.path.join(currDirectory, "videos", label)

    # Get a list of video files in the folder
    video_files = [file for file in os.listdir(videos_folder) if file.endswith(".mp4")]
    if(len(video_files) == 0):
        print("No video files found")
        return

    # Create VideoFileClip objects for each video file
    video_clips = [mp.VideoFileClip(os.path.join(videos_folder, video)) for video in video_files]

    # Concatenate all video clips into a single video
    composition = mp.concatenate_videoclips(video_clips, method='compose')
    composition = composition
    composition.write_videofile(f"{currDirectory}/compiled_videos/{label}.mp4", codec='libx264', 
        audio_codec='aac', 
        temp_audiofile='temp-audio.m4a', 
        remove_temp=True)
    # Get the duration of the final concatenated video in seconds
    video_duration = composition.duration

    # Create a dictionary with video duration
    video_info = {'duration_seconds': video_duration}

    # Specify the output JSON file path
    json_output_path = f"{currDirectory}/compiled_videos/{label}.json"

    # Write video duration information to a JSON file
    with open(json_output_path, 'w') as json_file:
        json.dump(video_info, json_file, indent=4)

def CreateScript(label):
    jsonFile = f"{currDirectory}/compiled_videos/{label}.json"
    with open(jsonFile, 'r') as file:
        videoData = json.load(file)
    videoDuration = round(videoData["duration_seconds"]) - 3 # margen de 3 segundos

    client = OpenAI(api_key=OPENAI_API_KEY)
    print(f"{label} script should be {videoDuration} seconds long")

    chatgpt = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a poetic assistant, experienced documentary filmmaker with some traits of Herzog and Wong Kar Wai."},
        {"role": "user", "content": f"Write in first person about your childhood memory. be specific, extensive and honest with your feeling. The topic is {label}. Make the text so that it takes aprox {videoDuration} seconds when read aloud."}
    ])
    script = chatgpt.choices[0].message.content
    scriptFile = os.path.join(currDirectory, "scripts", label + ".txt")
    # Write the folders to a file
    with open(scriptFile, 'w') as file:
        file.write(script)

def ComposeVideo(videoFile, audioFile, label):
    print(f"**** Composing {label} ****")
    # Compose Audio And Video
    videoclip = mp.VideoFileClip(videoFile).fx(afx.audio_normalize).fx(afx.volumex, 0.024)
    audioclip = mp.AudioFileClip(audioFile)
    
    # Define the delay duration (in seconds)
    delay_duration = random.uniform(2, 4)
    # Mix original audio with new audio
    new_audioclip = mp.CompositeAudioClip([videoclip.audio, audioclip.set_start(delay_duration)])
    # Set new audio
    videoclip = videoclip.set_audio(new_audioclip)

    videoclip.write_videofile(f"{currDirectory}/export/{label}.mp4", codec='libx264', 
        audio_codec='aac', 
        temp_audiofile='temp-audio.m4a', 
        remove_temp=True)


def CreateVideo():
    # Loop labels
    for i in range(1, len(labels)):
        print(labels[i])
        
        # Check if compiled video file exists
        compiledVideoFile = os.path.join(currDirectory, "compiled_videos", labels[i] + ".mp4")
        if(not os.path.exists(compiledVideoFile)):
            print(labels[i] + ": compiled file does not exist. Creating")
            CreateCompiledVideo(labels[i])

        # Check if script file exists
        scriptFile = os.path.join(currDirectory, "scripts", labels[i] + ".txt")
        if(not os.path.exists(scriptFile)):
            print(labels[i] + ": script file does not exist. Creating")
            CreateScript(labels[i])
        
        # Check if audio file exists
        audioFile = os.path.join(currDirectory, "audios", labels[i] + ".mp3")
        if(not os.path.exists(audioFile)):
            print(labels[i] + ": audio file does not exist. Creating")
            CreateAudioFile(labels[i])
        
        ComposeVideo(compiledVideoFile, audioFile, labels[i])


CreateVideo()
