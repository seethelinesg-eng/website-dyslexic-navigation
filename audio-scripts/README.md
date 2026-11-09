# MRT station pronunciation reference

This folder contains the station pronunciation reference for the SeeTheLine SG interactive MRT map.

## Files
- `ALL-STATIONS-UNIQUE.csv`: one row per distinct station name, with its station codes, lines, and pronunciation cue.
- `NSL.csv`, `EWL.csv`, `NEL.csv`, `CCL.csv`, `DTL.csv`, `TEL.csv`: line-by-line versions. Interchange stations appear on more than one line.

## Free website audio
The website uses the browser's built-in Speech Synthesis voice. It does not need Azure, an API key, paid audio files, or a separate audio service.

When a station is selected, the map passes its pronunciation cue to speech synthesis where one is available. Safari chooses the closest available English voice on the device, prioritising Singapore English, then Malaysian and other English variants. The available voices depend on the device and macOS/Safari voice settings, so a female Singapore-English voice cannot be guaranteed on every device.

## Pronunciation notes
The map's pronunciation cues are readable phonetic guides, not official IPA transcriptions. Station names that are less predictable in English have custom cues in the map code. Please test the audio on the target device and refine any cue that sounds wrong. The voice engine may interpret phonetic spellings differently, so listening checks remain important.
