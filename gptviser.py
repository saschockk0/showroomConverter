import os.path
import subprocess
from pathlib import Path
import ffmpeg
from os import listdir
from os.path import isfile, join
import logging

video_extensions = ['.mp4', '.avi', '.MOV']
EXCEPTIONS = [".DS_Store", "Инструкция.txt"]
#network_folder = '/mnt/winshare/Магия/Покрутить видосики на экране'
network_folder: Path = Path('/home/vids/')
logger = logging.getLogger(__name__)
final = network_folder / 'merged_video.mp4'


def get_video_files():
    #files = next(walk(network_folder), (None, None, []))[2]
    files = [f for f in listdir(Path(network_folder)) if isfile(join(Path(network_folder), f))]
    files = sorted(files)
    return files


def create_file_list(file_list, output_file): #todo ignore .DS_STORE
    with open(output_file, 'w') as f:
        for file in file_list:
            if file and os.path.splitext(file) not in EXCEPTIONS:
                f.write(f'file {Path(network_folder)}/{file}\n')


def ffmpeg_convert(vids_file: Path, output_file: Path):
    return ffmpeg.input(vids_file, format='concat', safe=0).output(output_file, c='copy', overwrite=1).run()

def merge_videos(file_list):
    output_file = 'merged_video.mp4'
    create_file_list(file_list, 'file_list.txt')
    command = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'file_list.txt', '-c', 'copy', output_file]
    subprocess.run(command)
    return output_file



def play_video(video_file):
    subprocess.run(['vlc', video_file])


if __name__ == '__main__':
    video_files = get_video_files()
    if video_files:
        # merged_video = concatenate(network_folder.glob(), final)
        merged_video = ffmpeg_concat(Path('./file_list.txt'), 'merged_video.mp4')
        play_video(merged_video)
    else:
        print("No video files found.")
