# Export Guide

## Overview

Image2Melody now supports exporting your animations in multiple formats:

- **MIDI**: Musical notation file
- **VIDEO**: Visual animation as MP4/AVI
- **AUDIO**: Sound as WAV file

## Export Options

### 1. Export MIDI (Music Notation)

**What it includes:**
- All musical notes generated from the image
- Timing and duration information
- Velocity (volume) data

**How to export:**
1. Run the animation
2. When complete, click the **MIDI** button
3. Choose save location
4. File will be saved as `.mid`

**Use cases:**
- Edit music in DAW software (FL Studio, Ableton, Logic Pro)
- Share with other musicians
- Import into music notation software

---

### 2. Export VIDEO (Animation)

**What it includes:**
- All visual frames from the animation
- Bitmap effect with glitch history
- Data moshing and trace effects

**Important notes:**
- Video does NOT include audio automatically
- Frame rate is calculated from animation speed
- Typical output: 10-60 FPS

**How to export:**
1. Run the animation (frames are recorded automatically)
2. When complete, click the **VIDEO** button
3. Choose MP4 or AVI format
4. Wait for rendering to complete

**Requirements:**
```bash
pip install imageio imageio-ffmpeg
```

**Use cases:**
- Share animation on social media
- Create video art
- Combine with audio in video editor (Adobe Premiere, DaVinci Resolve, etc.)

---

### 3. Export AUDIO (Sound)

**What it includes:**
- 8-bit style square wave audio
- All notes with correct timing
- Single channel (mono) WAV file

**Format specifications:**
- Sample rate: 44100 Hz
- Bit depth: 16-bit PCM
- Channels: Mono

**How to export:**
1. Run the animation
2. When complete, click the **AUDIO** button
3. Choose save location
4. File will be saved as `.wav`

**Use cases:**
- Import into video editor with exported video
- Edit audio in DAW
- Use as background music
- Sample for other projects

---

## Workflow Examples

### Create Complete Video with Audio

1. **Run animation** - Let it complete fully
2. **Export VIDEO** - Save as `animation.mp4`
3. **Export AUDIO** - Save as `audio.wav`
4. **Combine in video editor:**
   - Import both files into Adobe Premiere / DaVinci Resolve / iMovie
   - Align video and audio tracks
   - Export final video with synchronized audio

### Create Shareable Content

1. **Export VIDEO** for visuals
2. **Export MIDI** for remixing
3. Share both files so others can:
   - Watch the animation
   - Remix the music in their DAW

### Music Production

1. **Export MIDI** - Import into FL Studio / Ableton
2. **Export AUDIO** - Use as reference track
3. Replace MIDI instrument with better synths
4. Keep the bitmap animation as video backdrop for live performance

---

## Technical Details

### Video Export

- Uses `imageio` library with FFmpeg codec
- Frames captured at runtime during animation
- FPS calculated from frame timestamps
- Color space: RGB (RGBA converted automatically)

### Audio Export

- Square wave synthesis (8-bit style)
- Direct waveform generation (no MIDI playback)
- Duration matches note timing exactly
- Amplitude scaled by velocity (0-127)

### File Sizes

Typical file sizes for a 800×600 image with 500 frames:

- **MIDI**: ~10-50 KB (very small)
- **VIDEO**: ~2-10 MB (depends on length and compression)
- **AUDIO**: ~5-20 MB (depends on length)

---

## Troubleshooting

### "imageio library is required"

Install video export dependencies:
```bash
pip install imageio imageio-ffmpeg
```

### Video/Audio buttons not showing

- Make sure animation runs to completion
- Frames are only recorded during animation playback
- If you press STOP early, export may not be available

### Audio sounds different from playback

This is normal - the export uses pure square waves while pygame playback may have slight variations. The timing and pitches are identical.

### Video export is slow

- Normal for longer animations (500+ frames)
- FFmpeg encoding takes time
- Be patient, check terminal for progress

---

## Best Practices

1. **Test with small images first** - Large images create many frames
2. **Export all formats** - You can always delete what you don't need
3. **Combine in professional tools** - Use DaVinci Resolve or Premiere for best results
4. **Keep source files** - MIDI can be re-exported with different instruments

---

## Future Enhancements

Potential future features:
- Direct video+audio export (combined in one file)
- Multiple audio formats (MP3, FLAC, OGG)
- Adjustable video quality settings
- Batch export multiple images

