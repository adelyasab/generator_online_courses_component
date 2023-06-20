import wave
from pydub import AudioSegment


def process_audio_file(input_file, output_file):
    audio_file = wave.open(input_file, "r")

    sample_rate = audio_file.getframerate()
    num_frames = audio_file.getnframes()
    duration = num_frames / float(sample_rate)

    audio_file.close()

    data_file = open("videoPlusAudio/output6.txt", "r")
    data_lines = data_file.readlines()
    data_file.close()

    output_file = open(output_file, "w")

    for i, line in enumerate(data_lines):
        line = line.strip().split()
        time_stamp = float(line[0])
        label = line[1]

        start_time = time_stamp
        end_time = duration if i >= len(data_lines) - 1 else float(data_lines[i + 1].strip().split()[0])

        output_file.write(f"{start_time:.2f} {end_time:.2f} {label}\n")

    output_file.close()

    # WAV to MP3 conversion
    audio = AudioSegment.from_wav(input_file)
    audio.export(output_file.replace('.txt', '.mp3'), format='mp3')
