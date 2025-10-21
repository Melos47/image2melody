# Quick Test Guide - Dithering & Data Moshing

## How to Test the New Features

### 1. Launch the Application
```bash
./run.sh
```

### 2. Load an Image
- Click the **LOAD IMAGE** button (beige button in center)
- Select any image (PNG, JPG, etc.)
- A popup will appear showing image info

### 3. Watch for Dithering Phase
When you click **START ANIMATION**, watch the status bar:
```
[ DITHERING ] Applying 1-bit dithering...
```

This converts your image to 1-bit black & beige using Floyd-Steinberg algorithm.

### 4. Observe Data Moshing During Animation

**Early Phase (0-30%)**
- Clean or very light glitches
- No ⚡ indicator
- Status: `[ PLAYING ] Block (x,y) RGB(...) | X/Y | Z%`

**Peak Phase (30-70%)**
- Heavy glitching effects
- ⚡ indicator appears in status bar
- Status: `[ PLAYING ] ⚡ Block (x,y) RGB(...) | X/Y | Z%`
- Watch for:
  - Pixel blocks jumping around
  - Pink/beige color streaks
  - Horizontal scanline smearing

**Fade Phase (70-100%)**
- Glitches gradually reduce
- ⚡ indicator disappears
- Returns to stable state

### 5. Visual Effects to Look For

#### Floyd-Steinberg Dithering
✓ Image converted to only black (#010101) and beige (#CDBEB8)
✓ Details preserved through dot patterns
✓ Authentic Mac OS Classic 1-bit aesthetic
✓ No color gradients, only patterns

#### Data Moshing Glitches
✓ **Displacement**: Rectangular chunks shifted horizontally/vertically
✓ **Color Shift**: Pink/beige horizontal streaks
✓ **Scanline**: Horizontal smearing/stretching
✓ **Progressive**: Glitches intensify then fade

### 6. Test Different Images

**Best Results:**
- Photos with faces (dithering creates iconic halftone effect)
- High contrast images (black/white separation)
- Detailed patterns (dithering preserves texture)

**Interesting Results:**
- Landscapes (dithering creates artistic patterns)
- Text/logos (clean 1-bit conversion)
- Gradients (shows dithering error diffusion)

### 7. Control the Animation

**Keyboard Controls:**
- `[W]` - Pitch up (octave +12)
- `[S]` - Pitch down (octave -12)
- `[A]` - Pitch down (semitone -1)
- `[D]` - Pitch up (semitone +1)
- `[SPACE]` - Pause/Resume

**Mouse Controls:**
- Hover over buttons → Hand cursor
- Click buttons → Beige → Pink color change

### 8. Save Your Work

After animation completes:
- Click **SAVE MIDI** to export melody
- Click **LOAD NEW** to try another image

---

## Expected Behavior

### Successful Dithering
```
Console Output:
✓ Using Jersey 10 font
[ User loads image ]
[ Dithering phase: 50-200ms ]
[ Animation starts with dithered image ]
```

### Successful Data Moshing
```
Status Bar Progression:
0-30%:   [ PLAYING ] Block (2,3) RGB(205,190,184) | 12/70 | 17.1%
30-70%:  [ PLAYING ] ⚡ Block (5,4) RGB(1,1,1) | 35/70 | 50.0%
70-100%: [ PLAYING ] Block (9,6) RGB(205,190,184) | 68/70 | 97.1%
```

### Performance Indicators
- Dithering: Brief pause before animation starts
- Moshing: Occasional visual corruption every 5 frames
- No lag or freezing (glitches are intentional, not bugs!)

---

## Troubleshooting

### "Image looks normal, not dithered"
- Make sure you started a NEW animation after the update
- Check console for "✓ Using Jersey 10 font" message
- Verify image loaded successfully

### "No glitches appear"
- Glitches only appear when intensity > 0.05
- Watch for ⚡ indicator in status bar
- Peak glitching occurs at 30-70% progress
- Try loading a larger image (more pixels = more visible glitches)

### "Too many/few glitches"
- This is controlled by `moshing_intensity` in code
- Default settings: Peak at 0.21 intensity
- Glitches apply every 5 frames

### "Application crashes during dithering"
- Very large images (>4000px) may cause issues
- Try resizing image to ~1000px before loading
- Check console for error messages

---

## Quick Comparison

### Before This Update
- Original color images
- No dithering
- No glitch effects
- Modern dark theme UI

### After This Update
- 1-bit dithered images (black & beige only)
- Floyd-Steinberg error diffusion
- Progressive data moshing glitches
- Mac OS Classic pink/beige UI

---

## Test Checklist

- [ ] Application launches successfully
- [ ] Jersey 10 font loads
- [ ] LOAD IMAGE button works
- [ ] Image file dialog appears
- [ ] Popup shows image info
- [ ] START ANIMATION button works
- [ ] Status shows "[ DITHERING ] ..." message
- [ ] Image converts to black & beige (1-bit)
- [ ] Animation starts with dithered image
- [ ] Glitches appear during middle phase (30-70%)
- [ ] ⚡ indicator appears in status bar
- [ ] Glitches fade out near end (70-100%)
- [ ] SAVE MIDI button appears after completion
- [ ] LOAD NEW button works
- [ ] Audio plays during animation
- [ ] Keyboard controls work (W/A/S/D/SPACE)

---

## Example Test Session

```
1. Launch: ./run.sh
   ✓ Window opens with pink title bar
   ✓ "Scrapbook - Image2Melody" title

2. Load: Click "LOAD IMAGE"
   ✓ File dialog opens
   ✓ Select test image
   ✓ Popup appears

3. Start: Click "START ANIMATION"
   ✓ Popup closes
   ✓ Status: "[ DITHERING ] ..."
   ✓ Brief pause (100-200ms)
   ✓ Status: "[ PLAYING ] ..."

4. Watch Animation:
   0-30%:   Clean dithered blocks, black & beige only
   30-50%:  ⚡ appears, glitches start
   50-70%:  Heavy glitching, peak chaos
   70-90%:  Glitches fade, ⚡ disappears
   90-100%: Clean final frames

5. Complete:
   ✓ Status: "[ COMPLETE ] Generated X notes | SAVE MELODY?"
   ✓ SAVE MIDI and LOAD NEW buttons appear

6. Save: Click "SAVE MIDI"
   ✓ File dialog opens
   ✓ MIDI file saved successfully

7. Reload: Click "LOAD NEW"
   ✓ Canvas resets
   ✓ File dialog opens automatically
   ✓ Ready for next image
```

---

## Visual Verification

### Dithering Success
- Look at any smooth gradient in original image
- After dithering, it should show dot patterns
- No color except black (#010101) and beige (#CDBEB8)
- Details preserved through strategic dot placement

### Moshing Success
- Watch carefully during 30-70% progress
- Should see at least one of:
  - Rectangular blocks shifted/duplicated
  - Pink or beige horizontal streaks
  - Horizontal smearing effects
- Status bar shows ⚡ during glitch frames

---

Last Updated: 2025-10-21
Purpose: Testing Floyd-Steinberg Dithering & Data Moshing Features
