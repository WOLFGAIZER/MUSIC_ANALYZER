# services/ffmpeg_mixer.py
import os
import subprocess
from uuid import uuid4

def generate_karaoke_mix(stems_dir: str, mute_stems: list) -> str:
    output_file = os.path.join("outputs", f"{uuid4().hex}_karaoke.wav")

    # Collect all stem paths
    stem_map = {
        "vocals": "vocals.wav",
        "drums": "drums.wav",
        "bass": "bass.wav",
        "other": "other.wav"
    }

    inputs = []
    filters = []
    index = 0

    for stem, file in stem_map.items():
        file_path = os.path.join(stems_dir, file)
        if not os.path.exists(file_path): continue

        inputs.extend(["-i", file_path])
        vol = "volume=0" if stem in mute_stems else "volume=1"
        filters.append(f"[{index}:a]{vol}[a{index}]")
        index += 1

    # Combine filters and output
    filter_complex = "; ".join(filters) + f"; {' '.join([f'[a{i}]' for i in range(index)])}amix=inputs={index}:duration=longest[out]"
    command = [
        "ffmpeg", *inputs,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-y", output_file
    ]

    try:
        subprocess.run(command, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg mixing failed: {e}")
