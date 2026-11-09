#!/usr/bin/env python3
"""Generate the MRT station MP3s with Azure Speech's en-SG-LunaNeural voice."""
import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "audio-scripts" / "ALL-STATIONS-UNIQUE.csv"
OUTPUT_DIR = ROOT / "audio" / "stations"
MANIFEST_PATH = OUTPUT_DIR / "manifest.json"
VOICE = "en-SG-LunaNeural"


def slugify(value: str) -> str:
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", value.lower()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Regenerate files even if they already exist")
    args = parser.parse_args()

    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")
    if not key or not region:
        print("Missing AZURE_SPEECH_KEY or AZURE_SPEECH_REGION environment variable.", file=sys.stderr)
        return 2
    if not CSV_PATH.exists():
        print(f"Station CSV not found: {CSV_PATH}", file=sys.stderr)
        return 2

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config = speechsdk.SpeechConfig(subscription=key, region=region)
    config.speech_synthesis_voice_name = VOICE
    config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
    )

    generated = []
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))

    for index, row in enumerate(rows, start=1):
        station = (row.get("station_name") or "").strip()
        spoken_text = (row.get("luna_text") or "").strip()
        if not station or not spoken_text:
            print(f"Skipping row {index}: missing station_name or luna_text")
            continue

        slug = slugify(station)
        destination = OUTPUT_DIR / f"{slug}.mp3"
        if destination.exists() and not args.force:
            generated.append(slug)
            print(f"[{index}/{len(rows)}] Keeping existing {destination.name}")
            continue

        audio_config = speechsdk.audio.AudioOutputConfig(filename=str(destination))
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=config, audio_config=audio_config
        )
        result = synthesizer.speak_text_async(spoken_text).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            details = getattr(result, "error_details", "Unknown synthesis error")
            raise RuntimeError(f"Failed for {station}: {details}")

        generated.append(slug)
        print(f"[{index}/{len(rows)}] Generated {destination.name}")

    # Include only MP3s that actually exist, so the website never expects a missing file.
    available = sorted(path.stem for path in OUTPUT_DIR.glob("*.mp3") if path.is_file())
    MANIFEST_PATH.write_text(json.dumps(available, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest updated with {len(available)} MP3 files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
