import os
import shutil
import subprocess
import wave
from collections.abc import Iterator
from pathlib import Path

from IPython.display import Audio, display


def play(audio: bytes, notebook: bool = False) -> None:
    if notebook:
        display(Audio(audio, rate=44100, autoplay=True))
    else:
        if not is_installed("ffplay"):
            raise ValueError("ffplay from ffmpeg not found, necessary to play audio.")
        args = ["ffplay", "-autoexit", "-", "-nodisp"]
        proc = subprocess.Popen(
            args=args,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate(input=audio)
        proc.poll()


def save(audio: bytes, filename: str) -> None:
    with wave.open(filename, "w") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(44100)
        f.writeframes(audio)


def is_installed(lib_name: str) -> bool:
    lib = shutil.which(lib_name)
    if lib is None:
        return False
    global_path = Path(lib)
    # else check if path is valid and has the correct access rights
    return global_path.exists() and os.access(global_path, os.X_OK)


def stream(audio_stream: Iterator[bytes]) -> None:
    if not is_installed("mpv"):
        raise ValueError("mpv not found, necessary to stream audio.")

    mpv_command = ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"]
    mpv_process = subprocess.Popen(
        mpv_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    for chunk in audio_stream:
        if chunk is not None:
            mpv_process.stdin.write(chunk)  # type: ignore
            mpv_process.stdin.flush()  # type: ignore

    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()
