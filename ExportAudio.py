import subprocess
import json
import sys

a = sys.argv[1]
b = sys.argv[2]
print(a, b)



# with open('story.json', 'r') as file:
#     nostalgic_story = json.load(file)

# print(nostalgic_story)


# # Create a say command for each phrase and export to a file
# speechVoice = "Princess"
# speechSpeed = "120"

# for i in range(len(nostalgic_story)):
#     phrase = nostalgic_story[i]["phrase"]
#     tag = nostalgic_story[i]["tag"]
#     args = ["say", "-v", speechVoice, "-r", speechSpeed, phrase, "-o", f"audio/{i}.aiff"]
#     # print(args)
#     subprocess.run(args)

# for i in range(len(nostalgic_story)):
#     # Convert to mp3
#     # ffmpeg -i audio/0.aiff -acodec libmp3lame audio/0.mp3
#     args = [
#         "ffmpeg",
#         "-i",
#         f"audio/{i}.aiff",
#         "-acodec",
#         "libmp3lame",
#         f"audio/{i}.mp3",
#     ]
#     subprocess.run(args)