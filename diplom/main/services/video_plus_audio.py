from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import ImageSequenceClip


def merge_video_audio(video_path, audio_path, output_path):
    with open(video_path, "r") as file:
        lines = file.readlines()

    frames = []
    durations = []

    audio = AudioFileClip(audio_path)

    for line in lines:
        line = line.strip().split()
        start_time = float(line[0])
        end_time = float(line[1])
        letter = line[2]

        image_path = f"lipsink_images/{letter}.jpg"
        frames.append(image_path)
        durations.append(end_time - start_time)

    video = ImageSequenceClip(frames, durations=durations)
    video = video.resize((1440, 900))
    video = video.set_audio(audio)
    video.write_videofile(output_path, fps=50)
