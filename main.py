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
network_folder = '/home/vids/'
logger = logging.getLogger(__name__)
final = './merged_video.mp4'


def get_video_files():
    #files = next(walk(network_folder), (None, None, []))[2]
    files = [f for f in listdir(Path(network_folder)) if isfile(join(Path(network_folder), f))]
    return sorted(files)


def create_file_list(file_list, output_file): #todo ignore .DS_STORE
    with open(output_file, 'w') as f:
        for file in file_list:
            if file and os.path.splitext(file) not in EXCEPTIONS:
                f.write(f'file {Path(network_folder)}/{file}\n')


def concatenate(videos_to_concatenate: list[Path], output_file: Path):
    try:
        main_video = ffmpeg.input(videos_to_concatenate.pop(0))
    except IndexError:
        logger.error("List is empty, cannot pop main video")
        raise

    for video in videos_to_concatenate:
        video_to_concat = ffmpeg.input(video)
        main_video = ffmpeg.concat(main_video, video_to_concat)

    main_video = ffmpeg.output(main_video, filename=output_file)
    logger.info("Concatenating main video")
    ffmpeg.run(main_video, overwrite_output=True)

def merge_videos(file_list):
    output_file = 'merged_video.mp4'
    create_file_list(file_list, 'file_list.txt')
    command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'file_list.txt', '-c', 'copy', output_file]
    subprocess.run(command)
    return output_file


def play_video(video_file):
    subprocess.run(['vlc', video_file])


if __name__ == '__main__':
    video_files = get_video_files()
    create_file_list()
    # if video_files:
    #     merged_video = concatenate(video_files, final)
    #     # merged_video = merge_videos(video_files)
    #     play_video(merged_video)
    # else:
    #     print("No video files found.")
