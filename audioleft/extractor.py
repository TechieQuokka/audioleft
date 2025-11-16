"""Audio extraction module using ffmpeg."""

import os
import subprocess
from pathlib import Path
from typing import Optional


def extract_audio(input_path: str, output_path: str) -> None:
    """
    Extract audio from video file using ffmpeg with codec copy.

    Args:
        input_path: Path to input video file
        output_path: Path to output audio file

    Raises:
        FileNotFoundError: If input file doesn't exist
        RuntimeError: If ffmpeg extraction fails
    """
    input_file = Path(input_path)

    # Validate input file exists
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if not input_file.is_file():
        raise ValueError(f"Input path is not a file: {input_path}")

    # Create output directory if needed
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Build ffmpeg command with codec copy (no re-encoding)
    cmd = [
        'ffmpeg',
        '-i', str(input_file),
        '-vn',  # No video
        '-acodec', 'copy',  # Copy audio codec as-is
        '-y',  # Overwrite output file if exists
        str(output_file)
    ]

    try:
        # Run ffmpeg with progress output
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Audio extraction failed:\n"
            f"STDERR: {e.stderr}\n"
            f"Command: {' '.join(cmd)}"
        ) from e
    except FileNotFoundError:
        raise RuntimeError(
            "ffmpeg not found. Please install ffmpeg:\n"
            "  sudo apt-get install ffmpeg"
        )


def get_output_path(input_path: str, output_dir: Optional[str] = None) -> str:
    """
    Generate output audio file path.

    Args:
        input_path: Input video file path
        output_dir: Output directory (optional)

    Returns:
        Output audio file path with appropriate extension
    """
    input_file = Path(input_path)

    # Keep original filename, change extension to match audio codec
    # Since we're using codec copy, we'll use a generic extension
    # Note: Extension should ideally match the actual codec, but for simplicity
    # we'll use the original extension or default to .aac
    output_name = input_file.stem + input_file.suffix

    if output_dir:
        return str(Path(output_dir) / output_name)

    # Default to autokr2/audio_data
    default_output_dir = Path(__file__).parent.parent.parent / 'audio_data'
    return str(default_output_dir / output_name)
