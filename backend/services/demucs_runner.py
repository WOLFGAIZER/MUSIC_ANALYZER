# services/demucs_runner.py
import os
import subprocess
from uuid import uuid4

OUTPUT_DIR = "outputs"

def run_demucs(input_path: str) -> str:
    output_subdir = os.path.join(OUTPUT_DIR, uuid4().hex)
    os.makedirs(output_subdir, exist_ok=True)

    # Run Demucs command
    command = [
        "python", "-m", "demucs",
        "--two-stems=vocals",  # can also use "all" or leave default
        "--out", output_subdir,
        input_path
    ]

    try:
        subprocess.run(command, check=True)
        return output_subdir
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Demucs failed: {e}")
