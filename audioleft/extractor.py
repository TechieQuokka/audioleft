"""Audio extraction module using ffmpeg."""

import json
import os
import subprocess
from pathlib import Path
from typing import Optional


def get_audio_codec(input_path: str) -> str:
    """
    Detect audio codec from video file using ffprobe.

    Args:
        input_path: Path to input video file

    Returns:
        Audio codec name (e.g., 'aac', 'mp3', 'opus')

    Raises:
        RuntimeError: If ffprobe fails or no audio stream found
    """
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        '-select_streams', 'a:0',  # Select first audio stream
        str(input_path)
    ]

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        data = json.loads(result.stdout)
        
        if not data.get('streams'):
            raise RuntimeError(f"No audio stream found in: {input_path}")
        
        codec_name = data['streams'][0].get('codec_name', 'unknown')
        return codec_name
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ffprobe failed: {e.stderr}") from e
    except FileNotFoundError:
        raise RuntimeError(
            "ffprobe not found. Please install ffmpeg:\n"
            "  sudo apt-get install ffmpeg"
        )
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse ffprobe output: {e}") from e


def get_extension_for_codec(codec: str) -> str:
    """
    Get appropriate file extension for audio codec.

    Args:
        codec: Audio codec name from ffprobe

    Returns:
        File extension with dot (e.g., '.aac', '.mp3')
    """
    codec_map = {
        'aac': '.m4a',
        'mp3': '.mp3',
        'opus': '.opus',
        'vorbis': '.ogg',
        'flac': '.flac',
        'pcm_s16le': '.wav',
        'pcm_s24le': '.wav',
        'pcm_s32le': '.wav',
        'alac': '.m4a',
        'ac3': '.ac3',
        'eac3': '.eac3',
        'dts': '.dts',
        'truehd': '.thd',
    }
    
    return codec_map.get(codec, '.mka')  # Default to Matroska audio


def extract_audio(input_path: str, output_path: str) -> None:
    """
    Extract audio from video file and convert to WAV format using ffmpeg.

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

    # Build ffmpeg command for WAV conversion
    cmd = [
        'ffmpeg',
        '-i', str(input_file),
        '-vn',  # No video
        '-acodec', 'pcm_s16le',  # Convert to 16-bit PCM (WAV format)
        '-ar', '44100',  # Sample rate: 44.1 kHz
        '-ac', '2',  # Stereo (2 channels)
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
    Generate output audio file path with .wav extension.

    Args:
        input_path: Input video file path
        output_dir: Output directory (optional)

    Returns:
        Output audio file path with .wav extension
    """
    input_file = Path(input_path)

    # Always use .wav extension
    output_name = input_file.stem + '.wav'

    if output_dir:
        return str(Path(output_dir) / output_name)

    # Default to autokr2/audio_data
    default_output_dir = Path(__file__).parent.parent.parent / 'audio_data'
    return str(default_output_dir / output_name)