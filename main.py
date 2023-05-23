# Import the necessary libraries
import os  # For file and directory operations
import subprocess  # To call ffmpeg command
import pandas as pd  # For data handling
from tabulate import tabulate  # For pretty printing tables


# This function gets the duration of a video file
def get_video_length(video_path):
    # We are calling the ffprobe command which is a part of ffmpeg, a tool to handle multimedia data
    # -v error: We only want error messages
    # -show_entries format=duration: We are interested in the duration of the video
    # -of default=noprint_wrappers=1:nokey=1: Do not print the key of each field
    cmd = '"C:/Program Files/ffmpeg/bin/ffprobe" -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "' + video_path + '"'

    # Call the command and get the output
    output = subprocess.check_output(cmd, shell=True)

    # The output is the duration in seconds, so we convert it to a float and return it
    return float(output)


# Define the folder path where your video files are
folder_path = 'C:/my-videos'

# These are the lists that will hold the folder names and their respective total video durations
folder_list = []
duration_list = []

# os.walk returns a generator that creates a tuple of values for each directory in the path
# These values are the name of the current folder, the names of its subfolders, and the names of all the files in the current folder
for folder_name, subfolders, filenames in os.walk(folder_path):
    # For each folder, we start with a total duration of 0 seconds
    total_seconds = 0
    # We go through each file in the current folder
    for filename in filenames:
        # We are interested in video files, so we check the extension of the file
        if filename.endswith(('.mp4', '.mkv', '.avi', '.mov')):  # add or remove video formats as needed
            # We get the complete path of the file
            file_path = os.path.join(folder_name, filename)
            try:
                # We get the duration of the video and add it to the total duration
                total_seconds += get_video_length(file_path)
            except Exception as e:
                # If there was an error getting the duration of the video, we print it
                print(f"Couldn't get duration of {file_path}, reason: {e}")

    # We convert the total duration from seconds to hours
    total_hours = total_seconds / 3600

    # If the total duration is greater than 0, we add the folder name and the duration to our lists
    if total_hours > 0:
        folder_list.append(folder_name)
        duration_list.append(total_hours)

# After we have checked all folders and videos, we calculate the total duration of all videos in all folders
total_hours_all_videos = sum(duration_list)

# We create a DataFrame from our lists
df = pd.DataFrame(list(zip(folder_list, duration_list)), columns=['Folder', 'Total Duration (hours)'])

# We print the DataFrame in a pretty table
print(tabulate(df, headers='keys', tablefmt='psql'))

# We print the total duration of all videos
print(f"\nTotal Duration of All Videos: {total_hours_all_videos} hours")
