from collections import Iterable
from pathlib import Path
from typing import Optional, Union

from discord.ext.commands import Context
from mutagen import MutagenError
from mutagen.easymp4 import EasyMP4
from mutagen.flac import FLAC
from mutagen.mp3 import EasyMP3

from music.playing_status import PlayingStatus


def check_conditions(ctx: Context, music_player) -> tuple:
    """
    Check conditions for playing music.
    :param ctx: discord `Context` object.
    :param music_player: the music player instance.
    :type music_player: MusicPlayer
    :return: a tuple of
        (the playing condition has been matched, the message to send if any)
    """
    ch = ctx.author.voice.channel
    status = music_player.playing_status
    try:
        ctx_ch = ctx.voice_client.channel
    except AttributeError:
        ctx_ch = None
    if status == PlayingStatus.NO and not ch:
        return False, 'You must be in a voice channel to use this command.'
    if (status != PlayingStatus.NO and
            not (ch == ctx_ch or ctx_ch is None)):
        return False, (
            'You must be in the same voice'
            'channel as me to use this command.'
        )
    return True, None


def __to_string(tag: Union[str, list, None]) -> Optional[str]:
    """
    Function to turn a tag into a string.
    :param tag: the tag.
    :return: the tag as a string.
    """
    if isinstance(tag, str):
        res = tag.strip()
    elif isinstance(tag, Iterable):
        res = ', '.join(tag).strip()
    else:
        res = None
    if isinstance(res, str):
        return res or None
    return None


def get_file_info(file_path: str) -> tuple:
    """
    Get mp3/mp4/flac tags from a file.
    :param file_path: the file path.
    :return: a tuple of  (title, genre, artist, album, length)
    """
    empty = lambda: (Path(file_path).name, None, None, None, None)
    tag = None
    try:
        if file_path.endswith('.flac'):
            tag = FLAC(file_path)
        elif file_path.endswith('.mp3'):
            tag = EasyMP3(file_path)
        elif file_path.endswith('m4a'):
            tag = EasyMP4(file_path)
        else:
            return empty()
        get = lambda t, s: t.get(s, None) or t.get(s.upper(), None)
        title = get(tag, 'title') or Path(file_path).name
        genre = get(tag, 'genre')
        artist = get(tag, 'artist')
        album = get(tag, 'album')
        length = tag.info.length
        if isinstance(length, (int, float)):
            minutes, seconds = divmod(length, 60)
            length_str = f'{int(minutes)}:{round(seconds):02d}'
        else:
            length_str = None
        return (__to_string(title), __to_string(genre),
                __to_string(artist), __to_string(album), length_str)
    except MutagenError:
        return empty()
    finally:
        del tag