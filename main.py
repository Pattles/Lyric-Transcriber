from yt_dlp import YoutubeDL
import os
from moviepy.editor import *
import asyncio
import imageio_ffmpeg as ffmpeg
import subprocess
from typing import Literal
import whisper
# import openai-whisper as whisper

### find . -name "whisper*"

PATH = '/Users/pattles/Lyric_Transcriber'
TEST_LINKS = {
    1:'https://www.youtube.com/watch?v=9Rc53l0iIOM', # Starfall
    2:'https://www.youtube.com/watch?v=dknT7xn59DY' # Капкан - МОТ
}

def download_mp4(link:str, status=Literal['title', 'current_song']):
    """
    * Downloads youtube video target as .mp4
    * Stores target in /videos directory
    * Returns title
    """
    ### Downloading youtube video target as .mp4
    ### Storing target in /videos directory

    # If target is named per title
    if status == 'title':
        options = {
            'format': 'mp4,webm,mkv,best',
            'outtmpl': os.path.join(f'{PATH}/videos/', '%(title)s.%(ext)s')
            }

    # If target is named 'current_song'
    elif status == 'current_song':
        options = {
            'format': 'mp4,webm,mkv,best',
            'outtmpl': f'{PATH}/videos/current_song.%(ext)s'
            }
        
    else:
        return ValueError('Invalid status for func download_mp4()')
    
    with YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(link) 
        title = info_dict.get('title', None)
        print('title: ', title)
   

    return title

def convert_mp3(status:Literal['title', 'current_song'], title=None):
    """
    * Converts target from .mp4/.webm to .mp3
    * Stores target in /mp3 directory
    """
    ### Finding target from /videos directory (if video is named 'current_song')

    # If target is named per title
    if status == 'title':
        try:
            # If target is .mp4
            video = VideoFileClip(os.path.join(f'{PATH}/videos/{title}.mp4'))
        except OSError:
            # If target is .webm
            video = VideoFileClip(os.path.join(f'{PATH}/videos/{title}.webm'))

        ### Saving target as .mp3 in /mp3 directory
        video.audio.write_audiofile(os.path.join(f'{PATH}/mp3/{title}.mp3'), codec='libmp3lame')
        return

    # If target is named 'current_song'
    elif status == 'current_song':
        try:
            # If target is .mp4
            video = VideoFileClip(os.path.join(f'{PATH}/videos/current_song.mp4'))
        except OSError:
            # If target is .webm
            video = VideoFileClip(os.path.join(f'{PATH}/videos/current_song.webm'))

        ### Saving target as .mp3 in /mp3 directory
        video.audio.write_audiofile(os.path.join(f'{PATH}/mp3/current_song.mp3'), codec='libmp3lame')
        return
    
    else:
        return ValueError('Invalid status for func convert_mp3()')

def transcribe(status:Literal['title', 'current_song'], title=None):
    ### Loading whisper model
    model = whisper.load_model('turbo')

    ### Transcribing lyrics
    # If target is named per title
    if status == 'title':
        result = model.transcribe(f'{PATH}/mp3/{title}.mp3')

    # If target is named 'current_song'
    elif status == 'current_song':
        result = model.transcribe(f'{PATH}/mp3/current_song.mp3')

    else:
        return ValueError('Invalid status for func transcribe()')

    # Outputting lyrics
    return print(result["text"])


def testing():
    status = 'title'
    link = 'https://www.youtube.com/watch?v=Jc1_j0NQjSc&pp=ygUaaGVubnl0aGluZyBpcyBwb3NzaWJsZSA0MDQ%3D'


    
    ### Downloading youtube video target as .mp4
    ### Storing target in /videos
    title = download_mp4(link=link, status=status)

    ### Converting target from .mp4 to .mp3
    ### Storing target in /mp3
    convert_mp3(status=status, title=title) 

    ### Transcribing lyrics
    # transcribe(status=status, title='sora - serotonin (slowed and reverb)')



def main():
    status = 'current_song'
    link = input('Enter a Youtube link: ')
    
    ### Downloading youtube video target as .mp4
    ### Storing target in /videos
    title = download_mp4(link)

    ### Converting target from .mp4 to .mp3
    ### Storing target in /mp3
    convert_mp3(status=status)

    ### Transcribing lyrics
    transcribe(status=status)

### whisper --model turbo --language Russian 'videos/current_song.mp3' 
### whisper --model turbo --language English /Users/pattles/Lyric_Transcriber/mp3/current_song.mp3
# /Users/pattles/Lyric_Transcriber/mp3/Zei - Hennything (Ft. 404Studios) Lyrics.mp3

# command = ['whisper', '--model turbo', '\'videos/current_song.mp3\'' ]
# result = subprocess.run(command, capture_output=True, text=True)

if __name__ == '__main__':
    testing() 

    # print(whisper.__file__)
    # print(dir(whisper))

