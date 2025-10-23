# Export Features Test Guide

## Quick Test Steps

### 1. Install Dependencies

```bash
cd /Users/siqi/Documents/PolyU/Sem1/SD5913/image2melody
pip install -r requirements.txt
```

This will install:
- `imageio` - For video encoding
- `imageio-ffmpeg` - FFmpeg codec wrapper

### 2. Run Application

```bash
./run.sh
```

### 3. Test Workflow

#### Test with Small Image (Recommended First)

1. **Load Image** - Use a small image (400×400 or less)
2. **Wait for Completion** - Let animation finish fully
3. **Check Buttons** - Should see 4 buttons:
   ```
   [ MIDI ]  [ VIDEO ]  [ AUDIO ]  [ NEW ]
   ```
4. **Test Each Export**:
   - Click **MIDI** → Save as `test.mid` → Check file exists
   - Click **VIDEO** → Save as `test.mp4` → Wait for encoding → Play video
   - Click **AUDIO** → Save as `test.wav` → Play audio

---

## Expected Behavior

### After Animation Completes

**Status Bar:**
```
[ COMPLETE ] Generated 250 notes, 250 frames | EXPORT OPTIONS
```

**Buttons:**
- **MIDI** - Always available (if notes were generated)
- **VIDEO** - Only if frames were recorded
- **AUDIO** - Always available (if notes were generated)
- **NEW** - Always available

**Hover Effects:**
- Buttons turn pink when mouse hovers
- Cursor changes to hand pointer

---

## File Outputs

### MIDI File
- **Size**: 10-50 KB
- **Format**: Standard MIDI (.mid)
- **Test**: Open in GarageBand / Logic Pro / FL Studio

### VIDEO File
- **Size**: 2-10 MB (depends on length)
- **Format**: MP4 with H.264 codec
- **Test**: Play in VLC / QuickTime
- **Note**: NO audio in video (export separately)

### AUDIO File
- **Size**: 5-20 MB (uncompressed)
- **Format**: WAV, 44.1kHz, 16-bit mono
- **Test**: Play in any audio player
- **Sound**: 8-bit square wave (chiptune style)

---

## Troubleshooting

### Error: "imageio library is required"

**Solution:**
```bash
pip install imageio imageio-ffmpeg
```

### VIDEO/AUDIO Buttons Missing

**Cause**: Animation didn't complete or stopped early

**Solution**: 
- Let animation finish completely
- Don't press space to pause near end
- Use smaller image for testing

### Video Export is Slow

**Normal**: 500+ frames takes 30-60 seconds to encode

**Tips**:
- Test with small images first (200-300 pixels)
- Check terminal for progress
- Be patient with FFmpeg encoding

### Audio Sounds Different from Playback

**Normal**: WAV export uses pure square waves

**Expected**: Timing and pitches are identical, timbre may vary slightly

---

## Quick Verification

Run this checklist:

- [ ] All 4 buttons appear after animation
- [ ] Hover effects work (pink highlight)
- [ ] MIDI exports successfully
- [ ] VIDEO exports and plays
- [ ] AUDIO exports and plays
- [ ] Status bar updates after each export
- [ ] Can load new image after export

---

## Example: Combine Video + Audio

### Using iMovie (macOS)

1. Export VIDEO as `animation.mp4`
2. Export AUDIO as `sound.wav`
3. Open iMovie
4. Import both files
5. Drag to timeline
6. Align tracks
7. Export final video

### Using FFmpeg (Command Line)

```bash
ffmpeg -i animation.mp4 -i sound.wav -c:v copy -c:a aac -strict experimental output.mp4
```

---

## Success!

If you can export all three formats and play them back, the feature is working correctly! 🎉

**Next Steps:**
- Try with your own images
- Experiment with different sizes
- Share your glitch art videos!
