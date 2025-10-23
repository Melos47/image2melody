# Export Feature Update (v3.1)

## 🎉 New Features

Image2Melody now supports **multi-format export**!

### Export Options

After animation completes, you'll see these buttons:

```
[ MIDI ] [ VIDEO ] [ AUDIO ] [ NEW ]
```

---

## 📦 What Can You Export?

### 1. **MIDI** - Musical Notes
- Standard MIDI file (.mid)
- Import into any DAW (FL Studio, Ableton, Logic Pro)
- Editable musical notation

### 2. **VIDEO** - Visual Animation  
- MP4 or AVI format
- All bitmap effects and glitch history
- Ready to share on social media

### 3. **AUDIO** - Sound Waveform
- WAV file (44.1kHz, 16-bit)
- Pure 8-bit square wave audio
- Ready to combine with video

---

## 🚀 How to Use

### Basic Workflow

1. **Load Image** - Click "LOAD IMAGE" button
2. **Run Animation** - Wait for it to complete
3. **Export Files**:
   - Click **MIDI** to save music notation
   - Click **VIDEO** to save animation
   - Click **AUDIO** to save sound
4. **Load New** - Click **NEW** to start over

### Create Video with Audio

**Option A: Video Editor (Recommended)**
1. Export VIDEO as `animation.mp4`
2. Export AUDIO as `sound.wav`
3. Import both into video editor (Premiere, DaVinci Resolve, iMovie)
4. Align tracks and export final video

**Option B: Command Line (Advanced)**
```bash
# Combine using ffmpeg
ffmpeg -i animation.mp4 -i sound.wav -c:v copy -c:a aac output.mp4
```

---

## 📋 Requirements

### For Video Export

Install additional dependencies:
```bash
pip install imageio imageio-ffmpeg
```

Or update all dependencies:
```bash
pip install -r requirements.txt
```

### Already Included
- MIDI export (no extra dependencies)
- AUDIO export (uses numpy, already installed)

---

## 🎬 Technical Details

### Recording

- **Automatic**: Frames and audio recorded during animation
- **Frame Rate**: 10-60 FPS (calculated from animation speed)
- **Quality**: Full resolution bitmap frames

### File Sizes

Typical sizes for 800×600 image, 500 frames:

| Format | Size | Notes |
|--------|------|-------|
| MIDI | 10-50 KB | Very small |
| VIDEO | 2-10 MB | Compressed |
| AUDIO | 5-20 MB | Uncompressed WAV |

---

## 💡 Tips

1. **Test small images first** - Large images = more frames = longer export time
2. **Export all formats** - Keep your options open
3. **Keep MIDI files** - Re-export with different instruments later
4. **Combine in pro tools** - Use DaVinci Resolve (free) for best results

---

## 📚 Documentation

See full export guide: [`docs/EXPORT_GUIDE.md`](EXPORT_GUIDE.md)

---

## 🐛 Troubleshooting

### "imageio library is required"
```bash
pip install imageio imageio-ffmpeg
```

### Video/Audio buttons not showing
- Animation must complete fully
- Don't press STOP early
- Frames only recorded during playback

### Export is slow
- Normal for 500+ frames
- FFmpeg encoding takes time
- Check terminal for progress

---

## 🎨 Example Workflow

```
1. Load flower.jpg
2. Watch animation (2 minutes)
3. Export:
   ├─ flower_melody.mid  (for DAW)
   ├─ flower_anim.mp4    (visual)
   └─ flower_audio.wav   (sound)
4. Combine in DaVinci Resolve
5. Share on Instagram! 🎉
```

---

## 🔮 Future Plans

- Combined video+audio export (single file)
- MP3/OGG audio formats
- Adjustable video quality
- Batch processing multiple images

---

**Enjoy creating glitch art music videos!** 🎨🎵
