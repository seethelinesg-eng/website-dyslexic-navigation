# Luna station audio preparation

This folder contains the station text scripts for the SeeTheLine SG MRT map.

## Files
- `ALL-STATIONS-UNIQUE.csv`: one row per distinct station name. Use this to generate one MP3 per station.
- `NSL.csv`, `EWL.csv`, `NEL.csv`, `CCL.csv`, `DTL.csv`, `TEL.csv`: line-by-line versions. Interchange stations appear on more than one line, so use the unique master file to avoid generating duplicates.

## Generating the recordings
1. Open the Luna voice page: https://speakscribe.me/voices/english/en-sg-lunaneural
2. Copy the `luna_text` value for one station into the generator and export an MP3.
3. Name the MP3 using the station name in lowercase, with spaces and punctuation replaced by hyphens. Examples: `pasir-ris.mp3`, `one-north.mp3`, `marina-south-pier.mp3`.
4. Put the MP3 files in `audio/stations/`.

The `luna_text` column uses the pronunciation cues already present in the map wherever available. Rows marked "station spelling (needs listening check)" do not yet have a custom cue; preview those carefully before using them.

## Website playback
The map is being prepared to prefer these MP3 recordings when their filenames are listed in `audio/stations/manifest.json`. The manifest is a JSON array of filename slugs without the `.mp3` extension, for example:

```json
["pasir-ris","tampines","simei"]
```

If a station is not in the manifest or its MP3 is unavailable, the map will continue using its existing browser speech fallback. Do not upload API keys or credentials to this public GitHub repository.

 
## Automated generation with Azure Speech
A manual GitHub Actions workflow is available at **Actions → Generate Singapore MRT station audio → Run workflow**.

Before running it, an adult helping with the project should:
1. Create an Azure Speech resource and check the current pricing.
2. In the repository, open **Settings → Secrets and variables → Actions → New repository secret**.
3. Add `AZURE_SPEECH_KEY` with the Speech resource key and `AZURE_SPEECH_REGION` with the resource region.
4. Keep both values private. Never put them in website files, CSVs, commits, or chat messages.

The workflow uses the `en-SG-LunaNeural` voice and the existing `luna_text` pronunciation column. It creates one MP3 per distinct station, updates the manifest, and commits the generated files to the repository. By default it keeps existing MP3s; the optional regenerate setting replaces them.
