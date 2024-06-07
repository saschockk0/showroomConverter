from pathlib import Path
import subprocess
import os
import glob

# todo config
FFMPEG = Path('/usr/bin/ffmpeg')
# NET_FOLDER = Path('/mnt/winshare/nas/Магия/Покрутить видосики на экране')
NET_FOLDER = Path('/home/vids')


class VideoList:
    def __init__(self, file_name: str):
        self.file_name = file_name

    def get_videos(self) -> list[Path]:
        ...

    def add_video(self, path: Path):
        ...

    def delete_video(self, path: Path):
        ...


def convert_to_mov(source_path: Path):
    mp4_videos = source_path.glob("*.mp4")
    for video in mp4_videos:
        print(f"Converting {video}")
        command = [FFMPEG, '-i', video, '-f', 'mov', f'{video.parent}/{video.stem}.mov']
        subprocess.run(command)


if __name__ == '__main__':
    convert_to_mov(NET_FOLDER)
    '''
    delete_mp4(mp4s_path)
    videos: list(Path) = VideoList.get_videos()
    
    '''