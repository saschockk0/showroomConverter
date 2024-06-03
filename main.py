import subprocess
from pathlib import Path
import ffmpeg
from os import listdir
from os.path import isfile, join

# Конфигурация сетевой папки
# network_folder = Path(r'"\\NAME-SERVER\D$\Folder 1\Folder 2\Folder 3\file.exe"')
video_extensions = ['.mp4', '.avi', '.MOV']
EXCEPTIONS = ["", ".DS_STORE", "Инструкция.txt"]
network_folder = r'\\10.2.0.4\nas\Магия\Покрутить видосики на экране'


def get_video_files():
    #files = next(walk(network_folder), (None, None, []))[2]
    files = [f for f in listdir(Path(network_folder)) if isfile(join(Path(network_folder), f))]
    return sorted(files)


def create_file_list(file_list, output_file): #todo ignore .DS_STORE
    with open(output_file, 'w') as f:
        for file in file_list:
            if file not in EXCEPTIONS:
                f.write(join(file))


def merge_videos(file_list):
    output_file = 'merged_video.mp4'
    create_file_list(file_list, 'file_list.txt')
    command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'file_list.txt', '-c', 'copy', output_file]
    subprocess.run(command)
    return output_file


def play_video(video_file):
    subprocess.run(['vlc.exe', video_file])


if __name__ == '__main__':
    video_files = get_video_files()
    if video_files:
        merged_video = merge_videos(video_files)
        play_video(merged_video)
    else:
        print("No video files found.")
