from moviepy.editor import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

# Список видео файлов для соединения
video_files = []

# Загрузка видео и создание объектов VideoFileClip
clips = [VideoFileClip(video) for video in video_files]

# Соединение видео
final_clip = concatenate_videoclips(clips)

# Сохранение итогового видео
final_clip.write_videofile("merged_video.mp4")