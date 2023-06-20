import cv2
import os

images_folder = "lipsink_images"

input_file = "input.txt"

with open(input_file, "r") as file:
    lines = file.readlines()

frames = []
durations = []

for line in lines:
    line = line.strip().split()
    start_time = float(line[0])
    end_time = float(line[1])
    letter = line[2]


    image_path = os.path.join(images_folder, f"{letter}.jpg")


    image = cv2.imread(image_path)


    frames.append(image)
    print(int((end_time - start_time) * 1000))
    durations.append(int((end_time - start_time) * 1000))


fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video = cv2.VideoWriter("output.mp4", fourcc, 4000, (frames[0].shape[1], frames[0].shape[0]))

for frame, duration in zip(frames, durations):
    for _ in range(duration):
        video.write(frame)

video.release()
