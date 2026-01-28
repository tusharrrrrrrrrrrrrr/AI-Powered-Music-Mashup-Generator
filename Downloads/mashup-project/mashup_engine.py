import os
import subprocess
from pydub import AudioSegment
from clean_up import delete_all_files
AudioSegment.converter = r"C:\Users\dell\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"

DOWNLOAD_DIR = "downloads"
AUDIO_DIR = "audios"
TRIM_DIR = "trimmed"
OUTPUT_DIR = "output"

def create_dirs():
    for d in [DOWNLOAD_DIR, AUDIO_DIR, TRIM_DIR, OUTPUT_DIR]:
        os.makedirs(d, exist_ok=True)

def download_videos(singer, n):
    print("Downloading videos...")
    cmd = [
    "yt-dlp",
    f"ytsearch{n}:{singer} songs",
    "-f", "bestaudio",
    "--extract-audio",
    "--audio-format", "mp3",
    "--ignore-errors",
    "--no-abort-on-error",
    "--user-agent", "Mozilla/5.0",
    "--sleep-interval", "3",
    "-o", f"{DOWNLOAD_DIR}/%(id)s.%(ext)s"
]



    subprocess.run(cmd)


def trim_audios(seconds):
    print("Trimming audio clips...")
    os.makedirs(TRIM_DIR, exist_ok=True)

    count = 0
    for file in os.listdir(DOWNLOAD_DIR):
        if not file.lower().endswith(".mp3"):
            continue

        path = os.path.join(DOWNLOAD_DIR, file)

        try:
            audio = AudioSegment.from_file(path)
            if len(audio) < seconds * 1000:
                continue

            clip = audio[:seconds * 1000]
            clip.export(os.path.join(TRIM_DIR, file), format="mp3")
            count += 1

        except Exception as e:
            print("Skipping:", file)

    if count == 0:
        raise Exception("No valid audio clips to merge")


def merge_audios(output_name):

    print("Merging audios...")
    final = AudioSegment.empty()
    print("Files to merge:", os.listdir(TRIM_DIR))

    for file in os.listdir(TRIM_DIR):
        final += AudioSegment.from_mp3(os.path.join(TRIM_DIR, file))

    output_path = os.path.join(OUTPUT_DIR, output_name)
    final.export(output_path, format="mp3")
    delete_all_files(DOWNLOAD_DIR)
    delete_all_files(TRIM_DIR)
    return output_path

def create_mashup(singer, n, duration, output_file):
    create_dirs()
    download_videos(singer, n)
    trim_audios(duration)
    return merge_audios(output_file)

