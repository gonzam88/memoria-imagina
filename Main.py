import json
import csv
import random
import subprocess
import sys
import os
import moviepy.editor as mp
import moviepy.audio.fx.all as afx


currDirectory = os.path.dirname(os.path.abspath(__file__))
speechVoices = ["Princess", "Allison", "Victoria", "Samantha"]

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
    # print(files)
    # # Create a list of videos
    # videos = []
    # for i in range(len(files)):
    #     videoFile = os.path.join(folder, files[i])
    #     videos.append(videoFile)
    # # Create a list of clips
    # clips = []
    # for i in range(len(files)):
    #     # Get video clip
    #     videoClip = mp.VideoFileClip(videos[i]).fx(afx.audio_normalize).fx(afx.volumex, 0.05)
    #     # Get audio clip
    #     audioClip = mp.AudioFileClip(audios[i])
    #     # Mix original audio with new audio
    #     new_audioclip = mp.CompositeAudioClip([videoClip.audio, audioClip])
    #     # Set new audio
    #     videoClip = videoClip.set_audio(new_audioclip)
    #     # Set duration to shortest
    #     audioDuration = audioClip.duration
    #     videoDuration = videoClip.duration
    #     shortestDuration = min(audioDuration, videoDuration)
    #     videoClip = videoClip.subclip(0, shortestDuration)
    #     # Add to array
    #     clips.append(videoClip)
    # Render
    # composition = mp.concatenate_videoclips(clips, method='compose')
    # composition.write_videofile(f"{currDirectory}/compiled_videos/{label}.mp4", codec='libx264', 
    #                     audio_codec='aac', 
    #                     temp_audiofile='temp-audio.m4a', 
    #                     remove_temp=True)

def CreateVideo():
    # Loop labels
    for i in range(1, len(labels)):
        print(labels[i])
        
        # Check if compiled video file exists
        compiledVideoFile = os.path.join(currDirectory, "compiled_videos", labels[i] + ".mp4")
        if(not os.path.exists(compiledVideoFile)):
            print(labels[i] + ": compiled file does not exist. Creating")
            CreateCompiledVideo(labels[i])
            continue

        # Check if script file exists
        scriptFile = os.path.join(currDirectory, "scripts", labels[i] + ".txt")
        if(not os.path.exists(scriptFile)):
            print(labels[i] + ": script file does not exist. Skipping")
            continue
        
        # Check if audio file exists
        audioFile = os.path.join(currDirectory, "audios", labels[i] + ".mp3")
        if(not os.path.exists(audioFile)):
            print(labels[i] + ": audio file does not exist. Creating")
            CreateAudioFile(labels[i])
            continue

CreateVideo()
