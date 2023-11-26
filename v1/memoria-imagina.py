# import random

# def intro():
#     print ("test")

# def section():
#     print ("section")

# functions = [
#     intro,
#     section,
# ]

# def RandomFunction():
#     random.choice(functions)()

# RandomFunction()
import time
from transformers import pipeline
# Record the start time
start_time = time.time()

classifier = pipeline("zero-shot-classification", model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli")
sequence_to_classify = "The sun painted golden hues across the sky, and the laughter of my cousins echoed in my ears. We'd chase fireflies and tell ghost stories by the campfire, feeling like the world was ours to explore."
with open('labels.txt', 'r') as file:
    # Read the content of the file and split it into an array
    content = file.read()
    candidate_labels = content.split(',')
# print(candidate_labels[0])
# candidate_labels = ["politics", "economy", "entertainment", "environment"]
output = classifier(sequence_to_classify, candidate_labels, multi_label=False)
print(f"Sequence: {sequence_to_classify}")
print(f"{output['labels'][0]}, {output['scores'][0]}")
print(f"{output['labels'][1]}, {output['scores'][1]}")


# Record the end time
end_time = time.time()
# Calculate the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")