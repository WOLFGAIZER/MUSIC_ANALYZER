# services/ffmpeg_mixer.py

import os
import subprocess

def mix_selected_stems(input_dir: str, selected_stems: list, output_path: str) -> bool:
    """
    Mix selected stem WAV files using FFmpeg.

    Args:
        input_dir (str): Folder containing separated stems (e.g. vocals.wav, drums.wav, etc.)
        selected_stems (list): List of stems to include
        output_path (str): Path to save final mixed audio

    Returns:
        bool: True if successful, False otherwise
    """
    input_files = []
    filter_inputs = []

    for idx, stem in enumerate(selected_stems):
        file_path = os.path.join(input_dir, f"{stem}.wav")
        if not os.path.exists(file_path):
            continue
        input_files.extend(["-i", file_path])
        filter_inputs.append(f"[{idx}:a]")

    if not input_files:
        return False

    # FFmpeg filter: mix all selected stems
    filter_complex = f"{''.join(filter_inputs)}amix=inputs={len(filter_inputs)}:normalize=0[out]"

    cmd = ["ffmpeg", "-y"] + input_files + [
        "-filter_complex", filter_complex,
        "-map", "[out]",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
