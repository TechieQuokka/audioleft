"""CLI entry point for audioleft."""

import argparse
import sys
from pathlib import Path

from .extractor import extract_audio, get_output_path


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        prog='audioleft',
        description='Extract audio from video files preserving original codec'
    )

    parser.add_argument(
        '--input',
        required=True,
        help='Path to input video file'
    )

    parser.add_argument(
        '--output',
        required=False,
        help='Path to output audio file (default: autokr2/audio_data/)'
    )

    args = parser.parse_args()

    try:
        # Determine output path
        if args.output:
            # Force .wav extension even if user specifies different extension
            output_path = str(Path(args.output).with_suffix('.wav'))
        else:
            output_path = get_output_path(args.input)

        print(f"Input:  {args.input}")
        print(f"Output: {output_path}")
        print("Extracting audio...")

        # Extract audio
        extract_audio(args.input, output_path)

        print("✓ Audio extraction completed successfully!")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)


if __name__ == '__main__':
    main()
