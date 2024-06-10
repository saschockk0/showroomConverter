import os.path
import subprocess
# todo config
FFMPEG = Path('/usr/bin/ffmpeg')
# NET_FOLDER = Path('/mnt/winshare/nas/Магия/Покрутить видосики на экране')
NET_FOLDER = Path('/home/vids')
vids_file = 'file_list.txt'
output_file = Path('final.MOV')


class VideoList:
    def __init__(self, file_name: str):
        self.file_name: Path = Path(file_name)

    def get_video_paths(self) -> list[Path]:
        if not self.file_name.is_file():
            self.file_name.touch()
        with open(self.file_name, 'r') as f:
            files = f.readlines()

        return [Path(i[6:-2]) for i in files]

    def add_video_path(self, path: Path):
        print(f'added video {path}')
        with open(self.file_name, 'a') as f:
            f.write(f"file '{self.file_name}'\n")

    def add_video_paths(self, paths: list[Path]):  # todo rework function to add paths
        with open(self.file_name, 'a') as f:
            for path in paths:
                f.write(f"file '{path}'\n")

    def delete_video_path(self, path: Path):
        match_files = self.get_video_paths()
        match_files.remove(path)
        with open(self.file_name, 'w') as f:
            for file in match_files:
                f.write(f"file '{file}'\n")


def convert_to_mov(source_path: Path):
    mp4_videos = source_path.glob("*.mp4")
    for video in mp4_videos:
        print(f"Converting {video}")
        command = [FFMPEG, '-i', video, '-f', 'mov', f'{video.parent}/{video.stem}.mov']
        subprocess.run(command)


def concat_movs(videos_file, output_file: Path):
    command = [FFMPEG, '-y', '-f', 'concat', '-safe', '0', '-i', videos_file, '-c', 'copy', output_file]
    print(f"Concatenating {output_file}")
    subprocess.run(command)
   
 

if __name__ == '__main__':
    '''
    convert_to_mov(NET_FOLDER)
    delete_mp4(mp4s_path)
    videos: list(Path) = VideoList.get_video_paths()
    files = 
    '''
    changed = False
    video_list = VideoList(vids_file)
    source_video_list = list(NET_FOLDER.glob('*.MOV'))

    # comparing
    for video in source_video_list:
        if video in video_list.get_video_paths():
            continue

        video_list.add_video_paths(source_video_list)
        changed = True

    for video in video_list.get_video_paths():
        if video in source_video_list:
            continue

        video_list.delete_video_path(video)
        changed = True

    if changed:
        concat_movs('file_list.txt', output_file)
    """
    Если changed то пересборка перезапуск видоса
    Проверка процесса vlc, если не работает, запускаем
    """
