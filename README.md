# audioleft

Extract audio from video files while preserving the original audio codec (no re-encoding).

## Features

- ✅ Extract audio with original codec (codec copy, no quality loss)
- ✅ Support for common video formats (MP4, AVI, MKV, etc.)
- ✅ Automatic output directory creation
- ✅ Overwrites existing files
- ✅ Simple CLI interface

## Requirements

- Python 3.10+
- ffmpeg (system dependency)

### Install ffmpeg (Ubuntu/WSL2)

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

## Installation

```bash
# Install in editable mode
pip install -e .
```

## Usage

### Basic usage (output to default directory)

```bash
audioleft --input /path/to/video.mp4
```

Output will be saved to `autokr2/audio_data/video.mp4` (with audio codec preserved).

### Specify output path

```bash
audioleft --input /path/to/video.mp4 --output /path/to/output.aac
```

### Command-line options

- `--input <path>` (required): Path to input video file
- `--output <path>` (optional): Path to output audio file. If not specified, saves to `autokr2/audio_data/` directory

## Examples

```bash
# Extract audio from MP4 video
audioleft --input movie.mp4

# Specify custom output location
audioleft --input movie.mp4 --output extracted_audio.aac

# Extract from MKV file
audioleft --input video.mkv --output audio.mkv
```

## How it works

The tool uses `ffmpeg` with codec copy (`-acodec copy`) to extract audio without re-encoding, which:
- Preserves original audio quality
- Fast extraction (no encoding overhead)
- Keeps original codec format

## Error Handling

- Throws exception if input file doesn't exist
- Throws exception if input path is invalid
- Throws exception if ffmpeg is not installed
- Automatically creates output directory if it doesn't exist
- Overwrites existing output files

## License

MIT
